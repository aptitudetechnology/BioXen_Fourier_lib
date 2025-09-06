from setuptools import setup, find_packages

setup(
    name="bioxen_jcvi_vm_lib",
    version="0.0.6",
    author="aptitudetechnology",
    author_email="support@aptitudetechnology.com",
    description="BioXen Hypervisor-focused biological VM management library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aptitudetechnology/BioXen_jcvi_vm_lib",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pylua-bioxen-vm-lib>=0.1.22",
        "questionary>=2.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bioxen=cli.main:main",
        ],
    },
)
