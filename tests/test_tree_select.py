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
from tests.utils import add_children


class TreeSelectTestCase(TestCase):
    def setUp(self):
        add_children(None, 0, 1, 3)

    def test_select_in_order(self):
        node_0 = TreeNode.objects.get(name="0")
        node_0_0 = TreeNode.objects.get(name="0_0")
        node_0_1 = TreeNode.objects.get(name="0_1")
        node_0_2 = TreeNode.objects.get(name="0_2")
        node_1 = TreeNode.objects.get(name="1")
        node_1_0 = TreeNode.objects.get(name="1_0")
        node_1_1 = TreeNode.objects.get(name="1_1")
        node_1_2 = TreeNode.objects.get(name="1_2")
        node_2 = TreeNode.objects.get(name="2")
        node_2_0 = TreeNode.objects.get(name="2_0")
        node_2_1 = TreeNode.objects.get(name="2_1")
        node_2_2 = TreeNode.objects.get(name="2_2")

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
        node_0 = TreeNode.objects.get(name="0")
        node_0_0 = TreeNode.objects.get(name="0_0")
        node_0_1 = TreeNode.objects.get(name="0_1")
        node_0_2 = TreeNode.objects.get(name="0_2")
        node_1 = TreeNode.objects.get(name="1")
        node_1_0 = TreeNode.objects.get(name="1_0")
        node_1_1 = TreeNode.objects.get(name="1_1")
        node_1_2 = TreeNode.objects.get(name="1_2")
        node_2 = TreeNode.objects.get(name="2")
        node_2_0 = TreeNode.objects.get(name="2_0")
        node_2_1 = TreeNode.objects.get(name="2_1")
        node_2_2 = TreeNode.objects.get(name="2_2")

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    node_0.pk,
                    {
                        "node": node_0,
                        "children": OrderedDict(
                            (
                                (
                                    node_0_0.pk,
                                    {
                                        "node": node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_0_1.pk,
                                    {
                                        "node": node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_0_2.pk,
                                    {
                                        "node": node_0_2,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    node_1.pk,
                    {
                        "node": node_1,
                        "children": OrderedDict(
                            (
                                (
                                    node_1_0.pk,
                                    {
                                        "node": node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_1_1.pk,
                                    {
                                        "node": node_1_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_1_2.pk,
                                    {
                                        "node": node_1_2,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    node_2.pk,
                    {
                        "node": node_2,
                        "children": OrderedDict(
                            (
                                (
                                    node_2_0.pk,
                                    {
                                        "node": node_2_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_2_1.pk,
                                    {
                                        "node": node_2_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    node_2_2.pk,
                                    {
                                        "node": node_2_2,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
            )
        )

        self.assertDictEqual(node_tree, expected_node_tree)
