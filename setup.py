from setuptools import setup, find_packages

setup(
    name="zephyr",
    version="0.0.1",
    description="A lightweight ASGI framework for Python",
    author="Matt J. Stevenson",
    author_email="dev@mattjs.me",
    packages=find_packages(),
    install_requires=["httpx", "uvicorn", "starlette", "pydantic"],
    python_requires=">=3.11",
)
