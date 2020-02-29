# Copyright [2020] [Vitaly Budovski]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from collections import OrderedDict
import functools

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import transaction
from django.db.models import Case
from django.db.models import Value
from django.db.models import When
from django.db.models.expressions import OuterRef
from django.db.models.expressions import Subquery
from django_cte import CTEManager
from django_cte import CTEQuerySet
from django_cte import With


class BaseTreeNodeManager(CTEManager):
    def in_order(self):
        def _make_cte(cte: CTEManager, key: str, result: str) -> CTEQuerySet:
            return (
                self.get_queryset()
                .filter(**{key: None})
                .values(
                    'id',
                    key,
                    **{result: Value(0, output_field=models.IntegerField())},
                )
                .union(
                    cte
                    .join(
                        self.model,
                        **{key: cte.col.pk},
                    )
                    .values(
                        'id',
                        key,
                        **{
                            result: Case(
                                When(
                                    **{key: cte.col.pk},
                                    then=getattr(cte.col, result) + Value(1, output_field=models.IntegerField()),
                                ),
                                default=Value(0, output_field=models.IntegerField()),
                            ),
                        },
                    ),
                    all=True,
                )
            )

        def make_annotated_query(key: str, result: str):
            make_cte = functools.partial(_make_cte, key=key, result=result)

            cte = With.recursive(make_cte)
            return (
                cte
                .join(
                    self.model,
                    pk=cte.col.pk,
                )
                .with_cte(cte)
                .annotate(**{result: getattr(cte.col, result)})
            )

        nodes_by_index = make_annotated_query('previous', 'index')
        nodes_by_depth = make_annotated_query('parent', 'depth')

        return (
            nodes_by_depth
            .annotate(
                index=Subquery(nodes_by_index.filter(pk=OuterRef('pk')).values('index')),
            )
            .order_by(
                'depth',
                'index',
                'pk',
            )
        )

    def build_tree(self) -> OrderedDict:
        ordered_nodes = self.in_order()

        node_tree = OrderedDict()
        paths = OrderedDict()
        for node in ordered_nodes:
            if node.parent_id is None:
                paths[node.pk] = [node.pk]
            else:
                paths[node.pk] = paths[node.parent_id] + [node.pk]

            insert_into = node_tree
            for node_id in paths[node.pk]:
                if node_id in insert_into:
                    insert_into = insert_into[node_id]['children']
                else:
                    insert_into[node_id] = {
                        'node': node,
                        'children': OrderedDict(),
                    }

        return node_tree

    @transaction.atomic
    def insert_before(self, node: 'BaseTreeNode', new_node: 'BaseTreeNode'):
        old_previous = node.previous

        node.previous = new_node
        node.save(update_fields=['previous'])

        new_node.parent = node.parent
        new_node.previous = old_previous
        new_node.save(update_fields=['parent', 'previous'])

    @transaction.atomic
    def insert_after(self, node: 'BaseTreeNode', new_node: 'BaseTreeNode'):
        try:
            new_node_next = new_node.next
        except ObjectDoesNotExist:
            pass
        else:
            new_node_next.previous = new_node.previous
            new_node_next.save(update_fields=['previous'])

        try:
            old_next = node.next
        except ObjectDoesNotExist:
            pass
        else:
            old_next.previous = new_node
            old_next.save(update_fields=['previous'])

        new_node.parent = node.parent
        new_node.previous = node
        new_node.save(update_fields=['parent', 'previous'])


class BaseTreeNode(models.Model):
    objects = BaseTreeNodeManager()

    parent = models.ForeignKey('self', related_name='children', null=True, on_delete=models.PROTECT)
    previous = models.OneToOneField('self', related_name='next', null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True
