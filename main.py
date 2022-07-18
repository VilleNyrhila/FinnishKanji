import yaml
import json
import re
import time

from utils.fileUtils import read_a_data_file

PALATALS_AFFRICATES = ("tsy", "tsyh", "dzy", )
ROUND_VOWELS = ('u', 'o', 'y', 'ü', 'ö')
# Conf
BAXTER_SUPERSEDE: bool = True

guangyun = {}
baxter = {}
initial_map = {}
final_map = {}
main_vowel_map = {}
coda_map = {}
definitions = {}
finnic_initials = {}
finnish_initials = {}
finnic_finals = {}

def read_data_files():
    global guangyun, baxter, initial_map, final_map, main_vowel_map, coda_map, definitions,\
        finnic_initials, finnic_finals, finnish_initials
    yaml_counter: int = 0
    json_counter: int = 0
    print("Reading source data files.")
    read_yaml_start = time.perf_counter()
    guangyun, yaml_counter, json_counter = read_a_data_file(guangyun, 'data/MiddleChinese.yaml',
                                                            yaml_counter, json_counter)
    baxter, yaml_counter, json_counter = read_a_data_file(baxter, 'data/BaxterSagartData.yaml',
                                                          yaml_counter, json_counter)
    initial_map, yaml_counter, json_counter = read_a_data_file(initial_map, 'data/maps/InitialMapPlus.yaml',
                                                               yaml_counter, json_counter)
    final_map, yaml_counter, json_counter = read_a_data_file(final_map, 'data/maps/FinalMapPlus.yaml',
                                                             yaml_counter, json_counter)
    main_vowel_map, yaml_counter, json_counter = read_a_data_file(main_vowel_map, "data/maps/MainVowelMap.yaml",
                                                                  yaml_counter, json_counter)
    coda_map, yaml_counter, json_counter = read_a_data_file(coda_map, "data/maps/CodaMap.yaml",
                                                            yaml_counter, json_counter)
    definitions, yaml_counter, json_counter = read_a_data_file(definitions,
                                   "DefinitionsCollection/Chinese/CompleteRuns/DefinitionsFinnishFullPlus.yaml",
                                                               yaml_counter, json_counter)
    read_yaml_stop = time.perf_counter()
    read_json_start = time.perf_counter()
    finnic_initials, yaml_counter, json_counter = read_a_data_file(finnic_initials, "data/maps/MapFinnicInitials.yaml",
                                                                   yaml_counter, json_counter)
    finnish_initials, yaml_counter, json_counter = read_a_data_file(finnic_initials,
                                                                    "data/maps/MapFinnishInitials.yaml",
                                                                    yaml_counter, json_counter)
    finnic_finals, yaml_counter, json_counter = read_a_data_file(finnic_finals,
                                                                 "data/maps/deprecated/MapFinnicFinals.json",
                                                                 yaml_counter, json_counter)
    read_json_stop = time.perf_counter()
    print(f"Read {yaml_counter} YAML files in {read_yaml_stop - read_yaml_start:0.4f} seconds and "
          f"{json_counter} JSON files in {read_json_stop - read_json_start:0.4f} seconds.")



