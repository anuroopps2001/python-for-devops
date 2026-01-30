import json
import os
from pathlib import Path
import sys

source_file_path = "golden_content.json"  # for testing give, kept files in script path
live_configuration_file = "live_config.json"
#check whether the file exists or not in the specified path
p = Path(source_file_path)

if p.is_file():
    print(f"The file {source_file_path} is an existing file")
else:
    print(f"The file {source_file_path} is not an existing file or doesn;t exists")

# if p.exists(): # we can also use exists method to confirm whether 

# read and load the file content with json.load() method

with open(source_file_path, "r") as source:
    golden_data = json.load(source)  # the json.load() function converts a JSON file directly into a Dictionary

with open(live_configuration_file, "r") as live:
    live_data = json.load(live)  # the json.load() function converts a JSON file directly into a Dictionary


print("Data loaded successfully!")


drif_count = 0

# check for missing keys
missing_keys = set(live_data.keys() - golden_data.keys())

for key in missing_keys:
    print(f"ABSENT: {key} is missing from live config")
    drif_count = drif_count + 1

# check for value mismatch
common_keys = set(golden_data.keys() & live_data.keys())

for key in common_keys:
    if golden_data[key] != live_data[key]:
        print(f"DRIFT at key: {key} (Expected: {golden_data[key]}, Actual: {live_data[key]})")
        drif_count + drif_count + 1

print("\n" + "="*30)

if drif_count == 0:
    print(f"SUCCESS: No Drift Detected and environment is clean")
    sys.exit(0)
else:
    print(f"Failure: found {drif_count} instances of drift.!")
    sys.exit(1)