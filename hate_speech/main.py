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



def create_speak_pattern(word):
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
    for char in word.lower():
        if char in leet_map:
            pattern += leet_map[char]
        else:
            pattern += char
    
    return pattern


def create_pattern(word):
    pattern = ''

    for i, char in enumerate(word.lower()):
        if char in 'aeiostz':
            leet_map = {
                'a': '[a@4]', 'e': '[e3]', 'i': '[i1!|]',
                'o': '[o0]', 's': '[s5$]', 't': '[t7+]', 'z': '[z2]'
            }

            # pattern += leet_map.get(char, char)
            pattern += leet_map.get(char, char) + '+'

        else:
            pattern += char


        pattern += r'[\*\.\-_\s]{0,2}'

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

        pattern = create_pattern(word)
        pattern = rf'\b{pattern}\b'


        # if re.search(pattern, text_lower):
        #     matches.append(word)

        # Identifying regex error
        try:
            if re.search(pattern, text_lower):
                matches.append(word)

        except re.error as e:
            # print("\n🚨 REGEX CRASH 🚨")
            # print("Word:", repr(word))
            # print("Pattern:", pattern)
            # print("Error:", e)
            # raise
            print(f"SKIPPED INVALID WORD: {raw_word} -> {pattern}")

    return list(set(matches))



def match_custom_pattern(text, patterns):

    text_lower = text.lower()
    matches = []

    for pattern_data in patterns:
        if isinstance(pattern_data, dict):
            pattern = pattern_data.get("pattern")
            word = pattern_data.get("word")
        else:
            
            pattern = pattern_data
            word = pattern_data
        
        try:
            if re.search(pattern, text_lower):
                matches.append({"word": word, "pattern": pattern})
        except re.error:
            
            continue
    
    return matches


def tokenize(text):
    tokens = re.split(r"[—\-\s']", text)
    return [normalize(t) for t in tokens if t]


def check_profanity(text):
    bad_words_data = load_badwords()
    
    simple_words = bad_words_data.get("words", [])
    custom_patterns = bad_words_data.get("patterns", [])
    
    simple_matches = pattern_matching(text, simple_words)
    
    pattern_matches = match_custom_pattern(text, custom_patterns)
    
    # all_matches = simple_matches + [m["word"] for m in pattern_matches]
    all_matches = list(set(simple_matches + [m["word"] for m in pattern_matches]))


    return {
        "detected": len(all_matches) > 0,
        "matched_words": all_matches,
        "type": "profanity"
    }


# --------------------- HATE SPEECH DETECTION
def check_slurs(text):
    slurs_data = load_slurs()
    text_lower = text.lower()
    matched = []
    
    for category, slur_info in slurs_data.items():
        words = slur_info.get("words", [])
        patterns = slur_info.get("patterns", [])
        
        word_matches = pattern_matching(text, words)
        for word in word_matches:
            matched.append({"slur": word, "category": category})
        
        pattern_matches = match_custom_pattern(text, patterns)
        for match in pattern_matches:
            matched.append({"slur": match["word"], "category": category})
    
    return {
        "detected": len(matched) > 0,
        "matches": matched
    }


def check_group_dehumanization(text):
    group_identifiers = load_group_identifiers()
    dehumanizing_data = load_dehumanizing_terms()
    text_lower = text.lower()
    
    groups = []
    dehumanizing = []
    
    for category, identifiers in group_identifiers.items():
        for identifier in identifiers:
            if re.search(rf"\b{re.escape(identifier)}\b", text_lower):
                groups.append(category)
    
    
    words = dehumanizing_data.get("words", [])
    patterns = dehumanizing_data.get("patterns", [])
    
    
    word_matches = pattern_matching(text, words)
    dehumanizing.extend(word_matches)
    
    # Check patterns
    pattern_matches = match_custom_pattern(text, patterns)
    dehumanizing.extend([m["word"] for m in pattern_matches])
    
    detected = len(groups) > 0 and len(dehumanizing) > 0
    
    return {
        "detected": detected,
        "groups": groups,
        "dehumanizing_terms": dehumanizing
    }


def check_group_violence(text):
    group_identifiers = load_group_identifiers()
    violence_patterns = load_violence_patterns()
    text_lower = text.lower()
    
    groups = []
    violence = []
    
    
    for category, identifiers in group_identifiers.items():
        for identifier in identifiers:
    
            # if identifier in text_lower:
            if re.search(rf"\b{re.escape(identifier)}\b", text_lower):
                groups.append(category)
    
    # Look for violenve patterns
    for pattern in violence_patterns:
        if pattern in text_lower:
            violence.append(pattern)
    
    detected = len(groups) > 0 and len(violence) > 0
    
    return {
        "detected": detected,
        "groups": groups,
        "violence_patterns": violence
    }


def check_hate_phrases(text):

    hate_phrases = load_hate_phrases()
    text_lower = text.lower()
    
    matched = [phrase for phrase in hate_phrases if phrase in text_lower]
    
    return {
        "detected": len(matched) > 0,
        "matches": matched
    }


def identify_target_groups(text):

    group_identifiers = load_group_identifiers()
    text_lower = text.lower()
    targets = []
    
    for category, identifiers in group_identifiers.items():
        for identifier in identifiers:

            # if identifier in text_lower:
            if re.search(rf"\b{re.escape(identifier)}\b", text_lower):
                targets.append(category)
                break
    
    return list(set(targets))


