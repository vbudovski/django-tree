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

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import transaction


class BaseTreeNodeManager(models.Manager):
    def in_order(self):
        table_name = self.model._meta.db_table
        query = f"""
            SELECT nodes.*, depth, index
            FROM
            {table_name} nodes,
            (
                WITH RECURSIVE depth_cte AS (
                    SELECT id, parent_id, 0 as depth
                    FROM {table_name}
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT
                    t.id,
                    t.parent_id,
                    CASE
                        WHEN t.parent_id = depth_cte.id THEN depth_cte.depth + 1
                        ELSE 0
                    END AS depth
                    FROM {table_name} t
                    INNER JOIN depth_cte ON depth_cte.id = t.parent_id
                )
                SELECT id, depth
                FROM depth_cte
            ) depth_cte,
            (
                WITH RECURSIVE index_cte AS (
                    SELECT id, previous_id, 0 as index
                    FROM {table_name}
                    WHERE previous_id IS NULL
                    UNION ALL
                    SELECT
                    t.id,
                    t.previous_id,
                    CASE
                        WHEN t.previous_id = index_cte.id THEN index_cte.index + 1
                        ELSE 0
                    END AS index
                    FROM {table_name} t
                    INNER JOIN index_cte ON index_cte.id = t.previous_id
                )
                SELECT id, index
                FROM index_cte
            ) index_cte
            WHERE nodes.id = depth_cte.id
            AND depth_cte.id = index_cte.id
            ORDER BY depth, index, id
        """

        return self.get_queryset().raw(query)

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
