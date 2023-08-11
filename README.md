# ParallelFileConcatenator

## Overview
`ParallelFileConcatenator` is a robust tool designed to efficiently combine data files of various formats (CSV, Feather, Parquet, XLSX, XLS) from a specified directory. It intelligently filters out duplicate files, merges file with matching column headers, and saves the combined data into a compressed Parquet file.


## Features
- **File Hashing:** Efficiently identifies duplicate files through hashing, minimizing redundant processing.
- **Parallel Processing:** Utilizes parallel processing for faster reading and combining large datasets.
- **Flexible Formats:** Supports merging of CSV, Feather, and Parquet file formats.
- **Duplicate Removal:** Filters out duplicate rows within the combined dataframe.
- **Space Saving:** Saves the combined data in compressed Parquet format, conserving storage space.

## Requirements
- Python 3.x
- pandas
- tqdm

## Usage
1. Clone the repository to your local machine.
2. Navigate to the directory containing the Python script.
3. Run the script: python ParallelFileConcatenator.py
4. Follow the prompt to enter the path to the parent folder containing the data files you wish to combine.

## Output
The script will save the combined data as combined_data.parquet (or a custom name) in the same directory. It will also print statistics regarding the total number of files processed, total rows, duplicated files, and the amount of space saved.

## Contributing
Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss the proposed change.

## License
This project is licensed under the MIT License. See the LICENSE.md file for details.

## Contact
For any inquiries, issues, or support, don't hesitate to get in touch with the repository owner.
