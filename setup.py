from setuptools import setup, find_namespace_packages

setup(
    name="Clean_folder",
    version="0.0.23",
    description="Garbadge sorter",
    url="https://github.com/JurijProcenko/clean_folder.git",
    author="Yurii Protsenko",
    author_email="elsoul@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["cleanfolder = clean_folder.clean:main"]},
)
