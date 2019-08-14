import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feign",
    version="1.0.0",
    author="Zsolt Elter",
    description="feign: geometric efficiency in spent fuel passive gamma spectroscopy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ezsolti/feign",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "matplotlib"
    ]
)
