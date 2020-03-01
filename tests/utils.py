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


from typing import Optional

from django.db import transaction

from tests.models import TreeNode


@transaction.atomic
def add_children(parent: Optional[TreeNode], depth: int, max_depth: int, nodes_per_level: int):
    if parent is None:
        prefix = ''
    else:
        prefix = f'{parent.name}_'

    nodes = []
    for i in range(nodes_per_level):
        try:
            previous = nodes[i - 1]
        except IndexError:
            previous = None

        new_node = TreeNode.objects.create(name=f'{prefix}{i}', parent=parent, previous=previous)
        nodes.append(new_node)

    if depth < max_depth:
        for node in nodes:
            add_children(node, depth + 1, max_depth, nodes_per_level)
