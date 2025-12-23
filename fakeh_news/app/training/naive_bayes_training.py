import sys, os
import math
import re
import random
import pickle
import pprint
import time

# ADD WEIGHT FOR THE SOURCE IF ITS FROM A LEGIT SOURCE REAL UP IF NOT FAKE UP


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preProcessing.preprocessing import Preprocessing
from utils.file_utils import File_Utility


class Training:
    
    def __init__(self):
        
        self.preprocessing = Preprocessing(neg_scope=3)
        self.file_utility = File_Utility()
        
        self.train_path = "../dataset/train.pkl"
        self.test_path = "./dataset/test.pkl"
        
        self.train = self.file_utility.read_pickle_file(self.train_path)
        
        
    def tokenize_docs(self, docs, token_list):
        
        print("TOKENIZING..")
         
        
        
        for i in docs:
            
            # print(i)
            content = i[1]
            label = i[0]
            # print(label)
            
            if label not in ['0', '1']:
                label = '0'
                
            
            
            token = self.preprocessing.tokenize(content)
            
            modified_train = (label, token)
            
            token_list.append(modified_train)
        return token_list
            
            
 
    def get_doc_bagOfwords(self, tlist,vocab_size,class_counter, class_word_counter):
        
        print("BAG OF WORDS")
        
        for doc in tlist:
            tokens = doc[1]
            label = doc[0]
            
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
        
        print("TRAINING RN...")
     
        # P(c|d) = P(d|c)*P(c) / P(d)
        
        probab_score={}
        
        docs_count = sum(class_counter.values())
        
        probab_score["docs_total"]= docs_count
        
        vocab_size = len(vocab_size)

        # print(vocab_size)  
        probab_score["__VOCAB_SIZE__"]= vocab_size  
        print("DOCS COUNT: ", docs_count)

        
        for label in class_counter:
            
            probab_score[label] = {} #P(c|d)
            probab_score[label]["TOKENS"]={}
            # prior = class_counter[label]/docs_count #P(c)
            prior = math.log(class_counter[label]/docs_count) #P(c)
            
            print("NB PRIOR: ", prior)
            
            probab_score[label]["__PRIOR__"] = prior
            
            class_total_tokens= sum(class_word_counter[label].values())
            probab_score[label]["class_total_tokens"] = class_total_tokens
 
            normalizer = class_total_tokens + vocab_size
           
            for docs in tokens:
                doc = docs[1]
                
                for token in doc:
                    l = class_word_counter[label].get(token,0) + 1
                    # likelihood = (class_word_counter[label].get(token,0) + 1) / normalizer
                    likelihood = math.log((class_word_counter[label].get(token,0) + 1))
                    if token.startswith("PERSON_NAME_"):
                        if label == "1":  
                            likelihood *= 0.3 
                        elif label == "0": 
                            likelihood = 0  # fake

                    elif token.startswith("NOT_PERSON_NAME_"):
                        if label == "1":  
                            likelihood *= 3  
                        elif label == "0":
                            likelihood *= 0

                                        
                    prob = prior + likelihood
                    
                    probab_score[label]["TOKENS"][token]= prob
                    
                # probab_score[label] = probab
                    
                    # print(f"{label}=={token}--{likelihood} ({l}/{normalizer})")
                    
        print("MAKING FILE")
        probab_score_pkl = self.file_utility.write_pickle_file(probab_score,"trained_dataset.pkl")
        # self.file_utility.write_file(class_word_counter[label].values(), "class_word_counter.txt")
        
        return probab_score_pkl
    

    
        
        
        
    def main(self):
        
        start_time = time.time() 
        
        token_list= []
        ctoken_list = []
        vocab_size = set() #unique words
        class_counter={} #count of docs each class
        class_word_counter={} #bow
        
        
        tokens = self.tokenize_docs(self.train, token_list)
        
        # print(tokens)
        
        self.file_utility.write_file(tokens ,"token.txt")
        vs, c_counter, cw_counter= self.get_doc_bagOfwords(tokens, vocab_size,class_counter, class_word_counter)
        print(c_counter)
        # self.file_utility.write_file(self.train, "testtrain.txt")
        
        naive_bayes= self.train_naive_bayes(tokens,vs, c_counter, cw_counter)
        # print(naive_bayes)
        
        t=self.file_utility.read_pickle_file("trained_dataset.pkl")
        
        with open("output.txt", "w", encoding="utf-8") as f:
            pprint.pprint(t, stream=f)
            
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"\nExecution time: {elapsed:.2f} seconds")

        
        
        
        
    
    
        
        
        
        
        
        
train = Training()    
train.main()    
