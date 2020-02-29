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
from typing import Optional

from django.db import transaction
from django.test import TestCase

from tests.models import TreeNode


class TreeSelectTestCase(TestCase):
    @transaction.atomic
    def add_children(self, parent: Optional[TreeNode], depth: int, max_depth: int):
        if parent is None:
            prefix = ''
        else:
            prefix = f'{parent.name}_'

        nodes = []
        for i in range(3):
            try:
                previous = nodes[i - 1]
            except IndexError:
                previous = None

            new_node = TreeNode.objects.create(name=f'{prefix}{i}', parent=parent, previous=previous)
            nodes.append(new_node)

        if depth < max_depth:
            for node in nodes:
                self.add_children(node, depth + 1, max_depth)

    def setUp(self):
        self.add_children(None, 0, 1)

    def test_select_in_order(self):
        node_0 = TreeNode.objects.get(name='0')
        node_0_0 = TreeNode.objects.get(name='0_0')
        node_0_1 = TreeNode.objects.get(name='0_1')
        node_0_2 = TreeNode.objects.get(name='0_2')
        node_1 = TreeNode.objects.get(name='1')
        node_1_0 = TreeNode.objects.get(name='1_0')
        node_1_1 = TreeNode.objects.get(name='1_1')
        node_1_2 = TreeNode.objects.get(name='1_2')
        node_2 = TreeNode.objects.get(name='2')
        node_2_0 = TreeNode.objects.get(name='2_0')
        node_2_1 = TreeNode.objects.get(name='2_1')
        node_2_2 = TreeNode.objects.get(name='2_2')

        nodes_in_order = (
            node_0,
            node_1,
            node_2,
            node_0_0,
            node_1_0,
            node_2_0,
            node_0_1,
            node_1_1,
            node_2_1,
            node_0_2,
            node_1_2,
            node_2_2,
        )

        self.assertSequenceEqual(TreeNode.objects.in_order(), nodes_in_order)

    def test_build_tree(self):
        node_0 = TreeNode.objects.get(name='0')
        node_0_0 = TreeNode.objects.get(name='0_0')
        node_0_1 = TreeNode.objects.get(name='0_1')
        node_0_2 = TreeNode.objects.get(name='0_2')
        node_1 = TreeNode.objects.get(name='1')
        node_1_0 = TreeNode.objects.get(name='1_0')
        node_1_1 = TreeNode.objects.get(name='1_1')
        node_1_2 = TreeNode.objects.get(name='1_2')
        node_2 = TreeNode.objects.get(name='2')
        node_2_0 = TreeNode.objects.get(name='2_0')
        node_2_1 = TreeNode.objects.get(name='2_1')
        node_2_2 = TreeNode.objects.get(name='2_2')

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict((
            (node_0.pk, {
                'node': node_0,
                'children': OrderedDict((
                    (node_0_0.pk, {
                        'node': node_0_0,
                        'children': OrderedDict(),
                    }),
                    (node_0_1.pk, {
                        'node': node_0_1,
                        'children': OrderedDict(),
                    }),
                    (node_0_2.pk, {
                        'node': node_0_2,
                        'children': OrderedDict(),
                    }),
                )),
            }),
            (node_1.pk, {
                'node': node_1,
                'children': OrderedDict((
                    (node_1_0.pk, {
                        'node': node_1_0,
                        'children': OrderedDict(),
                    }),
                    (node_1_1.pk, {
                        'node': node_1_1,
                        'children': OrderedDict(),
                    }),
                    (node_1_2.pk, {
                        'node': node_1_2,
                        'children': OrderedDict(),
                    }),
                )),
            }),
            (node_2.pk, {
                'node': node_2,
                'children': OrderedDict((
                    (node_2_0.pk, {
                        'node': node_2_0,
                        'children': OrderedDict(),
                    }),
                    (node_2_1.pk, {
                        'node': node_2_1,
                        'children': OrderedDict(),
                    }),
                    (node_2_2.pk, {
                        'node': node_2_2,
                        'children': OrderedDict(),
                    }),
                )),
            }),
        ))

        self.assertDictEqual(node_tree, expected_node_tree)
