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


class TreeInsertTestCase(TestCase):
    def setUp(self) -> None:
        self.node_0 = TreeNode.objects.create(name="0")
        self.node_1 = TreeNode.objects.create(name="1", previous=self.node_0)
        self.node_0_0 = TreeNode.objects.create(name="0_0", parent=self.node_0)
        self.node_0_1 = TreeNode.objects.create(
            name="0_1", parent=self.node_0, previous=self.node_0_0
        )
        self.node_1_0 = TreeNode.objects.create(name="1_0", parent=self.node_1)
        self.node_1_1 = TreeNode.objects.create(
            name="1_1", parent=self.node_1, previous=self.node_1_0
        )

    def test_insert_before_first(self):
        before_first = TreeNode.objects.create(name="before_first")

        TreeNode.objects.insert_before(self.node_0, before_first)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    before_first.pk,
                    {
                        "node": before_first,
                        "children": OrderedDict(),
                    },
                ),
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_before_last(self):
        before_last = TreeNode.objects.create(name="before_last")

        TreeNode.objects.insert_before(self.node_1, before_last)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    before_last.pk,
                    {
                        "node": before_last,
                        "children": OrderedDict(),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_before_first_child(self):
        before_first_child = TreeNode.objects.create(name="before_first_child")

        TreeNode.objects.insert_before(self.node_0_0, before_first_child)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    before_first_child.pk,
                                    {
                                        "node": before_first_child,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_before_last_child(self):
        before_last_child = TreeNode.objects.create(name="before_last_child")

        TreeNode.objects.insert_before(self.node_0_1, before_last_child)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    before_last_child.pk,
                                    {
                                        "node": before_last_child,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_after_first(self):
        after_first = TreeNode.objects.create(name="after_first")

        TreeNode.objects.insert_after(self.node_0, after_first)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    after_first.pk,
                    {
                        "node": after_first,
                        "children": OrderedDict(),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_after_last(self):
        after_last = TreeNode.objects.create(name="after_last")

        TreeNode.objects.insert_after(self.node_1, after_last)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    after_last.pk,
                    {
                        "node": after_last,
                        "children": OrderedDict(),
                    },
                ),
            )
        )

        self.assertDictEqual(node_tree, expected_node_tree)

    def test_insert_after_first_child(self):
        after_first_child = TreeNode.objects.create(name="after_first_child")

        TreeNode.objects.insert_after(self.node_0_0, after_first_child)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    after_first_child.pk,
                                    {
                                        "node": after_first_child,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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

    def test_insert_after_last_child(self):
        after_last_child = TreeNode.objects.create(name="after_last_child")

        TreeNode.objects.insert_after(self.node_0_1, after_last_child)

        node_tree = TreeNode.objects.build_tree()

        expected_node_tree = OrderedDict(
            (
                (
                    self.node_0.pk,
                    {
                        "node": self.node_0,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_0_0.pk,
                                    {
                                        "node": self.node_0_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_0_1.pk,
                                    {
                                        "node": self.node_0_1,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    after_last_child.pk,
                                    {
                                        "node": after_last_child,
                                        "children": OrderedDict(),
                                    },
                                ),
                            )
                        ),
                    },
                ),
                (
                    self.node_1.pk,
                    {
                        "node": self.node_1,
                        "children": OrderedDict(
                            (
                                (
                                    self.node_1_0.pk,
                                    {
                                        "node": self.node_1_0,
                                        "children": OrderedDict(),
                                    },
                                ),
                                (
                                    self.node_1_1.pk,
                                    {
                                        "node": self.node_1_1,
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
