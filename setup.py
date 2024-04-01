from setuptools import setup, find_packages

setup(
    name="ai_models_lib",
    version="0.1.0",
    author="Ashley Zhang",
    author_email="ashzhang@wharton.upenn.edu",
    description="Python library for interfacing with different models / model providers.",
    url="https://github.com/ashleyzhang01/ai_models_library",
    packages=find_packages(),
    python_requires=">=3.11",
)
