import json
import sys


def aggregate_data(file_paths):
    aggregated_data = {}

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            json_content = json.load(file)

        if isinstance(json_content, dict):
            aggregated_data.update(json_content)

    return aggregated_data


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py file1.json file2.json ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    aggregated_data_result = aggregate_data(file_paths)
    print(json.dumps(aggregated_data_result, indent=4))


if __name__ == "__main__":
    main()
