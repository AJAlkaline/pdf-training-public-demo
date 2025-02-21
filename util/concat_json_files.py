import os
import json
import argparse

def concat_json_files(input_dir, output_file):
    # Initialize an empty list to hold all JSON objects
    concatenated_data = []

    # List all files in the input directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"Found {len(files)} JSON files to process.")

    # Process each file
    for json_file in files:
        file_path = os.path.join(input_dir, json_file)
        print(f"Processing {file_path}...")

        # Open the file and load its content
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)  # Load the JSON data
                if isinstance(data, list):
                    concatenated_data.extend(data)  # Extend the list of data
                else:
                    print(f"Warning: {file_path} does not contain a JSON array.")
            except json.JSONDecodeError as e:
                print(f"Error reading {file_path}: {e}")
                continue

        # Write periodically to avoid excessive memory usage
        if len(concatenated_data) > 1000000:  # Example threshold
            with open(output_file, 'a', encoding='utf-8') as out_f:
                json.dump(concatenated_data, out_f, ensure_ascii=False)
                concatenated_data = []  # Clear memory after writing

    # Write remaining data to the output file
    if concatenated_data:
        with open(output_file, 'a', encoding='utf-8') as out_f:
            json.dump(concatenated_data, out_f, ensure_ascii=False)
    
    print(f"Concatenation complete. Data saved to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description='Concatenate JSON files containing arrays of objects.')
    parser.add_argument('--input_dir', type=str, required=True, help='Directory containing the input JSON files.')
    parser.add_argument('--output_file', type=str, required=True, help='Output file to save the concatenated JSON.')

    args = parser.parse_args()

    concat_json_files(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
