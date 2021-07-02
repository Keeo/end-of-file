import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="end-of-file",
    version="1.0.1",
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
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "Click",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "eof=end_of_file:format",
        ],
    },
)
