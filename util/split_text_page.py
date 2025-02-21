import os
import json
import argparse

def split_text_into_chunks(text, max_length=2300):
    """Split text into chunks with a maximum length, ending at a newline or the end of the file."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end >= len(text):
            chunks.append(text[start:])
            break
        else:
            # Find the last newline before the end of the current chunk
            last_newline = text.rfind('\n', start, end)
            if last_newline == -1:  # If no newline is found, split at max_length
                chunks.append(text[start:end])
                start = end
            else:  # Split at the newline
                chunks.append(text[start:last_newline + 1])
                start = last_newline + 1
    return chunks

def process_file(file_path, output_dir):
    """Process a single .txt file and save the resulting JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chunks of at most 2300 characters
    chunks = split_text_into_chunks(text)

    # Get the base name of the file without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create an array of JSON objects
    json_data = []
    for page_number, chunk in enumerate(chunks, start=1):
        json_data.append({
            "text": chunk,
            "page": f"{base_name}-page{page_number}"
        })

    # Create a .json file with the same name as the .txt file
    output_file_name = base_name + '.json'
    output_path = os.path.join(output_dir, output_file_name)
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def process_directory(input_dir, output_dir):
    """Process all .txt files in the given directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_dir, file_name)
            process_file(file_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split .txt files into JSON chunks of max 2300 characters.")
    parser.add_argument('--input_dir', required=True, help="Directory containing .txt files to process.")
    parser.add_argument('--output_dir', required=True, help="Directory to save the resulting .json files.")

    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output_dir)
