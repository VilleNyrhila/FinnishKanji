import yaml

# Globals
initials_map = {}
manual_additions = {}
missing_initials= ""
result_line = ""

with open('../data/MiddleChinese.yaml', 'r', encoding='utf-8') as my_file:
    guangyun = yaml.safe_load(my_file)
with open('../data/BaxterSagartData.yaml', 'r', encoding='utf-8') as my_file:
    baxter = yaml.safe_load(my_file)

def assemble_initials():
    global initials_map, guangyun
    for zi in guangyun:
        for fanqie in guangyun[zi]["fanqie"]:
            initial = fanqie[0]
            initials_map[initial] = []
    print(f"{len(initials_map)} unique initials.")
assemble_initials()

def remove_redundants(map_):
    print("Removing redundant sounds")
    for zi_ in map_:
        map_[zi_] = list(dict.fromkeys(map_[zi_]))
    print("Redundant sounds removed.")
    return map_

def populate_map():
    global initials_map, result_line, missing_initials

    def append_to_map(map_, zi_, sound_):
        map_[zi_].append(sound_)
        return map_
    counter = 0
    for zi in initials_map:
        if zi in baxter:
            print(f"In Baxter")
            for zi_baxter in baxter[zi]:
                sound = zi_baxter["initial"]
                print(f"\t{zi} = {sound}")
                initials_map = append_to_map(initials_map, zi, sound)
            counter += 1
        elif zi in guangyun:
            print("In Guangyun, not Baxter")
            alt_ = ""
            for item in guangyun[zi]["fanqie"]:
                alt_ += item[0]
            for zi_alt in alt_:
                if zi_alt in baxter:
                    for zi_baxter in baxter[zi_alt]:
                        sound = zi_baxter["initial"]
                        print(f"\t{zi} = {sound} ({zi_alt})")
                        initials_map = append_to_map(initials_map, zi, sound)
            counter += 1
        else:
            missing_initials += zi
    result_line = f"Resolved initials: {counter}/{len(initials_map)} " \
                  f"({round(counter/len(initials_map), 3) * 100}%)"
    print(result_line)
populate_map()
initials_map = remove_redundants(initials_map)
def add_manual_additions():
    global manual_additions, initials_map, missing_initials
    missing_initials = ""
    print("Inserting manual additions.")
    with open('./Manual_InitialAdditions.yaml', 'r', encoding='utf-8') as my_file:
        manual_additions = yaml.safe_load(my_file)    # Get manual additions.
    print("\t", end="")
    for zi in manual_additions:
        print(zi, end="")
        missing_initials += zi
        initials_map[zi] = manual_additions[zi] # Add manual additions.
    print()
    print("Manual additions put in.")
add_manual_additions()

def find_empty_ones():
    global initials_map
    error_line = "Unfound keys are: '"
    for zi in initials_map:
        if not initials_map[zi]:
            error_line += zi
    error_line += "'"
    print(error_line)
find_empty_ones()

def write_to_file():
    with open("./InitialMap.yaml", 'w', encoding='utf-8') as f:
        f.write(f"# {result_line}\n")
        f.write(f"# Missing initials: {len(missing_initials)} "
                f"({round(len(missing_initials)/len(initials_map), 3) * 100}%)\n")
        f.write(f"# Manually added {len(manual_additions)} initials.\n")
        f.write(f"# {missing_initials}\n")
        mc_yaml = yaml.dump(initials_map, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
write_to_file()
