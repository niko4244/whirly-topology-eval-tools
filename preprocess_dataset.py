import argparse
import json
import pandas as pd

def preprocess(input_file, output_file):
    # Example: normalize and clean topology dataset
    with open(input_file, 'r') as f:
        data = json.load(f)
    # Convert to DataFrame for cleaning
    df = pd.json_normalize(data, sep='_')
    df = df.drop_duplicates()
    processed = df.to_dict(orient='records')
    with open(output_file, 'w') as f:
        json.dump(processed, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess a raw topology dataset.")
    parser.add_argument('--input', type=str, required=True, help="Input raw dataset JSON file")
    parser.add_argument('--output', type=str, required=True, help="Output processed dataset JSON file")
    args = parser.parse_args()

    preprocess(args.input, args.output)