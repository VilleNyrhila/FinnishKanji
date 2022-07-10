from pymongo import MongoClient
import pprint
import yaml
# import json

myclient = MongoClient("mongodb://localhost:27017/")

# db = myclient["test"]
# col = db[ "testcol" ]
# file_data = { "foo": "bar"}
# col.insert_one(file_data)
# pprint.pprint(col.find_one())

kanji_db = myclient["FinnicKanji"]
kanji_collection = kanji_db["main"]

with open('../product/FinnicKanji.yaml', 'r', encoding='utf-8') as my_file:
    finnics = yaml.safe_load(my_file)
    print(f"Done reading {my_file.name}.")

output_list = []
for kanji in finnics:
    entry = {}
    entry["character"] = kanji
    entry["pronunciations"] = finnics[kanji]
    output_list.append(entry)
print("Saving to database.")
kanji_collection.insert_many(output_list)
# kanji_collection.insert_one(finnics)
