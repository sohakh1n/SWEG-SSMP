from setuptools import setup, find_packages

setup(
    name="SWEG-SSMP",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    python_requires='>=3.8',
    author="houmairi",
    description="social media plattform for university project",
    test_suite='tests',
)