# Django Tree

[![Build Status](https://travis-ci.com/vbudovski/django-tree.svg?branch=master)](https://travis-ci.com/vbudovski/django-tree)
[![Coverage Status](https://codecov.io/gh/vbudovski/django-tree/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/vbudovski/django-tree)

## Overview

A tree structure for hierarchical data. Optimised for fast insertion/moving of nodes around the tree.


## Requirements

* Django 2.2+
* Python 3.6+


## Installation

* Add `django_tree` to `INSTALLED_APPS`.


## Usage

Simply extend the `BaseTreeNode` class in your application: e.g.

```python
from django.db import models

from django_tree.models import BaseTreeNode
from django_tree.services import build_tree


class Category(BaseTreeNode):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Will contain an OrderedDict of categories organised into a tree structure.
categories = build_tree()
```
