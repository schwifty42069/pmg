import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piptv_pmg",
    version="0.0.2",
    author="Brett Hufnagle",
    author_email="teachingchain0420@gmail.com",
    description="Piptv M3U Generator - An M3U IPTV playlist generator using piptvs scraping logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schwifty42069/pmg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
