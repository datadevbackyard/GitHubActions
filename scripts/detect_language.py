import os
import pandas as pd
from lingua import Language, LanguageDetectorBuilder

# Directories for input data
INPUT_DIR = "input_data"

def process_csv_files(input_dir):
    # Define the languages to detect
    languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()

    # Process each file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):  # Check for CSV files
            input_file_path = os.path.join(input_dir, file_name)

            print(f"Processing file: {file_name}")

            # Load the CSV file
            try:
                df = pd.read_csv(input_file_path)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

            # Skip files without 'text' column or those that already have 'detected_language'
            if 'text' not in df.columns:
                print(f"Skipping {file_name}: No 'text' column found.")
                continue
            if 'detected_language' in df.columns:
                print(f"Skipping {file_name}: 'detected_language' column already exists.")
                continue

            # Detect languages for each text
            try:
                df['detected_language'] = df['text'].apply(
                    lambda x: detector.detect_language_of(x).iso_code_639_1.name if isinstance(x, str) else None
                )

                # Print out the detected languages
                for index, row in df.iterrows():
                    print(f"Text: {row['text']} - Detected Language: {row['detected_language']}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                continue

if __name__ == "__main__":
    process_csv_files(INPUT_DIR)
