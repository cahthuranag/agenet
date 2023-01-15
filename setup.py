import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "agewire",
    version = "1.0.0" ,
    author = "Chathuranga Basnayaka",
    author_email = "chathurangab@sltc.ac.lk , basanayakac8@gmail.com",
    description = "Age of Inforamtaion Model for wireless networks",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "https://github.com/cahthuranag/agewire.git",
    packages = ['agewire'],
    install_requires = ['numpy', 'pandas', 'tabulate', 'matplotlib' , 'scipy','argparse'],
    python_requires = '>=3.8',
    entry_points = {
        'console_scripts': ['agecal=agewire.maincom:printval','ageplot=agewire.maincom:ageplot','ageprintex=agewire.av_age:printageex','ageplotex=agewire.av_age:plotageex'],
    },
    extras_require = {
        'dev' : [
            'pytest',
            'pytest-cov',
            'pytest-console-scripts',
            'coverage',
            'codecov'
        ]
    }
)