import json
import re
from datetime import datetime, timedelta

# import tokenize
# from hate_speech.bots.tgbot import *



# ---------------- 


# Load datasets | Maliit scope, add more tagalog
def load_badwords():
    with open("../../hate_speech/datasets/badwords.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_slurs():
    with open("../../hate_speech/datasets/slurs.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_group_identifiers():
    with open("../../hate_speech/datasets/group_identifiers.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_dehumanizing_terms():
    with open("../../hate_speech/datasets/dehumanizing_terms.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_violence_patterns():
    with open("../../hate_speech/datasets/violence_patterns.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_hate_phrases():
    with open("../../hate_speech/datasets/hate_phrases.json", "r", encoding="utf-8") as f:
        return json.load(f)


# Preloading
def preload_datasets():
    load_badwords()
    load_slurs()
    load_group_identifiers()
    load_dehumanizing_terms()
    load_violence_patterns()
    load_hate_phrases()




def normalize_word(word):
    return re.sub(r'[^a-zA-Z]', '', word.lower())



def create_pattern(word):
    leet_map = {
        'a': '[a@4]',
        'e': '[e3]',
        'i': '[i1!|]',
        'o': '[o0]',
        's': '[s5$]',
        't': '[t7]',
        'l': '[l1|]',
        'g': '[g9]',
        'b': '[b8]',
        'z': '[z2]'
    }

    pattern = ''

    for char in word:
        pattern += leet_map.get(char, char) + r"[\*\.\-_\s]{0,2}"


        # if i < len(word) - 1:
        #     pattern += r'+' 
    
    return pattern


def pattern_matching(text, word_list):
    text_lower = text.lower()
    matches = []

    for raw_word in word_list:
        # pattern = create_pattern(word)
        word = normalize_word(raw_word)

        if not word:
            continue

        # pattern = create_pattern(word)
        # pattern = rf'\b{pattern}\b'


        # if re.search(pattern, text_lower):
          #     matches.append(word)

        # Identifying regex error
        try:
            if re.search(rf"\b{create_pattern(word)}\b", text_lower):
                matches.append(word)

        except re.error as e:
            # print("\n🚨 REGEX CRASH 🚨")
            # print("Word:", repr(word))
            # print("Pattern:", pattern)
            # print("Error:", e)
            # raise
            print(f"SKIPPED INVALID WORD: {raw_word} -> {pattern}")
            continue

    return list(set(matches))



def check_profanity(text):
    data = load_badwords()
    matches = pattern_matching(text, data.get("words", []))
    
    
    # simple_words = bad_words_data.get("words", [])
    # custom_patterns = bad_words_data.get("patterns", [])
    
    # simple_matches = pattern_matching(text, simple_words)
    
    # pattern_matches = match_custom_pattern(text, custom_patterns)

    
    return {
        "detected": bool(matches), 
        "matched_words": matches
    }



def check_slurs(text):
    
    slurs_data = load_slurs()
    matches = []

    # text_lower = text.lower() 
    
    # for category, slur_info in slurs_data.items():
    #     words = slur_info.get("words", [])
    #     patterns = slur_info.get("patterns", [])
    
    for category, info in slurs_data.items():
        words = info.get("words", [])
        matches += pattern_matching(text, words)
    
    return {
        "detected": bool(matches), 
        "matches": matches
    }




def check_group_dehumanization(text):
    groups = load_group_identifiers()
    dehumanizing = load_dehumanizing_terms()
   
    text_lower = text.lower()
    targets = []
    
    for cat, identifiers in groups.items():

    # for category, identifiers in group_identifiers.items():
    #     for identifier in identifiers:
    #         if re.search(rf"\b{re.escape(identifier)}\b", text_lower):
    #             groups.append(category)

        for w in identifiers:            
            if re.search(rf"\b{re.escape(w)}\b", text_lower):
                
                targets.append(cat)
    
    
    dehumanizing_matches = pattern_matching(text, dehumanizing.get("words", []))
    detected = bool(targets) and bool(dehumanizing_matches)
    
    return {
        "detected": detected, 
        "groups": targets, 
        "dehumanizing_terms": dehumanizing_matches
    }



def check_violence(text):
    groups = load_group_identifiers()
    violence_patterns = load_violence_patterns()
    text_lower = text.lower()
    
    targets = []
    found_violence = []

    for cat, identifiers in groups.items():
        for w in identifiers:
            if re.search(rf"\b{re.escape(w)}\b", text_lower):
                targets.append(cat)

   
    for pattern in violence_patterns:
        if re.search(pattern, text_lower):
            found_violence.append(pattern)

    detected = bool(targets) and bool(found_violence)
    return {
        "detected": detected, 
        "groups": targets, 
        "patterns": found_violence
    }


def check_hate_phrases(text):
    phrases = load_hate_phrases()
    matched = [p for p in phrases if p.lower() in text.lower()]
    
    
    return {
        "detected": bool(matched), 
        "matches": matched
    }

def check_hate_speech(text):
    slurs = check_slurs(text)
    dehumanization = check_group_dehumanization(text)
    violence = check_violence(text)
    phrases = check_hate_phrases(text)
    
    detected = any([
        slurs["detected"], 
        dehumanization["detected"], 
        violence["detected"], 
        phrases["detected"]
    ])


    
    targets = list(set(dehumanization["groups"] + violence["groups"]))
    return {
        "detected": detected,
        "signals": {
            "slurs": slurs,
            "dehumanization": dehumanization,
            "violence": violence,
            "hate_phrases": phrases
        },
        "target_groups": targets
    }

   

def analyze_content(text):
    profanity = check_profanity(text)
    hate = check_hate_speech(text)

    severity = (
        "CRITICAL" if hate["detected"]
        else "WARNING" if profanity["detected"]
        else "CLEAN"
    )

    return {
        "severity": severity,
        "profanity": profanity,
        "hate_speech": hate
    }


# ------------------------ VIOLATION MANAGEMENT

def get_violators_log():

    with open("./hate_speech/datasets/violators.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_violators(violators):

    with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
        json.dump(violators, f, indent=4)


def handle_violation(user, violation_type, severity):
    violators = get_violators_log()
    entry = next((v for v in violators["violators"] if v["id"] == user.id), None)

    now = datetime.utcnow()

    if entry and entry.get("muted_until"):
        muted_until = datetime.fromisoformat(entry["muted_until"])
        
        if now >= muted_until:
            entry["warnings"] = 0
            entry["muted_until"] = None

    if not entry:
        entry = {
            "id": user.id,
            "name": user.full_name,
            "warnings": 0,
            "violations": [],
            "muted_until": None
        }

        violators["violators"].append(entry)

    entry["warnings"] += 1
    entry["violations"].append(violation_type)
    
    # save_violators(violators)
    action_result = {
        "action": "warn",
        "warnings": entry["warnings"]
    }


    if severity == "CRITICAL":
        if entry["warnings"] >= 1:
            # return {"action": "ban", "duration": timedelta(days=7)}
            
            return {
                "action": "kick"
                # "duration": timedelta(minutes=1)
            }

        else:
            
            mute_duration = timedelta(minutes=1)
            entry["muted_until"] = (now + mute_duration).isoformat()
            
            action_result = {
                "action": "mute",
                "duration": mute_duration
            }

        # return {"action": "mute", "duration": timedelta(hours=24)}
        # return {
        #     "action": "mute", 
        #     "duration": timedelta(minutes=1)
        # }
    


    elif severity == "WARNING" and entry["warnings"] >= 3:
        # return {"action": "mute", "duration": timedelta(hours=2)}
        
        mute_duration = timedelta(minutes=2)
        entry["muted_until"] = (now + mute_duration).isoformat()
        
        action_result = {
            "action": "mute",
            "duration": mute_duration
        }

        # return {
        #     "action": "mute", 
        #     "duration": timedelta(minutes=2)
        # }


    # return {
    #     "action": "warn", 
    #     "warnings": entry["warnings"]
    # }

    save_violators(violators)
    return action_result

# ------------------------------------ MAIN MESSAGE HANDLER

def reply_message(text, user):
    analysis = analyze_content(text)

    if analysis["severity"] == "CLEAN":
        return None

    violation_type = (
        "hate_speech" if analysis["hate_speech"]["detected"] else "profanity"
    )

    action = handle_violation(user, violation_type, analysis["severity"])

    return {
        "analysis": analysis,
        "action": action,
        "text": f"Severity: {analysis['severity']} | Violation: {violation_type}"
    }

# ----------------------------------------- TESTING

# if __name__ == "__main__":
#     test_messages = [
#         "This is clean",
#         # "f*ck this",
#         # "f u c k",
#         "fuuuuckkkkk",
#         # "sh1t",
#         "a$$holeeeee",
#         "Go back to your country",
#         "All immigrants are vermin",
#         "Get rid of latinos",
#         "disabled people should shut up"
#     ]
    
#     for msg in test_messages:
#         print(f"\nMessage: '{msg}'")
#         result = analyze_content(msg)
#         print(f"Severity: {result['severity']}")

#         violation_types = get_violation_types(result)
#         if violation_types:
#             print(f"Violation Type(s): {violation_types}")

#         if result['profanity']['detected']:
#             print(f"Matched Profanity: {result['profanity']['matched_words']}")

#         if result['hate_speech']['detected']:
#             print(f"Target Groups: {result['hate_speech']['target_groups']}")

# ---------------- GERI 


# ASH
# bw = None

# def check_violator_exists(user_id, violators):
#     return any(v["id"] == user_id for v in violators["violators"])

# def add_violator(violator_id, first_name, last_name):
#     violators = get_violators_log()

#     violators["violators"].append({
#         "id": violator_id,
#         "full_name": f"{first_name} {last_name}",
#         "warnings": 0,
#         "banned_until": None
#     })

#     with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
#         json.dump(violators, f, indent=4)

# def compute_ban_duration():
#     now = datetime.now()
#     ban_duration = now + timedelta(hours=2)

#     # print(ban_duration.strftime("%Y-%m-%d %H:%M:%S"))
#     return ban_duration

# def check_warnings(user_id):
#     violators = get_violators_log()

#     for vltr in violators["violators"]:
#         if vltr["id"] == user_id and vltr["warnings"] > 1:
#             # Reset warnings
#             vltr["warnings"] = 0
#             with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
#                 json.dump(violators, f, indent=4)

#             # Return True to indicate mute should happen
#             return True

#     # Not enough warnings
#     return False

    
#     # print(violators["violators"])
#     # for key, val in violators.items():
#     #     print(val)
#     # pass

# def get_violators_log():
#     with open("./hate_speech/datasets/violators.json", "r", encoding="utf-8") as violators_f:
#         violators = json.load(violators_f)

#     # print("get violators log: ", violators)

#     # check_warnings(violators)
#     return violators

# def update_violator(id):
#     log = get_violators_log()

#     for vltr in log["violators"]:
#         if vltr["id"] == id:
#             vltr["warnings"] += 1
#             break
    
#     with open("./hate_speech/datasets/violators.json", "w", encoding="utf-8") as updated_log_f:
#         json.dump(log, updated_log_f, indent = 4)
#     # pass

# def get_users_log():
#     with open("./hate_speech/datasets/users.json", "r", encoding="utf-8") as users_f:
#         users = json.load(users_f)

#     # print("get users log: ", users)

#     # check_users(users)
#     return users

# def log_user():
#     pass

# def reply_message(rcved_mssg, user):
#     tknz = tokenize(rcved_mssg)
#     print(f"Tokens: {tknz}")

#     violators = get_violators_log()

#     if any(token in bw for token in tknz):
#         if not check_violator_exists(user.id, violators):
#             add_violator(user.id, user.first_name, user.last_name)
#         else:
#             update_violator(user.id)

#         return f"⚠️ Warning: {user.full_name}"
    
#     return None

# def get_bad_words():
#     global bw

#     # if bw is None:
#     #     bw = get_bad_words()

#     print("get_bad_words")
#     with open("./hate_speech/datasets/bad_words.json", "r", encoding="utf-8") as f:
#         bw = json.load(f)

#     return bw

# def normalize(text):
#     text = text.lower()
#     text = re.sub(r"\W", '', text)
#     text = re.sub(r"\s+", '', text)
#     return text

# def tokenize(text, special_tokens = True):
#     # TODO: exclude multi-word
#     # tokens = re.split('[—\-\s\']', text)
#     tokens = re.split(r"[—\-\s']", text)

#     tokens = list(map(normalize, tokens))

#     # This one is optional, depending on your use case
#     # if special_tokens:
#     #     tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]
#     return tokens

# if __name__ == "__main__":
#     # m = main("bastard", "sample_violator")
#     # print(m)

#     # get_violators_log()

#     # check_warnings()
    
#     compute_ban_duration()