def construct_north_finnic_pronunciation(mc_initial: str, mc_final:str,
                                         fc_final: str, medial: str, main_vowel_fc: str, coda: str):
    """Construct a loaned pronunciation from Early Middle Chinese to North Finnic."""
    fc_initial = finnic_initials[mc_initial]
    # Potential medials include: '', 'j', 'w', 'jw', 'ji', 'jwi'
    if 'y' in mc_initial:
        # Palatalization in the initial.
        if mc_initial == 'y' or mc_initial in PALATALS_AFFRICATES:
            if medial and medial[0] == 'j':
                medial = medial[1:] # Remove palatalization from final, if it's already found in the initial.
        elif 'j' not in medial:
            # Palatalization in the initial, but not in the medial.
            medial = 'j' + medial   # Move the palatalization around.
    if not fc_initial or fc_initial == "h" and medial:
        if "w" in medial:
            fc_initial = 'v'
        elif "j" in medial:
            fc_initial = 'j'  # 'Y' in "Zhang Fei Yide"
        if not fc_initial and not coda:
            if medial == "jw":
                fc_final = "iu" # Unique case.
    else:
        # Non-empty initial.
        if len(fc_final) > 1:
            # Non-empty coda.
            if fc_final[1] not in ('u', 'i', 'ü'):
                # Not already a diphthong.
                if fc_final[0] in ('u', 'i'):
                    if medial == 'w':
                        fc_final = 'u' + fc_final
                    elif medial == 'j':
                        if main_vowel_fc != 'i':
                            fc_final = 'i' + fc_final
                    elif medial == 'jw':
                        fc_final = 'u' + fc_final
            elif fc_final[:2] == "uu":
                if 'j' in medial:
                    fc_final = "iu" + fc_final[2:]
            elif fc_final[:2] == "ii":
                if 'w' in medial:
                    fc_final = "ui" + fc_final[2:]
        if not coda :
            # Empty coda.
            if 'j' in medial:
                if fc_final[0] in ('u', 'i'):
                    fc_final = "i" + fc_final
    if mc_initial in PALATALS_AFFRICATES and fc_final[0] in ROUND_VOWELS:
        fc_initial = 'j'  # Post-alveolar affricates were borrowed as 'j' when followed by rounded vowels.
    output = f"{fc_initial}{fc_final}"
    output = output.strip()
    if len(output) == 1:
        output *= 2
    return output

def construct_early_finnish_pronunciation(mc_initial: str, mc_final:str,
                                         fi_final: str, medial: str, main_vowel_fc: str, coda: str):
    """Construct a loaned pronunciation from Late Middle Chinese to Early Finnish."""
    fi_initial = finnish_initials[mc_initial]
    if mc_initial in ('y') and medial and medial[0] == 'j':
        medial = medial[1:]
    if not fi_initial:
        if medial:
            if medial == 'j':
                fi_initial = 'j'
                medial = medial[1:]
            elif medial == 'w':
                fi_initial = 'v'
                medial = medial[1:]
    coda_vowel: str = None
    tmp_fi = main_vowel_fc
    if coda:
        if coda[0] in ('w', 'j'):
            coda_vowel = coda[0]
    if medial:
        if medial in ('w'):
            tmp_fi = f"u{tmp_fi}"
        elif medial in ('j', 'ji'):
            tmp_fi = f"i{tmp_fi}"
        elif medial == 'jw':
            if mc_initial in ('h', "hj"):
                fi_initial = 'j'
                tmp_fi = f"u{tmp_fi}"
            else:
                tmp_fi = f"u{tmp_fi}"
        if coda_vowel:
            tmp_fi += coda[1:]
        else:
            tmp_fi += coda
    elif coda_vowel:
        tmp_fi = f"{tmp_fi}{coda.replace('j', 'i')}"
    else:
        tmp_fi += coda
    tmp_fi = tmp_fi.replace("w", "u")
    if main_vowel_fc in ('ä', 'ü'):
        tmp_fi = tmp_fi.replace('ü', 'y')
        tmp_fi = tmp_fi.replace('u', 'y')
    if mc_initial in PALATALS_AFFRICATES and tmp_fi[0] in ROUND_VOWELS:
        fi_initial = 'j'  # Post-alveolar affricates were borrowed as 'j' when followed by rounded vowels.
    output = f"{fi_initial}{tmp_fi}"
    output = output.strip()
    return output

def insert_definitions(output_dictionary_):
    def get_definition(zi_: str):
        if zi_ in definitions:
            entries = definitions[zi_]["Finnish"]
            for i in range(len(entries)):
                entries[i] = entries[i].strip()
            return entries
        return None
    for zi in output_dictionary_:
        definition_ = get_definition(zi)
        if definition_:
            output_dictionary_[zi]["Unihan-Fi"] = definition_
    return output_dictionary_

