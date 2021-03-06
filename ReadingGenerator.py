import configparser
import os
import time

from utils.fileUtils import read_a_data_file

CONFIG = configparser.ConfigParser(allow_no_value=True)
CONFIG.read('reading.cfg')


IGNORED_FALSE_CHARACTERS = ('，')
INCLUDE_MC_LINE: bool = True
INCLUDE_FINNISH_LINE: bool = True
INCLUDE_LATE_LOAN: bool = True

finnic_guangyun = {}
shinjitai_map = {}
simples_map = {}
manual_map = {}

def read_data_files():
    global finnic_guangyun, shinjitai_map, simples_map, manual_map
    yaml_counter: int = 0
    json_counter: int = 0
    print("Reading source data files.")
    read_data_start = time.perf_counter()
    finnic_guangyun, yaml_counter, json_counter = read_a_data_file(finnic_guangyun, "product/FinnicKanji.yaml",
                                                                   yaml_counter, json_counter)
    shinjitai_map, yaml_counter, json_counter = read_a_data_file(shinjitai_map, "data/maps/ShinjitaiMap.yaml",
                                                                 yaml_counter, json_counter)
    simples_map, yaml_counter, json_counter = read_a_data_file(simples_map, "data/maps/SimplifiedChineseMap.yaml",
                                                               yaml_counter, json_counter)
    manual_map, yaml_counter, json_counter = read_a_data_file(manual_map, "data/maps/ManualMap.yaml",
                                                              yaml_counter, json_counter)
    read_data_end = time.perf_counter()
    print(f"Read source files in {read_data_end - read_data_start:0.4f} seconds.")

def save_unresolved_character(zi: str):
    if zi not in IGNORED_FALSE_CHARACTERS:
        with open("error/unresolved_characters.txt", 'a', encoding='utf-8') as my_file:
            my_file.write(f"{zi}\n")

def get_finnish_zi_readings(zi: str):
    readings: str = ""
    done_readings: list = []
    for item in finnic_guangyun[zi]["pronunciations"]["early-loan"]:
        reading_ = item['Finnish']
        if reading_ not in done_readings:
            readings += f"{reading_}/"
            done_readings.append(reading_)
    readings = readings[:-1]
    return readings

def get_finnic_zi_readings(zi: str):
    readings: str = ""
    done_readings: list = []
    for item in finnic_guangyun[zi]["pronunciations"]["early-loan"]:
        reading_ = item['Proto-Finnic']
        if reading_ not in done_readings:
            readings += f"{reading_}/"
            done_readings.append(reading_)
    readings = readings[:-1]
    return readings

def get_late_loan_readings(zi: str):
    readings: str = ""
    done_readings: list = []
    for item in finnic_guangyun[zi]["pronunciations"]["late-loan"]:
        reading_ = item['Early-Finnish']
        if reading_ not in done_readings:
            readings += f"{reading_}/"
            done_readings.append(reading_)
    readings = readings[:-1]
    return readings

def get_mc_entry_readings(proper_zi: str):
    readings: str = ""
    for item in finnic_guangyun[proper_zi]["pronunciations"]["Middle-Chinese"]:
        reading_ = item["reading"]
        if reading_ not in readings:
            readings += f"{reading_}/"
    readings = readings[:-1]
    return readings

