from setuptools import setup, find_packages

setup(
    name="sleekify",
    version="0.0.15",
    author="Matt J. Stevenson",
    author_email="dev@mattjs.me",
    description="Sleekify: A minimalistic, ASGI Python framework for building REST API's.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0mjs/sleekify",
    packages=find_packages(),
    install_requires=[
        "uvicorn",
        "starlette",
        "pydantic",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
