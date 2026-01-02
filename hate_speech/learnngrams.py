import re
import math
from collections import defaultdict, Counter

reviews = [
    "Absolutely loved it! Exceeded my expectations.",
    "Fantastic service and great attention to detail.",
    "I will definitely come back again.",
    "Five stars—couldn’t be happier!",
    "Everything worked perfectly from start to finish.",
    "It was a smooth and enjoyable experience.",
    "The product quality is top-notch.",
    "I’m really impressed with the level of professionalism.",
    "Clean, efficient, and reliable.",
    "Excellent value for money.",
    "The customer support team was very helpful.",
    "Quick delivery and the item matched the description.",
    "The interface was intuitive and easy to use.",
    "I’ve already recommended it to my friends.",
    "High quality and affordable.",
    "Surprisingly good, exceeded all my expectations.",
    "Super friendly staff and fast response times.",
    "Setup was easy and everything worked immediately.",
    "The packaging was beautiful and secure.",
    "Very satisfied with my purchase.",
    "This was one of the best decisions I’ve made!",
    "I felt well taken care of throughout the process.",
    "The colors were vibrant and exactly as pictured.",
    "Reliable and consistent every single time.",
    "I love it—will definitely buy again.",
    "Completely disappointed—nothing worked.",
    "Terrible experience from start to finish.",
    "Would not recommend to anyone.",
    "Poor quality and overpriced.",
    "I had high hopes but it failed miserably.",
    "Customer service was rude and unhelpful.",
    "The instructions were unclear and confusing.",
    "It broke within the first week.",
    "Slow delivery and bad packaging.",
    "Not worth the money at all.",
    "App kept crashing every few minutes.",
    "The item looked nothing like the photos.",
    "Misleading description and poor build quality.",
    "Very frustrating experience overall.",
    "It didn’t meet even basic expectations.",
    "I had to return it the same day I got it.",
    "Overhyped and underdelivered.",
    "I regret making this purchase.",
    "There were bugs they never fixed.",
    "The support team didn’t respond to my emails.",
    "It’s just a waste of time and money.",
    "Looks cheap and feels worse.",
    "The service was shockingly bad.",
    "Error messages every time I tried to use it.",
    "Nothing worked as advertised.",
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown bear sleeps.",
    "The quick brown fox sleeps",
]

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
    if special_tokens:
        tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]
    return tokens

# print(normalize(reviews))


def ngram(tokens, n = 3):
    ngrams = Counter()

    for i in range(len(tokens)):
        grams = tokens[i] if n == 1 else tuple(tokens[i:i+n])
        ngrams[grams] += 1

    return ngrams

# def ngram(tokens, n=3):
#     ngrams = Counter()

#     for i in range(len(tokens) - n + 1):
#         if n == 1:
#             grams = tokens[i]   # keep as string
#         else:
#             grams = tuple(tokens[i:i+n])
#         ngrams[grams] += 1

#     return ngrams

tokens = []

for review in reviews:
    tokens += tokenize(review)

for i in tokens:
    print(i)

trigrams = ngram(tokens)
bigrams = ngram(tokens, 2)
unigrams = ngram(tokens, 1)

vocab_size = (len(set(tokens)))

# (trigrams, bigrams, unigrams)
# print(f"tri: {trigrams}")
# print(f"bi: {bigrams}")
# print(f"uni: {unigrams}")

def create_freq_table(grams, n = 3):
    freq = defaultdict(Counter) if n > 1 else Counter(grams)

    if n == 1:
        return freq
    
    for gram in grams:
        prefix = tuple(gram[:-1])
        next_word = gram[-1]
        # print(next_word)

        freq[prefix][next_word] += 1

    # print(freq)
    return freq

trigram_freq = create_freq_table(trigrams)
bigrams_freq = create_freq_table(bigrams, 2)
unigrams_freq = create_freq_table(unigrams, 1)

# print(trigram_freq)

# def predict_next(word, model, top_k=3):
#     if (isinstance(model, Counter)):
#         return model.most_common(top_k)
    
#     next_words = model[tuple(word.lower().split(" "))]

#     return next_words.most_common(top_k)

# # predict_next("quick brown", trigram_freq)
# # predict_next("quick", bigrams_freq)
# # predict_next("quick", unigrams_freq)


# print(predict_next("quick brown", trigram_freq))
# print(predict_next("quick", bigrams_freq))
# print(predict_next("quick", unigrams_freq))

def predict_next(word, model, vocab_size, top_k=3):
    if (isinstance(model, Counter)):
        total = sum(model.values())
        probabillities = [
            (w, math.log((count + 1) / (total + vocab_size)))
            for w, count in model.items()
        ]

        probabillities.sort(key=lambda x: x[1], reverse=True)
        return probabillities[:top_k]
    
    word = tuple(word.lower().split(" "))
    if word not in model:
        return []
    next_words = model[word]
    total = sum(next_words.values())

    probabillities = [(w, math.log((count + 1) / (total + vocab_size))) for w, count in next_words.items()]
    probabillities.sort(key=lambda x: x[1], reverse=True)

    return probabillities[:top_k]

trigram_candidates = predict_next("the quick", trigram_freq, vocab_size)
# print(trigram_candidates)
bigram_candidates = predict_next("quick", bigrams_freq, vocab_size)
# print(bigram_candidates)
unigram_candidates = predict_next("lazy", unigrams_freq, vocab_size)
# print(unigram_candidates)

def interpolate(w1, w2, w3, weights = (0.1, 0.3, 0.6)):
    # P(w₃ | w₁, w₂) = λ₁ × P(w₃) + λ₂ × P(w₃ | w₂) + λ₃ × P(w₃ | w₁, w₂)

    # P(w₃)
    prob1 = unigrams.get(w3) / sum(unigrams.values()) if w3 in unigrams else 0

    # P(w₃ | w₂)
    prob2 = bigrams.get((w2, w3)) / unigrams.get(w2) if (w2, w3) in bigrams else 0
    # prob2 = bigrams.get((w2, w3)) / unigrams.get(w2) if (w2, w3) in bigrams else 0


    # P(w₃ | w₁, w₂)
    prob3 = trigrams.get((w1, w2, w3)) / bigrams.get((w1, w2)) if (w1, w2, w3) in trigrams else 0

    return (prob1 * weights[0]) + (prob2 * weights[1]) + (prob3 * weights[2])

def predict_with_interpolation(text):
    parsed = tokenize(text, False)
    w1, w2 = parsed[-2:]

    probabilities = Counter()

    for token in set(tokens):
        probabilities[token] = interpolate(w1, w2, token)

    return probabilities.most_common(5)

print(predict_with_interpolation("the quick"))

def perplexity(sentence, model):
    tokens = tokenize(sentence)
    bigrams = ngram(tokens)

    total_prob = 1.0
    word_count = len(tokens)

    for bigram in bigrams:
        prefix = tuple(bigram[:-1])
        total = 0
        count = 0
        prob = 1e-6

        if prefix in model:
            total = sum(model[prefix].values())
            count = model[prefix].get(bigram[-1], 0)
            prob = (count + 1) / (total + 1)

        total_prob *= prob

    return total_prob ** -(1 / word_count)

# perplexity("wqasdasd asdasds asd", trigram_freq)
# perplexity("the quick brown fox", trigram_freq)

print(f"Gibberish: {perplexity('wqasdasd asdasds asd', trigram_freq)}")
print(f"Sentence {perplexity('the quick brown fox', trigram_freq)}")




# for i in reviews:
#   print(tokenize(i))