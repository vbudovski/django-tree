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

from django.test import TestCase

from tests.models import TreeNode
from tree.services import build_tree


class TreeTestCase(TestCase):
    def setUp(self):
        self.node_0 = TreeNode.objects.create(name='0')
        self.node_1 = TreeNode.objects.create(name='1', previous=self.node_0)
        self.node_0_0 = TreeNode.objects.create(name='0_0', parent=self.node_0)
        self.node_0_1 = TreeNode.objects.create(name='0_1', parent=self.node_0, previous=self.node_0_0)
        self.node_1_0 = TreeNode.objects.create(name='1_0', parent=self.node_1)
        self.node_1_1 = TreeNode.objects.create(name='1_1', parent=self.node_1, previous=self.node_1_0)

    def test_select_in_order(self):
        nodes_in_order = (
            self.node_0,
            self.node_1,
            self.node_0_0,
            self.node_1_0,
            self.node_0_1,
            self.node_1_1,
        )

        self.assertSequenceEqual(TreeNode.objects.in_order(), nodes_in_order)

    def test_build_tree(self):
        node_tree = build_tree()

        expected_node_tree = OrderedDict((
            (self.node_0.pk, {
                'node': self.node_0,
                'children': OrderedDict((
                    (self.node_0_0.pk, {
                        'node': self.node_0_0,
                        'children': OrderedDict(),
                    }),
                    (self.node_0_1.pk, {
                        'node': self.node_0_1,
                        'children': OrderedDict(),
                    }),
                )),
            }),
            (self.node_1.pk, {
                'node': self.node_1,
                'children': OrderedDict((
                    (self.node_1_0.pk, {
                        'node': self.node_1_0,
                        'children': OrderedDict(),
                    }),
                    (self.node_1_1.pk, {
                        'node': self.node_1_1,
                        'children': OrderedDict(),
                    }),
                )),
            }),
        ))

        self.assertDictEqual(node_tree, expected_node_tree)
