import math
import re
import random




#THIS AIN'T RIGHT YET(MAYBE IT IS BUT ITS NOT WHAT IM SUPPOSE TO DO)
#TO DO:
#ACTUALLY try to train save it then compare the trained data to the user input
#USE NGRAM(test if its okay)
#TRY THE JS + PY
#OPEN LINKS

real_docs = [
    ("The government announced new policies to support small businesses.", "real"),
    ("Scientists discovered a new exoplanet orbiting a nearby star.", "real"),
    ("The stock market showed modest growth this week.", "real"),
    ("Local authorities are investigating a fire that broke out downtown.", "real"),
    ("The city council approved funding for a new hospital.", "real"),
    ("Researchers published a study on climate change effects in Asia.", "real"),
    ("The president met with foreign leaders to discuss trade.", "real"),
    ("A new vaccine has been approved after successful trials.", "real"),
    ("The mayor launched a campaign to improve public transport.", "real"),
    ("The economy grew by 2 percent in the last quarter.", "real"),
    ("Teachers across the country are demanding higher pay.", "real"),
    ("The championship game ended with a dramatic overtime goal.", "real"),
    ("A rare species of bird was spotted in the national park.", "real"),
    ("The university opened a new research center for technology.", "real"),
    ("The health department issued warnings about rising flu cases.", "real"),
    ("The train line will expand to three more towns next year.", "real"),
    ("Police arrested two suspects in connection with the robbery.", "real"),
    ("The museum unveiled its latest art exhibition.", "real"),
    ("The prime minister gave a speech on economic reform.", "real"),
    ("Scientists reported progress in renewable energy technology.", "real")
]

fake_docs = [
    ("Aliens landed in the desert and spoke to local farmers.", "fake"),
    ("Drinking only coffee for a week cures all diseases.", "fake"),
    ("A man turned invisible after eating a rare fruit.", "fake"),
    ("Secret government tunnels lead directly to the moon.", "fake"),
    ("Scientists confirm time travel will be available next year.", "fake"),
    ("Eating chocolate three times a day makes you live forever.", "fake"),
    ("A celebrity adopted a dragon as a pet.", "fake"),
    ("Newly found crystal can control people’s thoughts.", "fake"),
    ("The world will end on the 13th of next month.", "fake"),
    ("Dinosaurs still live in a hidden island in the Pacific.", "fake"),
    ("A smartphone app can make you fly for ten minutes.", "fake"),
    ("The government is hiding proof of mermaids in the ocean.", "fake"),
    ("Magical herbs discovered in the mountains heal any illness.", "fake"),
    ("Aliens are controlling weather patterns around the globe.", "fake"),
    ("The Eiffel Tower secretly produces free electricity.", "fake"),
    ("A new mineral allows humans to breathe underwater.", "fake"),
    ("Ancient ruins show humans were once 20 feet tall.", "fake"),
    ("Secret potion discovered that grants eternal youth.", "fake"),
    ("The moon is actually hollow and filled with gold.", "fake"),
    ("Robots have already taken over a hidden city underground.", "fake")
]


rpercentage = math.ceil(len(real_docs) * 0.2)
fpercentage = math.ceil(len(fake_docs) * 0.2)

real_test= real_docs[:rpercentage]
real_train = real_docs[rpercentage:]


fake_test = fake_docs[:fpercentage]
fake_train = fake_docs[fpercentage:]


train = real_train + fake_train
test= real_test + fake_test



random.shuffle(train)
random.shuffle(test)

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation but keep spaces
    return text.strip()


def tokenize(text, special_tokens = False):
    tokens = re.split("[- ]", text)
 

    if special_tokens:
        tokens = ["<s>"] + list(map(normalize, tokens)) + ["</s>"]

    return tokens


def train_naive_bayes(docs):
    vocab_size= set()
    
    class_counter = {}
    class_word_counter = {}
    
    
    
    for doc, label in docs:
       
        tokens = tokenize(doc)
       
        vocab_size.update(tokens)
       
        if label not in class_counter:
           class_counter[label] = 0
           class_word_counter[label] = {}
           
        class_counter[label] += 1
        
        for token in tokens:
            class_word_counter[label][token] = class_word_counter[label].get(token, 0) + 1 #BOW
            
    return class_counter, class_word_counter, len(vocab_size)


def predict(text, class_counts, class_word_counts, vocab_size):
    print(vocab_size)
    
    tokens = tokenize(text)
    total_docs = sum(class_counts.values())
    scores={}
    
    print("TOKEN", tokens)
    
    
    for label in class_counts.keys():
        prior = math.log(class_counts[label]/total_docs)
        print(f"PRIOR: ({label}): log({class_counts[label]} / {total_docs}) = {prior}")

        for token in tokens:
            print("T:", token)
            token_count = class_word_counts[label].get(token, 0)
            total_tokens = sum(class_word_counts[label].values())
            print(label, total_tokens)
            
            likelihood = math.log((token_count + 1) / (total_tokens + vocab_size))
            print(f"---> {token}: log({token_count + 1} / {total_tokens + vocab_size}) = {likelihood}")

            
            prob= prior + likelihood
            
        print(f"{label} at {prior}")
        scores[label] = prob
        
    return max(scores, key = scores.get)


        
            


def main(train, test):
    # WILL SHOW TRAINED DATA
    class_counts, class_word_counts, vocab_size= train_naive_bayes(train)
    
    for i in train:
        n = tokenize(i[0])
        print(n)
        prediction = predict(i[0], class_counts, class_word_counts, vocab_size)
        
    print(prediction)
        
        
    #TEST
    
    
    # class_counts, class_word_counts, vocab_size = train_naive_bayes(train)
    
  
    # score = 0
    # for doc in test:
    #     content, label = doc
    #     if predict(content, class_counts, class_word_counts, vocab_size) == label:
    #         score += 1
    
    # print("Accuracy Score:", score / len(test)) 
        
        
        
     
     
     
        
        
main(train,test)

# print(train_naive_bayes(train))


