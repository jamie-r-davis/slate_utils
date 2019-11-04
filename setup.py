from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="slate_utils",
    version="0.0.2",
    author="Jamie Davis",
    author_email="jamjam@umich.edu",
    description=("Some simple utilites to help automate tasks in Slate."),
    license="BSD",
    packages=["slate_utils"],
    long_description=readme(),
    classifiers=[],
    install_requires=["selenium"],
)
