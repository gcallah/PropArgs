import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PropArgs",
    version="0.0.1",
    author="Nathan Conroy, Gene Callahan",
    author_email="nathanconroydev@gmail.com",
    description="A module for systematically organizing user preferences acquired "
                "from a database, env vars, a parameter file, or user choices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gcallah/PropArgs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