def check_hate_speech(text):
    # Detecting matches for any type of hate speech    
    slur_matches = check_slurs(text)
    
    group_dehumanization = check_group_dehumanization(text)
    
    group_violence = check_group_violence(text)
    
    phrase_matches = check_hate_phrases(text)
    
    detected = any([
        slur_matches["detected"],
        group_dehumanization["detected"],
        group_violence["detected"],
        phrase_matches["detected"]
    ])
    
    return {
        "detected": detected,
        "type": "hate_speech",
        "signals": {
            "slurs": slur_matches,
            "group_dehumanization": group_dehumanization,
            "group_violence": group_violence,
            "hate_phrases": phrase_matches
        },
        "target_groups": identify_target_groups(text)
    }


# ---------------------------- CONTENT ANALYSIS
def calculate_severity(profanity_result, hate_speech_result):
    
    if hate_speech_result["detected"]:
        return "CRITICAL"  
        # Hate speech is most severe
    elif profanity_result["detected"]:
        return "WARNING"   
        # Bad words are less severe | 
    return "CLEAN"

def get_violation_types(analysis):
    violations = []

    if analysis["profanity"]["detected"]:
        violations.append("profanity")

    hate = analysis["hate_speech"]

    if hate["detected"]:
        if hate["signals"]["slurs"]["detected"]:
            violations.append("hate_speech:slur")

        if hate["signals"]["group_dehumanization"]["detected"]:
            violations.append("hate_speech:dehumanization")

        if hate["signals"]["group_violence"]["detected"]:
            violations.append("hate_speech:violence")

        if hate["signals"]["hate_phrases"]["detected"]:
            violations.append("hate_speech:phrase")

    return violations


def analyze_content(text):

    profanity_result = check_profanity(text)
    hate_speech_result = check_hate_speech(text)
    
    return {
        "profanity": profanity_result,
        "hate_speech": hate_speech_result,
        "severity": calculate_severity(profanity_result, hate_speech_result)
    }


# ------------------------ VIOLATION MANAGEMENT

def get_violators_log():

    with open("../../hate_speech/datasets/violators.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_violators(violators):

    with open("../../hate_speech/datasets/violators.json", "w", encoding="utf-8") as f:
        json.dump(violators, f, indent=4)


def check_violator_exists(user_id, violators):

    return any(v["id"] == user_id for v in violators["violators"])


def add_violator(user_id, first_name, last_name, violation_type):

    violators = get_violators_log()
    
    violators["violators"].append({
        "id": user_id,
        "full_name": f"{first_name} {last_name}",
        "warnings": 1,
        "violations": [violation_type],
        "banned_until": None
    })
    
    save_violators(violators)


def update_violator(user_id, violation_type):

    violators = get_violators_log()
    warnings = 0
    
    for vltr in violators["violators"]:
        if vltr["id"] == user_id:
            vltr["warnings"] += 1
            vltr["violations"].append(violation_type)
            warnings = vltr["warnings"]
            break
    
    save_violators(violators)
    return warnings


def handle_violation(user_id, first_name, last_name, violation_type, severity):

    violators = get_violators_log()
    

    if not check_violator_exists(user_id, violators):
        add_violator(user_id, first_name, last_name, violation_type)
        return {"action": "warn", "warnings": 1}
    

    warnings = update_violator(user_id, violation_type)
    

    if severity == "CRITICAL":  # Hate speech
        if warnings >= 2:
            return {"action": "ban", "duration": timedelta(days=7)}
        else:
            return {"action": "mute", "duration": timedelta(hours=24)}
    
    elif severity == "WARNING":  # Bad words
        if warnings >= 3:
            return {"action": "mute", "duration": timedelta(hours=2)}
        else:
            return {"action": "warn", "warnings": warnings}
    
    return {"action": "warn", "warnings": warnings}


# ------------------------------------ MAIN MESSAGE HANDLER
def reply_message(received_message, user):
    
    analysis = analyze_content(received_message)
    
    # If none detected
    if analysis["severity"] == "CLEAN":
        # return f"✅ {user.full_name}: No violations detected."
        print(f"Received: {received_message}\nSeverity: CLEAN")
        return None

    lines = [f"Message analyzed for {user.full_name}"]
    lines.append(f"Severity: {analysis['severity']}")
    
    # Violation type
    # if analysis["hate_speech"]["detected"]:
       
    #     target_groups = analysis['hate_speech']['target_groups']
    #     violation_type = f"hate_speech:{','.join(target_groups)}"
    
    # else:
    #     violation_type = "profanity"

    # if analysis['profanity_matches']:
    if analysis['profanity']['detected']:
        lines.append(f"⚠️ Profanity detected: {analysis['profanity']['matched_words']}")


    hate = analysis["hate_speech"]
    if hate["detected"]:
        lines.append(f"🚫 Hate speech detected!")
        target_groups = hate.get("target_groups", [])
        if target_groups:
            lines.append(f"Target groups: {target_groups}")

        slurs_result = hate["signals"]["slurs"]
        if slurs_result["detected"]:
            lines.append(f"Slurs: {slurs_result['matches']}")

    # violation_type = analysis["violation_type"]
    if hate["detected"]:
        violation_type = "hate_speech"
    
    elif analysis['profanity']['detected']:
        violation_type = "profanity"
    
    else:
        violation_type = "unknown"
    
    # Violation Handling

    action = handle_violation(
        user.id,
        user.first_name,
        user.last_name,
        violation_type,
        analysis["severity"]
    )

    
    # Response
    # if action["action"] == "ban":
    #     return f"🚫 {user.first_name} {user.last_name} has been banned for {action['duration'].days} days for hate speech."
    
    
    if action["action"] == "mute":
        hours = int(action['duration'].total_seconds() / 3600)
        return f"🔇 {user.full_name} has been muted for {hours} hours."
    
    
    else:
        return f"⚠️ Warning {action['warnings']}/3: {user.full_name}"

    return "\n".join(lines)

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