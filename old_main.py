import json
import yaml
import re

guangyun = {}
# with open("data/middle_chinese_new.json", 'r', encoding='utf-8') as my_file:
#     guangyun = json.load(my_file)

with open('data/MiddleChinese.yaml', 'r', encoding='utf-8') as my_file:
    guangyun = yaml.safe_load(my_file)

baxter = {}
with open("data/hanzi_api.json", 'r', encoding='utf-8') as my_file:
    baxter = json.load(my_file)

initial_map = {}
with open("data/maps/deprecated/MapFinnicInitials.json", 'r', encoding='utf-8') as my_file:
    initial_map = json.load(my_file)

final_map = {}
with open("data/maps/deprecated/MapFinnicFinals.json", 'r', encoding='utf-8') as my_file:
    final_map = json.load(my_file)

difficult_initials = {}
difficult_finals = {}

impossible_initials = []
impossible_finals = []
VOWELS = ('a', 'i', 'u', 'e', 'o')

def is_vowel(letter: str):
    if letter in VOWELS:
        return True
    return False

def get_initial(fanqie: str):
    initial = fanqie[0]
    alternate_zi = guangyun[initial]["fanqie"][0] if initial in guangyun else None
    if initial in baxter:
        return baxter[initial][0]["initial"]
    elif alternate_zi in baxter:
        return baxter[alternate_zi][0]["initial"]
    else:
        collection_ = f"{initial}"
        for item in guangyun:
            for i in range(len(guangyun[item]["fanqie"])):
                item_fanqie = guangyun[item]["fanqie"][i]
                item_initial = item_fanqie[0]
                if item_initial in collection_:
                    if item in baxter:
                        # difficult_initials[zi] = item
                        # difficult_initials[alternate_zi] = item
                        difficult_initials[initial] = item
                        return baxter[item][0]["initial"]
        # impossible_initials.append(zi)
        return False


def get_final(zi: str, fanqie: str):
    # print(f"Final: {zi}")
    # alternate_zi = guangyun[zi]["fanqie"][1]
    alternate_zi = fanqie[1]
    if zi in baxter:
        return baxter[zi][0]["final"], zi
    elif alternate_zi in baxter:
        return baxter[alternate_zi][0]["final"], alternate_zi
    else:
        collection_ = f"{zi}{alternate_zi}"
        for item in guangyun:
            for fanqie_ in guangyun[item]["fanqie"]:
                item_final = fanqie_[1]
                if item_final in collection_:
                    if item in baxter:
                        difficult_finals[zi] = item
                        difficult_finals[alternate_zi] = item
                        return baxter[item][0]["final"], item
        impossible_finals.append(zi)
        return False, False

def compose_finnic_reading(initial_mc: str, final_mc: str, zi: str = None) -> str:
    initial_fin: str = initial_map[initial_mc]
    final_fin: str = final_map[final_mc]
    def wz():
        if zi:
            print(f"{zi}:{initial_mc}+{final_mc} => {initial_fin}+{final_fin}")
    if not initial_fin:
        # Empty initial.
        if len(final_fin) == 1:
            final_fin *= 2
        # else:
        #     if final_mc[:2] == "jw":
        #         final_fin = "iv" + final_fin[2:]
    if initial_mc == 'y':
        # Initials with glide vowels.
        if re.match("ij\w", final_fin):
            pass
    if initial_mc[0] == 'h':
        if final_mc[0] == 'j':
            initial_fin = 'j'
            # wz()
            if final_mc[:2] == "jw":
                initial_fin = 'v'
                final_fin = final_fin
            elif final_fin[0] in ('j'):
                final_fin = final_fin[1:]
    output = f"{initial_fin}{final_fin}"
    return output

def parse_guangyun(output_dictionary: dict = {}):
    counter_ = 0
    for zi in guangyun:
        print(f"parse_guangyun(): {zi}, {counter_ + 1}", end="")
        for fanqie in guangyun[zi]["fanqie"]:
            initial_sound = get_initial(zi)
            final_sound, final_zi = get_final(zi, fanqie)
            if initial_sound and final_sound:
                tone = baxter[final_zi][0]["tone"]
                finnic_sound = compose_finnic_reading(initial_sound, final_sound, zi)
                new_fanqie = f"{fanqie}: {initial_sound}{final_sound}"
                new_fanqie = {fanqie: f"{initial_sound}{final_sound}"}
                entry = {
                    "Proto-Finnic": finnic_sound,
                    "Middle-Chinese": f"{initial_sound}{final_sound}",
                    "initial": f"{initial_sound}",
                    "final": f"{final_sound}",
                    "tone": tone,
                    "fanqie": [new_fanqie]
                }
                # print(counter_, zi, entry)
                if zi not in output_dictionary:
                    output_dictionary[zi] = [entry]
                else:
                    pre_existed: bool = False
                    for item in output_dictionary[zi]:
                        if item["Middle-Chinese"] == entry["Middle-Chinese"]:
                            # item["fanqie"].append(entry["fanqie"][0])
                            item["fanqie"].append(new_fanqie)   # Only include new entry for the fanqie
                            pre_existed = True
                    if not pre_existed:
                        output_dictionary[zi].append(entry) # Include a new entry for the whole zi itself.
                print(f", Success.")
            else:
                print(f", Failed.")
        counter_ += 1
    print(f"Retrieved {len(output_dictionary)} characters from Guangyun.")
    return output_dictionary

def parse_baxter(output_dictionary: dict = {}):
    counter_: int = 1
    for zi in baxter:
        if zi not in output_dictionary:
            initial_sound = baxter[zi][0]["initial"]
            final_sound = baxter[zi][0]["final"]
            finnic_sound = compose_finnic_reading(initial_sound, final_sound, zi)
            tone = baxter[zi][0]["tone"]
            output_dictionary[zi] = {
                "Proto-Finnic": finnic_sound,
                "Middle-Chinese": f"{initial_sound}{final_sound}",
                "initial": f"{initial_sound}",
                "final": f"{final_sound}",
                "tone": tone
            }
            counter_ += 1
    print(f"Added {counter_} characters from Baxter-Sagart.")
    return output_dictionary


if __name__ == '__main__':
    output_dictionary = {}
    # output_dictionary = parse_baxter(output_dictionary)
    output_dictionary = parse_guangyun(output_dictionary)
    print(f"Gathered {len(output_dictionary)} characters in total.")
    # print(f"Impossible initials ({len(impossible_initials)}):\n{impossible_initials}")
    # print(f"Impossible finals ({len(impossible_finals)}):\n{impossible_finals}")

    with open('product/FailedInitials.txt', 'w', encoding='utf-8') as f:
        f.write(f"# Impossible initials ({len(impossible_initials)})\n")
        f.write(str(impossible_initials))

    with open('product/FailedFinals.txt', 'w', encoding='utf-8') as f:
        f.write(f"# Impossible finals ({len(impossible_finals)})\n")
        f.write(str(impossible_finals))

    with open('product/FinnicKanji.json', 'w', encoding='utf-8') as f:
        json.dump(output_dictionary, f, ensure_ascii=False, indent=4)

    with open('product/FinnicKanji.yaml', 'w', encoding='utf-8') as f:
        mc_yaml = yaml.dump(output_dictionary, f, sort_keys=False, default_flow_style=False, allow_unicode=True)