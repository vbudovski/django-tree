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

from tests.models import TreeNode


def build_tree():
    ordered_nodes = TreeNode.objects.in_order()

    node_tree = OrderedDict()
    for node in ordered_nodes:
        if node.depth == 0:
            insert_into = node_tree
        else:
            insert_into = node_tree[node.parent_id]['children']

        insert_into[node.pk] = {
            'node': node,
            'children': OrderedDict(),
        }

    return node_tree
