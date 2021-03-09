from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rungcc',
    version='0.0.1',
    url='http://jlangvand.no/',
    license='GPLv3',
    author='Joakim Skogø Langvand',
    author_email='jlangvand@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
#    package_dir={"": "src"},
#    packages=find_packages(where="src"),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['pyuv'],
)
