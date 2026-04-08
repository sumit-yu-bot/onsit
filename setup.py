from setuptools import setup

setup(
    name="leakosint-cli",
    version="1.0.0",
    packages=["leakosint_cli"],
    install_requires=[
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "leakosint=leakosint_cli.main:main",
        ],
    },
)
