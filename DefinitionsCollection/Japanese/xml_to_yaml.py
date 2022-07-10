import xmltodict
import yaml

if __name__ == '__main__':
    with open("kanjidic2.xml", "rb") as file:
        kanji_dict = xmltodict.parse(file, dict_constructor=dict, encoding='utf-8')

    with open("KanjiDict2.yaml", 'w', encoding='utf-8') as file:
        mc_yaml = yaml.dump(kanji_dict, file, sort_keys=False, default_flow_style=False, allow_unicode=True)
