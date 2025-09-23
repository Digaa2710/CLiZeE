import google.generativeai as genai
import pandas as pd
import csv

genai.configure(api_key="your-api-key-here")
model = genai.GenerativeModel("gemini-2.0-flash")

df = pd.read_csv("./my_dataset_final.csv")
sentences = df['Statement'].tolist()
event_types = df['Event Type'].tolist()
event_actors = df['Event Actor'].tolist()
event_reasons = df['Event Reason'].tolist()
print(f"Number of sentences to process: {len(sentences)}")

prompt = """You are a sentence transforming agent and are given statements, event type, event actor, event reason.
Your task is to edit the statements to include the event type, event actor, and event reason in a natural way.
Your output should be a list of the edited statements, one per line, without any numbering or extra text or any formatting.
Here are the statements:"""
for i in range(len(sentences)):
    prompt += f"{sentences[i]},{event_types[i]},{event_actors[i]},{event_reasons[i]}\n"

try:
    response = model.generate_content(prompt)
    raw_text = response.text
    clean_text = raw_text.strip()
    print("===== Classification Result from Model =====\n")
    print(clean_text)

    with open(f"./Gemini_CSVs/final_dataset.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Statement", "Event Type", "Event Actor", "Event Reason"])        

    print("\n✅ Successfully parsed and saved the results to result.csv")

except Exception as e:
    print(f"An error occurred: {e}")
    e.with_traceback()
