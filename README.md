# ParallelFileConcatenator

## Overview
`ParallelFileConcatenator` is a robust tool designed to efficiently combine data files of various formats (CSV, Feather, Parquet, XLSX, XLS) from a specified directory. It intelligently filters out duplicate files, merges file with matching column headers, and saves the combined data into a compressed Parquet file.

## Need to Build the Tool

## Features
- **File Hashing:** Efficiently identifies duplicate files through hashing, minimizing redundant processing.
- **Parallel Processing:** Utilizes parallel processing for faster reading and combining large datasets.
- **Flexible Formats:** Supports merging of CSV, Feather, and Parquet file formats.
- **Duplicate Removal:** Filters out duplicate rows within the combined dataframe.
- **Space Saving:** Saves the combined data in very compressed Parquet format, conserving storage space.

## Requirements
- Python 3.x
- pandas
- tqdm
- pyarrow (for reading/writing Feather and Parquet files)


## Usage
1. Clone the repository to your local machine.
3. Navigate to the directory containing the Python script (ParallelFileConcatenator.py).
4. In the project directory, run : pip install -r requirements.txt
5. Run the script: python ParallelFileConcatenator.py
6. Follow the prompt to enter the path to the parent folder containing the data files you wish to combine (e.g., C:\Users\JohnDoe\Documents\Datasets).



## Why This Tool?
In modern data-driven research, collecting and analyzing vast amounts of data is a common but intricate task. This complexity often stems from the fragmented nature of the collected data, spread across different files, formats, and even duplicated across various datasets.

Imagine a scenario where a researcher is scraping online content based on specific keywords. Each keyword generates a distinct dataset, and this process can lead to several challenges:

1. Diverse File Types: Data may be stored in various formats such as CSV, Excel, JSON, etc., each requiring different handling techniques.
2. Duplication of Data: Multiple searches might lead to files with the same type of columns and content, resulting in redundant information and inconsistency.
3. Manual Aggregation: Combining files related to the same search or category manually is labor-intensive, time-consuming, and prone to errors.
4. Consistency and Integrity: Ensuring that the combined dataset maintains its original structure, quality, and integrity is essential for accurate analysis and interpretation.

The purpose of building this tool is to tackle these challenges by streamlining and automating the process of combining fragmented datasets. It aims to efficiently merge files that share the same structure, eliminate redundancy, and create a consistent, unified dataset that is ready for further analysis.



## Output
The script will save the combined data as combined_data.parquet (or a custom name) in the same directory. It will also print statistics regarding the total number of files processed, total rows, duplicated files, and the amount of space saved.

## Contributing
Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss the proposed change.

## License
This project is licensed under the MIT License. See the LICENSE.md file for details.

## Contact
For any inquiries, issues, or support, don't hesitate to get in touch with the repository owner.
