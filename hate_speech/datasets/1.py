import json
texts = []

with open("./hate_speech/datasets/txt.txt", "r") as file:
    for line in file:
        texts.append(line.strip())

for i in texts:
    print(i)

with open("./hate_speech/datasets/bad_words.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, indent=4, ensure_ascii=False)