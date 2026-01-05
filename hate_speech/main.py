import json
import re
from datetime import datetime, timedelta
# import tokenize
# from hate_speech.bots.tgbot import *

bw = None

def check_violator_exists(user_id, violators):
    return any(v["id"] == user_id for v in violators["violators"])

def add_violator(violator_id, first_name, last_name):
    violators = get_violators_log()

    violators["violators"].append({
        "id": violator_id,
        "full_name": f"{first_name} {last_name}",
        "warnings": 0,
        "banned_until": None
    })

    with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
        json.dump(violators, f, indent=4)

def compute_ban_duration():
    now = datetime.now()
    ban_duration = now + timedelta(hours=2)

    # print(ban_duration.strftime("%Y-%m-%d %H:%M:%S"))
    return ban_duration

def check_warnings(user_id):
    violators = get_violators_log()

    for vltr in violators["violators"]:
        if vltr["id"] == user_id and vltr["warnings"] >= 3:
            ban_until = compute_ban_duration()

            vltr["warnings"] = 0
            vltr["banned_until"] = ban_until.strftime("%Y-%m-%d %H:%M:%S")

            with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
                json.dump(violators, f, indent=4)

            return ban_until

    return None

    
    # print(violators["violators"])
    # for key, val in violators.items():
    #     print(val)
    # pass

def get_violators_log():
    with open("./hate_speech/datasets/violators.json", "r", encoding="utf-8") as violators_f:
        violators = json.load(violators_f)

    # print("get violators log: ", violators)

    # check_warnings(violators)
    return violators

def update_violator(id):
    log = get_violators_log()

    for vltr in log["violators"]:
        if vltr["id"] == id:
            vltr["warnings"] += 1
            break
    
    with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as updated_log_f:
        json.dump(log, updated_log_f, indent = 4)
    # pass

def get_users_log():
    with open("./hate_speech/datasets/users.json", "r", encoding="utf-8") as users_f:
        users = json.load(users_f)

    # print("get users log: ", users)

    check_users(users)
    return users

def log_user():
    pass

def reply_message(rcved_mssg, user):
    tknz = tokenize(rcved_mssg)
    print(f"Tokens: {tknz}")

    violators = get_violators_log()

    if any(token in bw for token in tknz):
        if not check_violator_exists(user.id, violators):
            add_violator(user.id, user.first_name, user.last_name)
        else:
            update_violator(user.id)

        return f"⚠️ Warning: {user.full_name}"
    
    return None

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
    # tokens = re.split('[—\-\s\']', text)
    tokens = re.split(r"[—\-\s']", text)

    tokens = list(map(normalize, tokens))

    # This one is optional, depending on your use case
    # if special_tokens:
    #     tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]
    return tokens

if __name__ == "__main__":
    # m = main("bastard", "sample_violator")
    # print(m)

    # get_violators_log()

    # check_warnings()
    
    compute_ban_duration()