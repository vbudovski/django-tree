from django.db import models

from django_tree.models import BaseTreeNode


class TreeNode(BaseTreeNode):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return self.name