def make_entry(initial_, final_, tone, source, fanqie = None, zi = None):
    def derive_finnish_reading(finnic_reading_: str) -> str:
        """Apply known regular sound changes and notation differences."""
        output: str = finnic_reading_
        output = output.replace('c', 's')
        output = output.replace('ü', 'y')   # A difference in notation.
        return output

    def convert_vowel_core_and_medial(final_: str):
        """Get the finnic vowel core of a final, and the preceding medial, if any."""

        def split_final(final_2: str):
            """Take a Middle Chinese final, and split it into its constituent components."""
            coda_: str = ""
            tmp_: str = final_2
            # First, get the coda.
            if tmp_[-3:] in ("wng"): coda_ = tmp_[-3:]
            elif tmp_[-2:] in ("ng", "wk"): coda_ = tmp_[-2:]
            elif tmp_[-1] in ('k', 'w', 'm', 'p', 'j', 'n', 't', 'i'):
                coda_ = tmp_[-1]
                if coda_ == 'i':
                    # 'i' can be a coda, a main vowel or even a medial in some cases.
                    if len(final_2) == 1: coda_ = ''
            if coda_: tmp_ = tmp_[:-len(coda_)]
            # Next, take the main vowel.
            if tmp_[-2:] in ("ea", "ae"): main_vowel_ = tmp_[-2:]
            else: main_vowel_ = tmp_[-1]
            tmp_ = tmp_[:-len(main_vowel_)]
            medial_ = tmp_  # Last, take the medial, if any.
            if medial_ not in ('', 'j', 'w', 'jw', 'ji', 'jwi'): raise ValueError(f"Medial was '{medial_}'!")
            return medial_, main_vowel_, coda_
        if final_ == "rea":
            return "e", "", "ä", ''
        medial_, main_vowel_, coda_ = split_final(final_)
        main_vowel_fc_ = main_vowel_map[main_vowel_]
        coda_fc = coda_map[coda_]
        finnic_a = f"{main_vowel_fc_}{coda_fc}"
        if coda_:
            if main_vowel_ in ("ea", "ae") and coda_[0] == 'w':
                finnic_a = f"{main_vowel_fc_}ü{coda_fc[1:]}"
        return finnic_a, medial_, main_vowel_fc_, coda_

    def make_mc_reading(initial_1: str, final_1: str, tone_: str):
        def append_tone_mark(body_text: str):
            if tone_ == 'B':
                body_text += 'X'
            elif tone_ == 'C':
                body_text += 'H'
            return body_text
        output = f"{initial_1}{final_1}"
        if initial_1:
            if ('y' in initial_1 or 'j' in initial_1) and final_[0] == 'j':
                output = f"{initial_1}{final_1[1:]}"  # hjjwang -> hjwang, nyje -> nye
        output = output.strip()
        output = append_tone_mark(output)
        return output
    fc_final, medial, main_vowel_fc, coda = convert_vowel_core_and_medial(final_)
    north_finnic = construct_north_finnic_pronunciation(initial_, final_, fc_final, medial, main_vowel_fc, coda)
    entry: dict = {
        "Middle-Chinese": [
            {
                "reading": make_mc_reading(initial_, final_, tone),
                "initial": initial_,
                "final": final_,
                "tone": tone,
                "source": source
            }
        ],
        "early-loan": [
            {
                "Proto-Finnic": north_finnic,
                "Finnish": derive_finnish_reading(north_finnic)
            }
        ],
        "late-loan": [
            {
                "Early-Finnish": construct_early_finnish_pronunciation(initial_, final_,
                                                                       fc_final, medial, main_vowel_fc, coda)
            }
        ]
    }
    if fanqie: entry["fanqie"] = [fanqie]
    return entry

def append_entry(zi: str, entry: dict, output_dictionary: dict):
    def insert_language(section_: str, language: str):
        pronunciations: dict = output_dictionary[zi]["pronunciations"]
        existed = False
        for item in pronunciations[section_]:
            if section_ == "Middle-Chinese":
                if (item["reading"] == entry["Middle-Chinese"][0]["reading"] and
                        item["tone"] == entry["Middle-Chinese"][0]["tone"]):
                    existed = True
            else:
                if item[language] == entry[section_][0][language]:
                    existed = True
        if not existed:
            output_dictionary[zi]["pronunciations"][section_].append(entry[section_][0])

    insert_language("Middle-Chinese", "")
    insert_language("early-loan", "Proto-Finnic")
    insert_language("late-loan", "Early-Finnish")

