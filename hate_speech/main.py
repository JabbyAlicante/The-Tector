import json
import re
# from hate_speech.bots.tgbot import *

bw = None

def check_user_exists(user_id, users):
    if user_id == 1:
        print(1)
    else:
        pass
    # pass

def add_user(user_id, first_name, last_name):

    pass

def check_users(users):
    for key, val in users.items():
        print(val)
    # pass

def get_users_log():
    with open("./hate_speech/datasets/users.json", "r", encoding="utf-8") as users_f:
        users = json.load(users_f)

    # print("get users log: ", users)

    check_users(users)
    # return users

def log_user():
    pass

def reply_message(rcved_mssg, user):

    tknz = tokenize(rcved_mssg)
    print(f"Tokens: {tknz}")

    if any(token in bw for token in tknz):
        return f"warning: {user}"

def get_bad_words():
    global bw

    # if bw is None:
    #     bw = get_bad_words()

    print("get_bad_words")
    with open("./hate_speech/datasets/bad_words.json", "r", encoding="utf-8") as f:
        bw = json.load(f)

    return bw

def normalize(text):
    text = text.lower()
    text = re.sub(r"\W", '', text)
    text = re.sub(r"\s+", '', text)
    return text

def tokenize(text, special_tokens = True):
    # TODO: exclude multi-word
    tokens = re.split('[—\-\s\']', text)
    tokens = list(map(normalize, tokens))

    # This one is optional, depending on your use case
    # if special_tokens:
    #     tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]
    return tokens

if __name__ == "__main__":
    # m = main("bastard", "sample_user")
    # print(m)

    get_users_log()