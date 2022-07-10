# import json
import yaml

if __name__ == '__main__':
    shinjitai_map = {}
    with open("data/raw/ShinjitaiRaw.txt", 'r', encoding='utf-8') as my_file:
        for line in my_file:
            line = line.strip()
            if line[0] == '#':
                continue
            pieces: list = line.split()
            shinjitai: str = pieces[0].strip()
            kyuujitai: str= pieces[1].strip()
            shinjitai_map[shinjitai] = kyuujitai

    # with open("product/ShinjitaiMap.json", 'w', encoding='utf-8') as map_file:
    #     json.dump(shinjitai_map, map_file, ensure_ascii=False, indent=4)

    with open('product/ShinjitaiMap.yaml', 'w', encoding='utf-8') as f:
        print(f"Writing to file '{f.name}'.")
        f.write(f"# Includes {len(shinjitai_map)} characters.\n")
        f.write("# Based on web page written by Dylan W.H. Sung 2003\n"
                "# From: https://web.archive.org/web/20081218203648/http://www.sungwh.freeserve.co.uk/hanzi/j-s.htm\n"
                "# Left is shinjitai, right is kyuujitai.\n")
        mc_yaml = yaml.dump(shinjitai_map, f, sort_keys=False, default_flow_style=False, allow_unicode=True)