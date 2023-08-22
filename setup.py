from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()


setup(
    name='ParallelFileConcatenator',
    version='0.1',
    description='ParallelFileConcatenator is a robust tool designed to efficiently combine data files of various formats (CSV, Feather, Parquet, XLSX, XLS) from a specified directory.',
    author='Kaleem Ullah Qasim',
    author_email='kaleem.qasim@gmail.com',
    keywords = ["parallel file concatenation",
                "data aggregation",
                "data merging",
                "data cleaning",
                "data deduplication",
                "data compression",
                "file management",
                "file processing",
                "data analysis",
                "data science",
                "machine learning",
                "big data",
                "data engineering",
                "data wrangling",
                "data preparation"],
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'

)

