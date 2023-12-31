# Author: https://github.com/Kaleemullahqasim
# Date: 2021-03-01
# Version: 0.2

import os
import pandas as pd
import hashlib
import logging
from tqdm import tqdm
from multiprocessing import cpu_count, Pool
from prettytable import PrettyTable
import shutil
import re
from tqdm import tqdm

# Function to print the summary statistics of the file processing
def print_summary(stats):
    terminal_width = shutil.get_terminal_size().columns

    table = PrettyTable()
    table.field_names = ["Metric", "Value"]
    table.add_row(["total_files", stats['total_files']])
    table.add_row(["total_rows", stats['total_rows']])
    table.add_row(["duplicated_files", stats['duplicated_files']])
    table.add_row(["duplicated_rows", stats['duplicated_rows']])
    table.add_row(["saved_MB", stats['saved_MB']])
    
    colored_table = table.get_string()
    plain_table = re.sub(r'\x1b\[\d+;\d+m', '', colored_table)
    table_width = max(len(line) for line in plain_table.split('\n'))
    padding = (terminal_width - table_width) // 2

    # Center the title based on the table width, then add padding
    print("\n")
    title = "Summary of File Processing:".center(table_width)
    title = " " * padding + title

    print(title)
    for line in colored_table.split('\n'):
        print(" " * padding + line)
    print("\n")




# Function to compute the MD5 hash of a file
def get_file_hash(file_path):
    hash_obj = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

# Function to process a single file and check for duplicates
def process_file(args):
    file_path, file_name, file_types, expected_columns = args
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_name)[1]
    if file_extension in file_types:
        file_hash = get_file_hash(file_path)
        try:
            if file_extension == '.csv':
                df = pd.read_csv(file_path, engine='python')
            elif file_extension == '.feather':
                df = pd.read_feather(file_path)
            elif file_extension == '.parquet':
                df = pd.read_parquet(file_path)
            elif file_extension == '.xlsx' or file_extension == '.xls':
                df = pd.read_excel(file_path)
            elif file_extension == '.json':
                df = pd.read_json(file_path)
            elif file_extension == '.pickle':
                df = pd.read_pickle(file_path)
            elif file_extension == '.hdf':
                df = pd.read_hdf(file_path)
            else:
                logging.info(f"Skipping {file_path} due to unsupported file type.")
                return None

            duplicate_rows = df.duplicated().sum()
            return file_name, file_size, file_extension, file_hash, df, duplicate_rows
        except Exception as e:
            logging.error(f"Error reading {file_path}: {str(e)}")
    return None



# Combine files from a given directory and check for duplicates
def combine_files(folder_path, output_file_name='combined_data.parquet', file_types=['.csv', '.feather', '.parquet', 'xlsx', 'xls', '.json', '.pickle', '.hdf']):
    logging.info("\033[1;34mCombining files in the folder " + folder_path + "\033[0m")

    stats = {
        'total_files': 0,
        'total_rows': 0,
        'duplicated_files': 0,
        'duplicated_rows': 0,
        'saved_MB': 0
    }
    files_processed = set()
    original_size_bytes = 0
    total_files = sum([len(files) for root, _, files in os.walk(folder_path)])
    
    pool = Pool(cpu_count())
    process_args = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            original_size_bytes += os.path.getsize(file_path)
            process_args.append((file_path, file_name, file_types, None))

    data_frames = []
    with tqdm(total=total_files, desc="Processing Files") as pbar:
        for result in pool.imap(process_file, process_args):  # Use imap instead of map
            if result is not None:
                file_name, file_size, file_extension, file_hash, df, duplicate_rows = result
                if (file_name, file_size, file_extension, file_hash) not in files_processed:
                    files_processed.add((file_name, file_size, file_extension, file_hash))
                    stats['total_files'] += 1
                    stats['total_rows'] += len(df)
                    stats['duplicated_rows'] += duplicate_rows
                    data_frames.append(df)
                else:
                    stats['duplicated_files'] += 1
            pbar.update(1)  # Update the progress bar after processing each file

        # Additional progress bar for final steps
        with tqdm(total=4, desc="Finalizing") as pbar_final:
            combined_df = pd.concat(data_frames, ignore_index=True)
            pbar_final.update(1)
            combined_df.drop_duplicates(inplace=True)
            pbar_final.update(1)
            combined_file_path = os.path.join(folder_path, output_file_name)
            combined_df.to_parquet(combined_file_path, compression='gzip')
            pbar_final.update(1)
            combined_file_size_bytes = os.path.getsize(combined_file_path)
            stats['saved_MB'] = (original_size_bytes - combined_file_size_bytes) / (1024 ** 2)
            pbar_final.update(1)

    return stats




if __name__ == "__main__":
    print("\033[1;31m" + r"""
      _____                _ _      _ ______ _ _       _____                      _                   _             
     |  __ \              | | |    | |  ____(_) |     / ____|                    | |                 | |            
     | |__) |_ _ _ __ __ _| | | ___| | |__   _| | ___| |     ___  _ __   ___ __ _| |_ ___ _ __   __ _| |_ ___  _ __ 
     |  ___/ _` | '__/ _` | | |/ _ \ |  __| | | |/ _ \ |    / _ \| '_ \ / __/ _` | __/ _ \ '_ \ / _` | __/ _ \| '__|
     | |  | (_| | | | (_| | | |  __/ | |    | | |  __/ |___| (_) | | | | (_| (_| | ||  __/ | | | (_| | || (_) | |   
     |_|   \__,_|_|  \__,_|_|_|\___|_|_|    |_|_|\___|\_____\___/|_| |_|\___\__,_|\__\___|_| |_|\__,_|\__\___/|_|   
                                                                            
                                                                            By:https://github.com/Kaleemullahqasim                                                                                         
                                                                                                                
    """ + "\033[0m")

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    folder_path = input("Please enter the path to the parent folder: ")
    stats = combine_files(folder_path)

    print_summary(stats)

    
