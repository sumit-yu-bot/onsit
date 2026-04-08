from setuptools import setup, find_packages

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "LeakOSINT CLI - Command-line tool for OSINT searches"

setup(
    name="leakosint-cli",
    version="1.0.0",
    author="Sumit",
    author_email="your.email@example.com",
    description="CLI tool for LeakOSINT API - Search leaked data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sumit-yu-bot/onsit",
    packages=["leakosint_cli"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "leakosint=leakosint_cli.main:main",
        ],
    },
)
