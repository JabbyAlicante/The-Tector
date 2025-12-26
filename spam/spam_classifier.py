import math
from models.trained_models import (
    load_dataset, ngram_model, save_models, load_models,
    spam_texts, ham_texts
)

print(" Loading Spam Detector:DD...")

models = load_models()
if models:
    print("Models loaded from pickle!")
    (spam_model, spam_bigram_model, spam_vocab_size, spam_unigrams, spam_total_unigrams,
     ham_model, ham_bigram_model, ham_vocab_size, ham_unigrams, ham_total_unigrams,
     spam_texts, ham_texts) = models
else:
    #if di pa nakakapagtrain and di nasave sa pickle mag train muna na masave sa pickle
    print("🛠 Training from CSV...")
    load_dataset()
    spam_model, spam_bigram_model, spam_vocab_size, spam_unigrams, spam_total_unigrams = ngram_model(spam_texts)
    ham_model, ham_bigram_model, ham_vocab_size, ham_unigrams, ham_total_unigrams = ngram_model(ham_texts)

    save_models(spam_model, spam_bigram_model, spam_vocab_size, spam_unigrams, spam_total_unigrams,
                ham_model, ham_bigram_model, ham_vocab_size, ham_unigrams, ham_total_unigrams)
    print("Models saved to pickle.")

# Classifier
def compute_log_probability(message, trigram_model, vocab_size, unigram_model, bigram_model, total_unigrams, show_logs=False):
    from models.trained_models import tokenize
    tokens = tokenize(message)
    if len(tokens) < 3:
        return -99.99
    total_log_prob = 0.0
    λ3, λ2, λ1 = 0.6, 0.3, 0.1
    
    if show_logs:
        print(f"\n🔍 Analyzing message: '{message}'")
        print("📊 Interpolated N-gram Match Results:")

    for i in range(len(tokens) - 2):
        w1, w2, w3 = tokens[i], tokens[i+1], tokens[i+2]
        trigram_prefix = (w1, w2)
        bigram_prefix = (w2,)

        # loop over trigrams
        trigram_count = trigram_model[trigram_prefix][w3] # computes hhow often it appears
        trigram_total = sum(trigram_model[trigram_prefix].values()) # gets the total count
        p_trigram = (trigram_count + 1) / (trigram_total + vocab_size) if trigram_total > 0 else 0 #the use laplace to avoid zero

        # loop over bigrams
        bigram_count = bigram_model[bigram_prefix][w3]
        bigram_total = sum(bigram_model[bigram_prefix].values())
        p_bigram = (bigram_count + 1) / (bigram_total + vocab_size) if bigram_total > 0 else 0

        # loop over unigrams
        unigram_count = unigram_model[w3]
        p_unigram = (unigram_count + 1) / (total_unigrams + vocab_size)

        # Interpolation computation
        interpolated_prob = λ3 * p_trigram + λ2 * p_bigram + λ1 * p_unigram
        total_log_prob += math.log(interpolated_prob)

        if show_logs:
            print(f"   {w1} {w2} ➜ {w3} | P3={p_trigram:.5f}, P2={p_bigram:.5f}, P1={p_unigram:.5f} → Interp={interpolated_prob:.5f}")

    return total_log_prob

def absolute(x):
    return x if x >= 0 else -x

def classify(message, threshold=-99.99, show_logs=True):
    from models.trained_models import normalize
    norm_msg = normalize(message)

    # Check for direct matches in training data
    for msg in ham_texts:
        if norm_msg in msg:
            if show_logs:
                print("🔁 Partial match found in HAM training set.")
                print(f"   📄 Matching HAM message: {msg}")
            return "ham"

    for msg in spam_texts:
        if norm_msg in msg:
            if show_logs:
                print("🔁 Partial match found in SPAM training set.")
                print(f"   📄 Matching SPAM message: {msg}")
            return "spam"

    # Compute log probabilities
    spam_score = compute_log_probability(message, spam_model, spam_vocab_size, spam_unigrams, spam_bigram_model, spam_total_unigrams, show_logs=False)
    ham_score  = compute_log_probability(message, ham_model, ham_vocab_size, ham_unigrams, ham_bigram_model, ham_total_unigrams, show_logs=False)

    print("\n📊 Log Probabilities:")
    print(f"   SPAM: {spam_score}")
    print(f"   HAM : {ham_score}")

    # Low support fallback
    if spam_score < threshold and ham_score < threshold:
        print("⚠️ Low support for both categories.")
        if absolute(spam_score - ham_score) > 10:
            prediction = "spam" if spam_score > ham_score else "ham"
            print(f"Choosing based on better score: {prediction.upper()}")
            return prediction
        else:
            print(" Scores are too close. Marking as UNKNOWN.")
            return "unknown"

    confidence = absolute(spam_score - ham_score)
    print(f"🎯 Confidence: {confidence:.2f}")

    if show_logs:
        print("\n🔍 Showing best prediction breakdown:")
        if spam_score > ham_score:
            compute_log_probability(message, spam_model, spam_vocab_size, spam_unigrams, spam_bigram_model, spam_total_unigrams, show_logs=True)
        else:
            compute_log_probability(message, ham_model, ham_vocab_size, ham_unigrams, ham_bigram_model, ham_total_unigrams, show_logs=True)

    if spam_score == ham_score:
        return "unknown"
    return "spam" if spam_score > ham_score else "ham"
def classify_message(message_text):
    #w/o printing the logs import it to the bot
    return classify(message_text, show_logs=False)

if __name__ == "__main__":
    print("\n--- 📨 Spam Detector is Ready!!! ---")
    print("Type a message to check if it's spam or ham.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("📝 Your message: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!Ciao~~~ 👋")
            break
        prediction = classify(user_input, show_logs=True)
        print(f"\n🔎 Final Prediction: {prediction.upper()}\n{'-'*50}")