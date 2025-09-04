from setuptools import setup, find_packages

setup(
    name="bioxen-jcvi-vm-lib",
    version="0.0.4",
    author="aptitudetechnology",
    author_email="support@aptitudetechnology.com",
    description="BioXen Factory Pattern API for biological VM management with JCVI integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aptitudetechnology/BioXen_jcvi_vm_lib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "questionary",
        "setuptools",
        "wheel",
        "twine",
    ],
)
