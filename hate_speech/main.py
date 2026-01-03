import json
import re 

def main(rcved_mssg, user):
    bw = get_bad_words()
    # for i in bw:
    #     print(i)

    
    pass

def get_bad_words():
    print("get_bad_words")
    with open("./hate_speech/datasets/bad_words.json", "r", encoding="utf-8") as f:
        bw = json.load(f)

    return bw

def normalize(text):
    text = text.lower()
    text = re.sub(r"\W", '', text)
    text = re.sub(r"\s+", '', text)
    return text

# if __name__ == "__main__":
#     main("bastard", "sample_user")