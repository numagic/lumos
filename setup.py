import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="numagic-lumos",
    version="0.0.2rc7",
    author="Yunlong Xu",
    author_email="yunlong@numagic.io",
    description="lumos - scalable accelerated optimal control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/numagic/lumos",
    project_urls={"Bug Tracker": "https://github.com/numagic/lumos/issues"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["lumos", "lumos.*"]),
    python_requires=">=3.7",
)
