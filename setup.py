import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="intesis_wmp",
    version="0.0.1",
    author="Myles Eftos",
    author_email="myles@madpilot.com.au",
    description="Python library for talking to Intesis devices using WMP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/madpilot/pyintesiswmp",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
