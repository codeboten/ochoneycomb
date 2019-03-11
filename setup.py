import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ochoneycomb",
    version="0.0.1",
    author="Alex Boten",
    author_email="alrex.boten@gmail.com",
    description="OpenCensus exporter for Honeycomb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codeboten/opencensus-python-honeycomb-exporter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'libhoney',
        'opencensus',
    ],
)
