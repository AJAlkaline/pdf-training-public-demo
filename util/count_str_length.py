import json
import argparse
import statistics

def load_json_file(json_file):
    """Loads the JSON data from a file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_text_lengths(json_data):
    """Extracts the lengths of the 'text' field in each object."""
    text_lengths = []
    
    for obj in json_data:
        if 'text' in obj and isinstance(obj['text'], str):
            text_lengths.append(len(obj['text']))
    
    return text_lengths

def calculate_statistics(text_lengths):
    """Calculates and prints the longest, mean, and median text lengths."""
    if not text_lengths:
        print("No 'text' fields found in the provided JSON data.")
        return
    
    longest = max(text_lengths)
    mean = sum(text_lengths) / len(text_lengths)
    median = statistics.median(text_lengths)
    
    print(f"Longest text length: {longest}")
    print(f"Mean text length: {mean:.2f}")
    print(f"Median text length: {median}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process a JSON file to calculate text field statistics.")
    parser.add_argument('--json_file', type=str, required=True, help='Path to the JSON file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load the JSON data
    json_data = load_json_file(args.json_file)
    
    # Extract text lengths
    text_lengths = get_text_lengths(json_data)
    
    # Calculate and print statistics
    calculate_statistics(text_lengths)

if __name__ == "__main__":
    main()
