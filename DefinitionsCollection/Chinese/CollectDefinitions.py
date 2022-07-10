import yaml
import time
# from googletrans import Translator
from google_trans_new import google_translator as Translator
import google_trans_new

translator = Translator()
BULK_TRANSLATE: bool = False

# translate_text = translator.translate('สวัสดีจีน',lang_tgt='en')
# print(translate_text)

def translate_definitions(definitions: list, error_wait_factor: int = 1) -> list:
    translations: list = []
    try:
        if BULK_TRANSLATE:
            translations = translator.translate(definitions, "fi", "en")
        else:
            for defi_ in definitions:
                transl_ = translator.translate(defi_, "fi", "en")
                translations.append(transl_)
    except google_trans_new.google_trans_new.google_new_transError as ex:
        error_wait_time = 2 * len(definitions) * error_wait_factor
        print(f"Translation error interrupted the program:"
              f"\n\t{ex}"
              f"\nTrying again after {error_wait_time} seconds.")
        time.sleep(error_wait_time)   # Wait a bit first.
        return translate_definitions(definitions, error_wait_factor=(error_wait_factor+1))
    return translations

if __name__ == '__main__':
    with open("kDefinitionsPlus.yaml", 'r', encoding='utf-8') as my_file:
        print(f"Reading '{my_file.name}'.")
        read_data_start = time.perf_counter()
        k_definitions = yaml.safe_load(my_file)
        read_data_stop = time.perf_counter()
        print(f"Collected {len(k_definitions)} entries in {read_data_stop - read_data_start:0.4f}. seconds")
    number_of_definitions = 0
    for zi in k_definitions:
        number_of_definitions += 1 if "kDefinition" in k_definitions[zi] else 0
    print(f"Number of definitions is {number_of_definitions}.")
    translations_dict = {}
    def collect_translations():
        print("Commencing translations.")
        counter = 1
        for zi in k_definitions:
            if "kDefinition" in k_definitions[zi]:
                definitions = k_definitions[zi]["kDefinition"]
                if not definitions: continue    # Skip empty definitions, if any.
                status_line = f"{zi} ({counter} / {number_of_definitions}, {round(counter / number_of_definitions * 100, 2)} %)"
                # for item in definitions:
                #     status_line += f"\n\t{item}"
                print(f"Translating {status_line}")
                translations = translate_definitions(definitions)
                time.sleep(0.7 * len(definitions))  # Avoid making requests too fast.
                # print(f"\t{translations}")
                translations_dict[zi] = {
                    "Unihan": definitions,
                    "Finnish": translations
                }
                counter += 1
    try:
        collect_translations()
    except KeyboardInterrupt:
        print(f"Application interrupted from keyboard."
              f"\nManaged to get translations for {len(translations_dict)} characters."
              f"\nWriting them to file now.")
    with open(f'DefinitionsFinnish{len(translations_dict)}.yaml', 'w', encoding='utf-8') as f:
        print(f"Collected and translated {len(translations_dict)} definitions.")
        f.write(f"# Contains {len(translations_dict)} / {number_of_definitions} entries. "
                f"({round(len(translations_dict)/number_of_definitions*100, 2)} %)\n")
        write_data_start = time.perf_counter()
        defi_yaml = yaml.dump(translations_dict, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        write_data_stop = time.perf_counter()
        print(f"Wrote to '{f.name}' in {write_data_stop - write_data_start:0.4f} seconds.")

