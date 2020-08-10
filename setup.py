import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="margo",
    version="0.0.1",
    author="Jinyu Hou",
    author_email="jhou@lunenfeld.ca",
    description="A tool that generates yaml cell type marker which maps cell types to gene expression.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camlab-bioml/margo",
    packages=["margo"],
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
    scripts=["bin/margo"],
)
