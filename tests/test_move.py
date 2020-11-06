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


from django.test import TestCase

from tests.models import TreeNode
from tests.utils import add_children


class MoveTestCase(TestCase):
    def test_move_front_to_back_top_level(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_0 = TreeNode.objects.get(name="0")
        node_1 = TreeNode.objects.get(name="1")
        node_2 = TreeNode.objects.get(name="2")

        TreeNode.objects.insert_after(node_2, node_0)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        order = [
            ("1", 0, 0),
            ("2", 0, 1),
            ("0", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

        TreeNode.objects.insert_after(node_0, node_1)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        order = [
            ("2", 0, 0),
            ("0", 0, 1),
            ("1", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

        TreeNode.objects.insert_after(node_1, node_2)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

    def test_move_back_to_front_top_level(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_0 = TreeNode.objects.get(name="0")
        node_1 = TreeNode.objects.get(name="1")
        node_2 = TreeNode.objects.get(name="2")

        TreeNode.objects.insert_before(node_0, node_2)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        order = [
            ("2", 0, 0),
            ("0", 0, 1),
            ("1", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

        TreeNode.objects.insert_before(node_2, node_1)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        order = [
            ("1", 0, 0),
            ("2", 0, 1),
            ("0", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

        TreeNode.objects.insert_before(node_1, node_0)
        node_0.refresh_from_db()
        node_1.refresh_from_db()
        node_2.refresh_from_db()

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

    def test_move_leaf_before_first(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_0 = TreeNode.objects.get(name="0")
        node_2_2 = TreeNode.objects.get(name="2_2")
        TreeNode.objects.insert_before(node_0, node_2_2)

        order = [
            ("2_2", 0, 0),
            ("0", 0, 1),
            ("1", 0, 2),
            ("2", 0, 3),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

    def test_move_second_level_node_before_first(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_0 = TreeNode.objects.get(name="0")
        node_1_1 = TreeNode.objects.get(name="1_1")
        TreeNode.objects.insert_before(node_0, node_1_1)

        order = [
            ("1_1", 0, 0),
            ("0", 0, 1),
            ("1", 0, 2),
            ("2", 0, 3),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_2", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

    def test_move_leaf_after_last(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_2 = TreeNode.objects.get(name="2")
        node_0_0 = TreeNode.objects.get(name="0_0")
        TreeNode.objects.insert_after(node_2, node_0_0)

        order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 0, 3),
            ("0_1", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_2", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )

    def test_move_second_level_node_after_last(self):
        add_children(None, 0, max_depth=1, nodes_per_level=3)

        initial_order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_1", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("1_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()],
            initial_order,
        )

        node_2 = TreeNode.objects.get(name="2")
        node_1_1 = TreeNode.objects.get(name="1_1")
        TreeNode.objects.insert_after(node_2, node_1_1)

        order = [
            ("0", 0, 0),
            ("1", 0, 1),
            ("2", 0, 2),
            ("1_1", 0, 3),
            ("0_0", 1, 0),
            ("1_0", 1, 0),
            ("2_0", 1, 0),
            ("0_1", 1, 1),
            ("1_2", 1, 1),
            ("2_1", 1, 1),
            ("0_2", 1, 2),
            ("2_2", 1, 2),
        ]

        self.assertSequenceEqual(
            [(n.name, n.depth, n.index) for n in TreeNode.objects.in_order()], order
        )
