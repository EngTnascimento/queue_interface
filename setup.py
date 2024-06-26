# setup.py
from setuptools import find_packages, setup

setup(
    name="queue_interface",
    version="0.1.0",
    author="Thiago Nascimento",
    author_email="ieng.tnascimento@outlook.com",
    description="Queue services interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EngTnascimento/queue_interface",
    packages=find_packages(),
    install_requires=[
        "pika==1.3.2",
        "pydantic==2.7.4",
        "pydantic-settings==2.3.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
