import yaml
import re
# import json

if __name__ == '__main__':
    simplified_map = {}
    with open("data/raw/SimplifiedChineseRaw.txt", 'r', encoding='utf-8') as my_file:
        for i, line in enumerate(my_file):
            line = line.strip()
            if line:
                if line[0] == '#':
                    # print("Skipped line:", line)
                    continue
                if re.match("([a-z])", line[0]):
                    # Block for a sound starts here.
                    continue
                if re.match("([0-9])", line[0]):
                    # A number always follows a classical entry.
                    pass
                pieces: list = line.split('⇒')
                print(pieces)
                simplified_zi: str = pieces[0].strip()
                traditionals: list = pieces[1:]
                entry = []
                for trad_zi in traditionals:
                    trad_zi = trad_zi.strip()
                    entry.append(trad_zi)
                simplified_map[simplified_zi] = entry

    # with open("product/SimplifiedChineseMap.json", 'w', encoding='utf-8') as map_file:
    #     json.dump(simplified_map, map_file, ensure_ascii=False, indent=4)

    with open('product/SimplifiedChineseMap.yaml', 'w', encoding='utf-8') as f:
        print(f"Writing to file '{f.name}'.")
        f.write(f"# Includes {len(simplified_map)} characters.\n")
        f.write("# Based on web page by SayJack.com 2018\n"
                "# From: https://www.sayjack.com/chinese/simplified-to-traditional-chinese-conversion-table/\n"
                "# Left is simplified, right is traditional.\n")
        mc_yaml = yaml.dump(simplified_map, f, sort_keys=False, default_flow_style=False, allow_unicode=True)