import yaml

with open('../data/MiddleChinese.yaml', 'r', encoding='utf-8') as my_file:
    guangyun = yaml.safe_load(my_file)
with open('../data/BaxterSagartData.yaml', 'r', encoding='utf-8') as my_file:
    baxter = yaml.safe_load(my_file)
with open('./ManualFinalAdditions.yaml', 'r', encoding='utf-8') as my_file:
    manual_additions = yaml.safe_load(my_file)

finals_map = {}
print("Going through Guangyun.")
for zi in guangyun:
    for fanqie in guangyun[zi]["fanqie"]:
        final = fanqie[1]
        finals_map[final] = ""
print(f"Finished reading Guangyun. Found {len(finals_map)} unique finals.")
counter = 0
missing_finals= ""
print(f"Looking up readings and tones for finals from Baxter-Sagart document data.")
for zi in finals_map:
    if zi in baxter:
        for zi_baxter in baxter[zi]:
            sound = zi_baxter["final"]
            tone = zi_baxter["tone"]
            print(f"{zi} = {sound} {tone}")
            finals_map[zi] = {
                "sound": sound,
                "tone": tone
            }
        counter += 1
    elif zi in guangyun:
        alt_ = ""
        for item in guangyun[zi]["fanqie"]:
            alt_ += item[1]
        sound = ""
        for zi_alt in alt_:
            if zi_alt in baxter:
                for zi_baxter in baxter[zi_alt]:
                    sound = zi_baxter["final"]
                    tone = zi_baxter["tone"]
                    # print(f"{zi} = {sound}")
                    print(f"{zi} = {sound} {tone}")
                    finals_map[zi] = {
                        "sound": sound,
                        "tone": tone
                    }
        if sound:
            counter += 1
        else:
            missing_finals += zi
    else:
        missing_finals += zi
result_line = f"Resolved finals: {counter}/{len(finals_map)} " \
              f"({round(counter / len(finals_map), 3) * 100}%)"
print(result_line)
print(f"Adding {len(manual_additions)} manual additions.")
for zi in manual_additions:
    finals_map[zi] = manual_additions[zi]
print(f"Done. Compiled {len(finals_map)} characters.")
result_line += f"\n# With manual additions: {len(finals_map)} characters."
with open("./FinalMap.yaml", 'w', encoding='utf-8') as f:
    f.write(f"# {result_line}\n")
    # f.write(f"# Missing initials: {len(missing_finals)} "
    #         f"({round(len(missing_finals) / len(finals_map), 3) * 100}%)\n")
    f.write(f"# {missing_finals}\n")
    f.write(f"# Manually added {len(manual_additions)} characters.\n")
    mc_yaml = yaml.dump(finals_map, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
