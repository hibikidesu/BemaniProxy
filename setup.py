from setuptools import setup


setup(
    name="bemaniproxy",
    author="hibikidesu",
    packages=["bemaniproxy"],
    version="1.0.0",
    entry_points={
        "console_scripts": "bemaniproxy=bemaniproxy:run"
    }
)
