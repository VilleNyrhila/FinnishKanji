import yaml
import json
import time

def read_a_data_file(target_variable, file_name: str, yaml_counter: int, json_counter: int):
    start = time.perf_counter()
    with open(file_name, 'r', encoding='utf-8') as my_file:
        print(f"\tReading '{my_file.name}'.")
        if ".yaml" in my_file.name:
            target_variable = yaml.safe_load(my_file)
            yaml_counter += 1
        elif ".json" in my_file.name:
            target_variable = json.load(my_file)
            json_counter += 1
        end = time.perf_counter()
        print(f"\tRead '{my_file.name}' in {end - start:0.4f} seconds. Got {len(target_variable)} items.")
        return target_variable, yaml_counter, json_counter
