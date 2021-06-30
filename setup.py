import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="end-of-file",
    version="0.0.1",
    author="Martin Moravek",
    author_email="moravek.martin@gmail.com",
    description="Small utility to ensure files end with one newline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keeo/end-of-file",
    project_urls={
        "Bug Tracker": "https://github.com/Keeo/end-of-file/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
