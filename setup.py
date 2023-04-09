import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="agenet",
    version="1.0.0",
    author="Chathuranga Basnayaka",
    author_email="chathurangab@sltc.ac.lk , basanayakac8@gmail.com",
    description="Age of Inforamtaion Model for wireless networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cahthuranag/agenet.git",
    packages=["agenet"],
    install_requires=["numpy", "pandas", "tabulate", "matplotlib", "scipy"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ageplot=agenet.plot:plot",
            "ageprint=agenet.printage:printage",
        ],
    },
    extras_require={
        "dev": ["pytest", "pytest-cov", "pytest-console-scripts", "coverage", "codecov"]
    },
)
