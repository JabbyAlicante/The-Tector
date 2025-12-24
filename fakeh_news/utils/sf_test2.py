import sys, os
import math
import re
import random
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.preProcessing.preprocessing import Preprocessing

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
    ("Marshalls landed in the desert and spoke to local fisher.", "fake"),
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


class Test_Train:
    
    def __init__(self):
        self.preprocess = Preprocessing()
       
        
        self.train = train
        self.test = test
        
        
        
        
    def write_pickle_file(self,file, file_name):
        
        
        with open(file_name, "ab") as pf:
            pickle.dump(file, pf)
            
        return file_name
    
    def read_pickle_file(self,file_name):
        with open (file_name, "rb") as pf:
            
            dataset = pickle.load(pf)
            
        return dataset
            
           
        
        
        
        
    def tokenize_docs(self,docs, tlist):
        
        for i in docs:
          
            token = self.preprocess.tokenize(i[0])
            modified_token = (token, i[1])
            tlist.append(modified_token)
        return tlist
    def tokenize_classification(self, user_input, tokenlist):
        # for i in user_input:
        token = self.preprocess.tokenize(user_input)
        # tokenlist.append(token)
        return token
    
    
    def get_doc_bagOfwords(self, tlist,vocab_size,class_counter, class_word_counter):
        
        for doc in tlist:
            tokens = doc[0]
            label = doc[1]
            
            vocab_size.update(tokens)
           
            if label not in class_counter:
               class_counter[label] = 0 
               class_word_counter[label] = {}
            class_counter[label] +=1
            
            for token in tokens:
                class_word_counter[label][token] = class_word_counter[label].get(token, 0) +1
            
                
           
        # print(class_counter)
        return vocab_size,class_counter,class_word_counter
    
    
    def train_naive_bayes(self,tokens ,vocab_size, class_counter, class_word_counter):
     
        # P(c|d) = P(d|c)*P(c) / P(d)
        
        probab_score={}
        
        docs_count = sum(class_counter.values())
        
        vocab_size = len(vocab_size)

        print(vocab_size)        
        print("DOCS COUNT: ", docs_count)
   
        
        for label in class_counter:
            probab_score[label] = {} #P(c|d)
            
            # prior = class_counter[label]/docs_count #P(c)
            prior = math.log(class_counter[label]/docs_count) #P(c)
            print("NB PRIOR: ", prior)
            probab_score[label]["__PRIOR__"] = prior
            
            
            class_total_tokens= sum(class_word_counter[label].values())
 
            normalizer = class_total_tokens + vocab_size
           
            for docs in tokens:
                doc = docs[0]
                
                for token in doc:
                    l = class_word_counter[label].get(token,0) + 1
                    # likelihood = (class_word_counter[label].get(token,0) + 1) / normalizer
                    likelihood = math.log((class_word_counter[label].get(token,0) + 1) / normalizer)
                    # print(normalizer)
                    
                    probab_score[label][token] = likelihood
                    
                # probab_score[label] = probab
                    
                    # print(f"{label}=={token}--{likelihood} ({l}/{normalizer})")
        probab_score_pkl = self.write_pickle_file(probab_score,"probab_score_ds.pkl")
        return probab_score_pkl
    
    














                    
    def clasification(self,text, token_list, probab_score_dict):
        # print(probab_score_dict)
       
        score={}
        tokenize = self.tokenize_classification(text,token_list)
        print(tokenize)
        
        
        # l = probab_score_dict[label]
        # print(l)
        
        for key, values in probab_score_dict.items():
            # classify = probab_score_dict['real'].get()
            s = values["__PRIOR__"]
            
            print("CLASSIFICATION: ",key,s)
            
        
            for i in tokenize:
                likelihood = probab_score_dict[key].get(i, 0)
                print(key,i,likelihood,"\n")
                
                s += likelihood
            
            score[key] = s
        
            print(score)
        exp_scores = {label: math.exp(s) for label, s in score.items()}
        total = sum(exp_scores.values())
        probs = {label: exp_scores[label] / total for label in exp_scores}


        for label, p in probs.items():
            print(f"Probability {label}: {p:.6f} ({p*100:.2f}%)")

     
        prediction = max(probs, key=probs.get)
        return prediction, probs
                        
                        
                        
                        
                        
                
                    

                    
            
                
                
            
            
            
            
            
            
        
        
        
        
    def main(self):
        token_list= []
        ctoken_list = []
        vocab_size = set() #unique words
        class_counter={} #count of docs each class
        class_word_counter={} #bow
        
        tokens = self.tokenize_docs(self.train, token_list)
        
        vs, c_counter, cw_counter= self.get_doc_bagOfwords(tokens, vocab_size,class_counter, class_word_counter)

        naive_bayes= self.train_naive_bayes(tokens,vs, c_counter, cw_counter)
        print(naive_bayes)
        
        print(self.read_pickle_file(naive_bayes))
        
        
        
        # classification = self.clasification("eiffel tower is made by aliens in national park", ctoken_list, naive_bayes)
        
        
        
    
    
        
        
              
        
t = Test_Train() 
t.main()

