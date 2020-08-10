import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mentor",
    version="0.0.1",
    author="Jinyu Hou",
    author_email="jhou@lunenfeld.ca",
    description=" ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camlab-bioml/mentor",
    packages=["mentor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="GPLv2",
    install_requires=[
        "pandas",
        "pyyaml",
        "argparse",
        "rootpath"
        # "sphinx",
        # "rinohtype"
    ],
    include_package_data=True,
    scripts=["bin/mentor"],
)
