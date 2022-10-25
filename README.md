# Django Tree

![CI](https://github.com/vbudovski/django-tree/workflows/Django%20CI/badge.svg)
[![Test Coverage](https://api.codeclimate.com/v1/badges/54fd3664631f52caa2e4/test_coverage)](https://codeclimate.com/github/vbudovski/django-tree/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/54fd3664631f52caa2e4/maintainability)](https://codeclimate.com/github/vbudovski/django-tree/maintainability)

## Overview

A tree structure for hierarchical data. Optimised for fast insertion/moving of nodes around the tree.


## Requirements

* Django 3.2+
* Python 3.8+


## Installation

* Add `django_tree` to `INSTALLED_APPS`.


## Usage

Simply extend the `BaseTreeNode` class in your application: e.g.

```python
from django.db import models

from django_tree.models import BaseTreeNode


class Category(BaseTreeNode):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Will contain an OrderedDict of categories organised into a tree structure.
categories = Category.objects.build_tree()
```

## Testing

1. Install dev dependencies: `poetry install`.
2. Install a supported version of Django: `pip install django==3.2`
3. Run the tests: `DB_NAME="django_tree" python -m pytest tests .`
