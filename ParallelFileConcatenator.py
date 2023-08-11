import os
import pandas as pd
import hashlib
import logging
from tqdm import tqdm
from multiprocessing import cpu_count, Pool

def get_file_hash(file_path):
    hash_obj = hashlib.md5()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

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

def combine_files(folder_path, output_file_name='combined_data.parquet', file_types=['.csv', '.feather', '.parquet', 'xlsx', 'xls' , '.json', '.pickle', '.hdf']):
    logging.info("Combining files in the folder " + folder_path)

    stats = {
        'total_files': 0,
        'total_rows': 0,
        'duplicated_files': 0,
        'duplicated_rows': 0, # Initialize duplicated_rows counter
        'saved_MB': 0
    }
    files_processed = set()
    original_size_bytes = 0
    total_files = sum([len(files) for root, _, files in os.walk(folder_path)])
    pbar = tqdm(total=total_files, desc="Processing Files")

    pool = Pool(cpu_count())
    process_args = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            original_size_bytes += os.path.getsize(file_path)
            process_args.append((file_path, file_name, file_types, None))

    results = pool.map(process_file, process_args)
    pbar.close()

    data_frames = []
    for result in results:
        if result is not None:
            file_name, file_size, file_extension, file_hash, df, duplicate_rows = result
            if (file_name, file_size, file_extension, file_hash) not in files_processed:
                files_processed.add((file_name, file_size, file_extension, file_hash))
                stats['total_files'] += 1
                stats['total_rows'] += len(df)
                stats['duplicated_rows'] += duplicate_rows # Accumulate duplicated_rows
                data_frames.append(df)
            else:
                stats['duplicated_files'] += 1

    combined_df = pd.concat(data_frames, ignore_index=True)
    combined_df.drop_duplicates(inplace=True)
    combined_file_path = os.path.join(folder_path, output_file_name)
    combined_df.to_parquet(combined_file_path, compression='gzip')
    combined_file_size_bytes = os.path.getsize(combined_file_path)
    stats['saved_MB'] = (original_size_bytes - combined_file_size_bytes) / (1024 ** 2)

    return stats

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    folder_path = input("Please enter the path to the parent folder: ")
    stats = combine_files(folder_path)
    for key, value in stats.items():
        logging.info(f'{key}: {value}')