def scrape_guangyun(output_dictionary: dict):
    def compose_guangyun_entry(zi_: str, fanqie_: str):
        # Most initials have only one value.
        #  For one's with multiple values, the first one seems to often be the canonical one.
        initial_ = initial_map[fanqie_[0]][0]
        final_ = final_map[fanqie_[1]]['sound']
        tone = final_map[fanqie_[1]]['tone']
        source = "Guangyun"
        entry = make_entry(initial_, final_, tone, source, fanqie_, zi=zi_)
        return entry

    def append_guangyun_entry(zi_: str, entry_: dict, output_dictionary_: dict):
        if zi_ not in output_dictionary_:
            output_dictionary_[zi_] = {"pronunciations": entry_}
        else:
            append_entry(zi_, entry_, output_dictionary_)
    for zi in guangyun:
        for fanqie in guangyun[zi]["fanqie"]:
            entry = compose_guangyun_entry(zi, fanqie)
            append_guangyun_entry(zi, entry, output_dictionary)

def scrape_baxter(output_dictionary: dict, baxter_counter: int = 0):
    def compose_baxter_entry(zi_: str, entry_b_: dict):
        initial_ = entry_b_["initial"]
        final_ = entry_b_["final"]
        tone = entry_b_["tone"]
        source = "Baxter-Sagart Data"
        entry = make_entry(initial_, final_, tone, source, zi=zi_)
        return entry

    def append_baxter_entries(zi_: str, entries_: list, output_dictionary_: dict):
        if BAXTER_SUPERSEDE:
            # Entries in Baxter-Sagart data must supersede data gathered by scraping Guangyun.
            for i in range(len(entries_[zi_])):
                entry_ = entries_[zi_][i]
                if i == 0:
                    output_dictionary_[zi_] = {"pronunciations": entry_}
                else:
                    append_entry(zi_, entry_, output_dictionary_)
        else:
            for zi_, baxter_entry in enumerate(entries_):
                append_entry(zi_, baxter_entry, output_dictionary_)
    for zi in baxter:
        baxter_counter += 1 if zi not in output_dictionary else 0
        entries: list = {}
        for entry_b in baxter[zi]:
            entry = compose_baxter_entry(zi, entry_b)
            if zi not in entries:
                entries[zi] = [entry]
            else:
                pre_existed = False
                for full_item in entries[zi]:
                    for item in full_item["Middle-Chinese"]:
                        if item["reading"] == entry["Middle-Chinese"][0]["reading"] and \
                                item["tone"] == entry["Middle-Chinese"][0]["tone"]:
                            pre_existed = True
                if not pre_existed:
                    entries[zi].append(entry)
        append_baxter_entries(zi, entries, output_dictionary)
    return baxter_counter

if __name__ == '__main__':
    read_data_files()
    output_dictionary: dict = {}
    print(f"Begin parsing Guangyun data.")
    scrape_guangyun(output_dictionary)
    print(f"Recovered {len(output_dictionary)} characters.")
    print("Gathering extra characters from Baxter-Sagart data.")
    # baxter_counter: int = 0
    baxter_counter = scrape_baxter(output_dictionary)
    print(f"Done. Got {baxter_counter} extra characters. Total is {len(output_dictionary)} characters.")
    print("Inserting definitions.")
    output_dictionary = insert_definitions(output_dictionary)
    print("Done inserting definitions.")
    with open('product/FinnicKanji.yaml', 'w', encoding='utf-8') as f:
        print(f"Writing to file '{f.name}'.")
        write_file_time_start = time.perf_counter()
        f.write(f"# Includes {len(output_dictionary)} characters.\n")
        mc_yaml = yaml.dump(output_dictionary, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        write_file_time_end = time.perf_counter()
        print(f"Compiled to file '{f.name}' in {write_file_time_end - write_file_time_start:0.4f} seconds. ")

