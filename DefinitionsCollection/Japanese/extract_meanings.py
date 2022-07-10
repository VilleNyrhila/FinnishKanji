import yaml


if __name__ == '__main__':
    with open("KanjiDict2.yaml", 'r', encoding='utf-8') as my_file:
        kanji_dict_2 = yaml.safe_load(my_file)

    for entry in kanji_dict_2:
        if entry == "character":
            # Only character entries.
            for item in entry:
                pass
            #character:
            #- literal: 亜

            meaning = entry["reading_meaning"]["meaning"]

