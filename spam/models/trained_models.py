import os
import pickle
import hashlib
from collections import defaultdict, Counter
import csv
import re

base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "..", "datasets", "spam_messages.csv")
pickle_path = os.path.join(base_path, "..", "pickle_models","spam_models.pkl")
pickle_hash_path = pickle_path + ".sha256"  #to ensure file is not corrupted or whatsoever

spam_texts = []
ham_texts = []

# Preprocessing 
def char_escape(s):
    special_chars = ".^$*+?{}[]\\|()"
    return "".join("\\" + c if c in special_chars else c for c in s)

def normalize(text):
    text = text.lower()
    contractions = {
        "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is", "it's": "it is",
        "we're": "we are", "they're": "they are", "i've": "i have", "you've": "you have",
        "we've": "we have", "they've": "they have", "i'd": "i would", "you'd": "you would",
        "he'd": "he would", "she'd": "she would", "they'd": "they would", "i'll": "i will",
        "you'll": "you will", "he'll": "he will", "she'll": "she will", "we'll": "we will",
        "they'll": "they will", "don't": "do not", "doesn't": "does not", "didn't": "did not",
        "can't": "cannot", "couldn't": "could not", "won't": "will not", "wouldn't": "would not",
        "shouldn't": "should not", "isn't": "is not", "aren't": "are not", "wasn't": "was not",
        "weren't": "were not", "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
        "n't": " not", "'re": " are", "'s": " is", "'d": " would", "'ll": " will",
        "'ve": " have", "'m": " am"
    }
    for contraction, expanded in contractions.items():
        text = re.sub(rf"\b{char_escape(contraction)}\b", expanded, text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def tokenize(text):
    return normalize(text).split()

def generate_ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

#Model building
def ngram_model(texts, n=3):
    all_tokens = []
    ngrams = []
    bigrams = []

    for text in texts:
        tokens = tokenize(text)
        
        for token in tokens:
            all_tokens.append(token)
        
        for ngram in generate_ngrams(tokens, n):
            ngrams.append(ngram)
        
        for bigram in generate_ngrams(tokens, 2):
            bigrams.append(bigram)

    trigram_freq = defaultdict(Counter)
    for gram in ngrams:
        prefix = gram[:-1]
        next_word = gram[-1]
        trigram_freq[prefix][next_word] += 1

    bigram_freq = defaultdict(Counter)
    for bigram in bigrams:
        prefix = bigram[:-1]
        next_word = bigram[-1]
        bigram_freq[prefix][next_word] += 1

    vocab = set(all_tokens)
    unigram_model = Counter(all_tokens)

    return trigram_freq, bigram_freq, len(vocab), unigram_model, sum(unigram_model.values())

# Load CSV
def load_dataset():
    spam_texts.clear()
    ham_texts.clear()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message = row.get("message", "").strip()
            label = row.get("label", "").strip().lower()
            if message:
                if label == "spam":
                    spam_texts.append(message)
                elif label == "ham":
                    ham_texts.append(message)

#Load Models
def save_models(spam_model, spam_bigram_model, spam_vocab_size, spam_unigrams, spam_total_unigrams,
                ham_model, ham_bigram_model, ham_vocab_size, ham_unigrams, ham_total_unigrams):
    with open(pickle_path, "wb") as f:
        pickle.dump((spam_model, spam_bigram_model, spam_vocab_size, spam_unigrams, spam_total_unigrams,
                     ham_model, ham_bigram_model, ham_vocab_size, ham_unigrams, ham_total_unigrams,
                     spam_texts, ham_texts), f)

    with open(pickle_path, "rb") as f:
        data = f.read()
    hash_digest = hashlib.sha256(data).hexdigest()
    with open(pickle_hash_path, "w") as f:
        f.write(hash_digest)

def load_models():
    if os.path.exists(pickle_path) and os.path.exists(pickle_hash_path):
        # Verify hash first
        with open(pickle_path, "rb") as f:
            data = f.read()
        computed_hash = hashlib.sha256(data).hexdigest()
        with open(pickle_hash_path, "r") as f:
            saved_hash = f.read()
        if computed_hash != saved_hash:
            print("!!! Pickle file integrity check failed! The file may be corrupted huhu.")
            return None


        return pickle.loads(data)
    return None
