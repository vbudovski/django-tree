from setuptools import find_packages
from setuptools import setup


def read_readme():
    with open("README.md") as readme:
        return readme.read()


setup(
    name="django-tree",
    version="0.1",
    url="https://github.com/vbudovski/django-tree",
    license="Apache Software License 2.0",
    description="Tree structure for hierarchical data",
    long_descriptiption=read_readme(),
    long_description_content_type="text/markdown",
    author="Vitaly Budovski",
    author_email="vbudovski@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=["django>=2.2"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License 2.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
