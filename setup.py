import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TracTaskCare",
    version="0.20191101.8",
    author="Gea-Suan Lin",
    author_email="darkkiller@gmail.com",
    description="Sync updates to task.care.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gslin/trac-taskcare",
    packages=setuptools.find_packages(),
    install_requires=["Trac>=0.10", "requests"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Apprived :: MIT License",
        "Operating System :: OS :: Independent",
    ],
    python_requires=">=2.7",
    entry_points={
        "trac.plugins": "TracTaskCare = TracTaskCare"
    },
)