def generate_reading(line: str) -> str:
    def get_from_shinjitai(zi_: str):
        proper_zi = shinjitai_map[zi_]
        if len(proper_zi) > 1:
            proper_zi = proper_zi[0]
        return proper_zi

    def get_from_simplified_map(zi_: str):
        for item in simples_map[zi_]:
            if item in finnic_guangyun:
                return item  # <-- proper_zi
        return item

    def get_manual_map(zi_: str):
        proper_zi = manual_map[zi_]
        return proper_zi
    zi_line: str = ""
    finnish_line: str = ""
    north_finnic_line: str = ""
    derived_finnic_line: str = ""
    mc_line: str = ""
    for zi in line:
        reading_fi = '?'
        middle_chinese_reading = ""
        finnish_reading = ""
        north_finnic_reading = ""
        derived_finnish = ""
        proper_zi: str = zi
        if proper_zi not in finnic_guangyun:
            if proper_zi in shinjitai_map:
                proper_zi = get_from_shinjitai(zi)
            elif proper_zi in simples_map:
                proper_zi = get_from_simplified_map(zi)
            if proper_zi not in finnic_guangyun:
                # If STILL not found in the data, look for it in the manual additions.
                if proper_zi in manual_map:
                    proper_zi = get_manual_map(proper_zi)
                else:
                    save_unresolved_character(zi)
        if proper_zi in finnic_guangyun:
            north_finnic_reading = get_finnic_zi_readings(proper_zi)
            middle_chinese_reading = ""
            derived_finnish = ""
            finnish_reading = ""
            if INCLUDE_MC_LINE:
                middle_chinese_reading = get_mc_entry_readings(proper_zi)
            if INCLUDE_FINNISH_LINE:
                derived_finnish = get_finnish_zi_readings(proper_zi)
            if INCLUDE_LATE_LOAN:
                finnish_reading = get_late_loan_readings(proper_zi)
        zi_line += zi

        north_finnic_line += f"{north_finnic_reading} "
        mc_line += f"{middle_chinese_reading} "
        derived_finnic_line += f"{derived_finnish} "

        finnish_line += f"{finnish_reading} "
    derived_finnic_line = derived_finnic_line.strip()
    output = ""
    output += f"\n{mc_line.strip()}\t# Middle Chinese reading." if INCLUDE_MC_LINE else ""
    output += f"\n{north_finnic_line}\t# North Finnic reading."
    output += f"\n{derived_finnic_line.strip()}\t# Finnish reading, early borrowing." if INCLUDE_FINNISH_LINE else ""
    output += f"\n{finnish_line.strip()}\t# Finnish reading, late borrowing." if INCLUDE_LATE_LOAN else ""
    output += "\n"
    return output

def compose_to_file(source_file_name: str):
    output = ""
    with open(f"ReaderFiles/Input/{source_file_name}", 'r', encoding='utf-8') as reading_file:
        print(f"\tReading file '{reading_file.name}'.")
        for line in reading_file:
            line = line.strip()
            if line:
                if line[0] == ';':
                    header_line = f"\n[{line[1:].strip()}]:"
                    output += header_line + "\n"
                elif line[0] != '#':
                    meat: str = ""
                    comment: str = ""
                    for i in range(len(line)):
                        if line[i] == '#':
                            comment = line[i:]
                            break
                        meat += line[i]
                    meat = meat.strip()
                    read_line = generate_reading(meat)
                    def ac(x: str): return f"\t\t{x}" if x else ""
                    output += f"{meat}{ac(comment)}{read_line}\n"
    output_file_name = f"{source_file_name.split('.')[0]}Output.txt"
    with open(f"ReaderFiles/Output/{output_file_name}", 'w', encoding='utf-8') as writing_file:
        writing_file.write(output.lstrip())
        print(f"\tWrote to file '{writing_file.name}'.")

if __name__ == '__main__':
    read_data_files()
    print(f"Start compiling finnic readings.")
    finnic_readings_start = time.perf_counter()
    counter: int = 0
    if CONFIG.getboolean("READ OPTIONS", "allFiles"):
        for root, dirs, files in os.walk("ReaderFiles/Input"):
            for source_file_name in files:
                compose_to_file(source_file_name)
                counter += 1
    else:
        for source_file_name, _ in CONFIG.items('SOURCE FILES'):
            if source_file_name not in CONFIG['DEFAULT']:
                compose_to_file(source_file_name)
                counter += 1
    print(f"Compiled {counter} files in {time.perf_counter() - finnic_readings_start:0.4f} seconds.")