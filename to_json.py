import pandas as pd
import json

DATASET_PATH = "./final_dataset.csv"

df = pd.read_csv(DATASET_PATH)

JSON_format = """
	"context": "{sentence}",
	"qas": [
		<
			"id": "{id_1}",
			"is_impossible": {is_impossible_1},
			"question": "What is the type of event?",
			"answers": [{answer_1}]
		>,
		<
			"id": "{id_2}",
			"is_impossible": {is_impossible_2},
			"question": "Who is the actor?",
			"answers": [{answer_2}]
		>,
		<
			"id": "{id_3}",
			"is_impossible": {is_impossible_3},
			"question": "What is the reason of the event?",
			"answers": [{answer_3}]
		>
	]
"""
print(df.columns)
final_jsons = []

for index, row in df.iterrows():
	sentence = row['Statement'].strip().replace("\"", "")
	answer_1_text = row['Event Type'].strip().replace("\"", "")
	is_impossible_1 = "false"
	is_impossible_2 = "false"
	is_impossible_3 = "false"
	answer_1_start = sentence.find(answer_1_text)
	answer_2_text = row['Event Actor'].strip().replace("\"", "")
	answer_2_start = sentence.find(answer_2_text)
	answer_3_text = row['Event Reason'].strip().replace("\"", "")
	answer_3_start = sentence.find(answer_3_text)
	if answer_1_text.lower() == "unknown":
		is_impossible_1 = "true"
	if answer_2_text.lower() == "unknown":
		is_impossible_2 = "true"
	if answer_3_text.lower() == "unknown":
		is_impossible_3 = "true"
	answer_1 = f'{{"text": "{answer_1_text}", "answer_start": {answer_1_start}}}' if is_impossible_1 == "false" else ''
	answer_2 = f'{{"text": "{answer_2_text}", "answer_start": {answer_2_start}}}' if is_impossible_2 == "false" else ''
	answer_3 = f'{{"text": "{answer_3_text}", "answer_start": {answer_3_start}}}' if is_impossible_3 == "false" else ''
	json_entry = JSON_format.format(
		sentence=sentence,
		id_1=f"{index*3+1}",
		is_impossible_1=is_impossible_1,
		answer_1=answer_1,
		id_2=f"{index*3+2}",
		is_impossible_2=is_impossible_2,
		answer_2=answer_2,
		id_3=f"{index*3+3}",
		is_impossible_3=is_impossible_3,
		answer_3=answer_3
	)
	json_entry = "{" + json_entry.replace("<", "{").replace(">", "}") + "}"
	final_jsons.append(json_entry)

with open("data/final.json", "w", encoding='utf-8') as f:
	f.write("[\n")
	f.write(",\n".join(final_jsons))
	f.write("\n]")
