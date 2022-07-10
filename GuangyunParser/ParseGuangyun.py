import xmltodict
import json
import yaml

guangyun: dict = {}
with open("Guangyun.xml", "rb") as file:
    # xml_content = file.read()
    # guangyun = xmltodict.parse(xml_content)
    guangyun = xmltodict.parse(file, dict_constructor=dict, encoding='utf-8')
    # print(guangyun)

with open("Guangyun.yaml", 'w', encoding='utf-8') as file:
    guangyun_yaml = yaml.dump(guangyun, file, sort_keys=False, default_flow_style=False, allow_unicode=True)

dict_to_json = {}

for volume in guangyun["book"]["volume"]:
    print("Start of a volume.")
    ipa_voice: str = ""
    for rhyme in volume['rhyme']:
        # print(line2)
        # print("   Start of a rhyme in volume.")
        for voice_part in rhyme['voice_part']:
            # print("      Start of a voice part", len(voice_part))
            print(f"Voice part: {voice_part}")
            ipa_voice = voice_part["@ipa"]
            for word_head in voice_part["word_head"]:
                # print("         Word head:", word_head, len(word_head))
                if type(word_head) == dict:
                    if '#text' in word_head:
                        zi = word_head['#text']
                    elif 'original_word' in word_head:
                        zi = word_head['original_word']['#text']
                    if "note" in word_head and word_head["note"] is not None:
                        if "fanqie" in word_head["note"]:
                            fanqie = word_head["note"]["fanqie"]
                            if type(fanqie) != str:
                                # print("\tFanqie:", fanqie)
                                if 'original_text' in fanqie:
                                    print(f"Original text, {zi} fanqie: {fanqie}")
                                    original_text = fanqie['original_text']["rewrite_text"]
                                    other_text = fanqie['#text']
                                    # fanqie = f"{original_text['rewrite_text']}{other_text}"
                                    fanqie = f"{original_text}{other_text}"
                                    print(f"Original text, {zi} fanqie: {fanqie}")
                                    # print("\toriginal_text: Fanqie:", fanqie)
                                elif 'added_text' in fanqie:
                                    print(f"Added text, {zi} fanqie: {fanqie}")
                                    added_text = fanqie['added_text']
                                    other_text = fanqie['#text']
                                    fanqie = f"{added_text}{other_text}"
                                    print(f"Added text, {zi} fanqie: {fanqie}")
                                # print(fanqie)
                        # print(f"         {zi}")
                        if zi not in dict_to_json:
                            dict_to_json[zi] = {
                                "fanqie": [fanqie],
                                "IPA": [ipa_voice]
                            }
                        else:
                            dict_to_json[zi]["fanqie"].append(fanqie)
                            dict_to_json[zi]["IPA"].append(ipa_voice)
                    # print("         Word head:", word_head)
            pass
    print()

# with open('middle_chinese.json', 'w', encoding='utf-8') as f:
#     pass    # Clear contents
with open('middle_chinese.json', 'w', encoding='utf-8') as f:
    json.dump(dict_to_json, f, ensure_ascii=False, indent=4)

with open("MiddleChinese.yaml", 'w', encoding='utf-8') as file:
    mc_yaml = yaml.dump(dict_to_json, file, sort_keys=False, default_flow_style=False, allow_unicode=True)