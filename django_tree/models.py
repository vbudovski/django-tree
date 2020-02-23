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


import functools

from django.db import models
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
            )
        )


class BaseTreeNode(models.Model):
    objects = BaseTreeNodeManager()

    parent = models.ForeignKey('self', related_name='children', null=True, on_delete=models.PROTECT)
    previous = models.OneToOneField('self', related_name='next', null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True
