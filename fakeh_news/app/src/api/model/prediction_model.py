
import math

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from app.preProcessing.preprocessing import Preprocessing
from post_extraction import PostExtractor
from app.utils.file_utils import File_Utility


class PredictionModel:
    
    def __init__(self):
        print("Model Initialized...")
        self.preprocessing = Preprocessing()
        self.extractor = PostExtractor()
        self.file_utility = File_Utility()
        
        self.trainedData_path = "src/files/trained_dataset.pkl"
        self.verifiedSources_path = "src/files/sources.txt"
        self.trained_data= self.file_utility.read_pickle_file(self.trainedData_path)
        self.sources = self.file_utility.read_file(self.verifiedSources_path)
        
        
    def tokenize_input(self, user_input, token_list):
            
        token = self.preprocessing.tokenize(user_input)
    
        return token
    
    def prediction(self, text, linksource = None):
        probab_score_dict = self.trained_data
        token_list=[]
        
        print("GOT IN THE MODEL: ", linksource)
        # print("INPUT: ", text, "\n")
        
        
        score = {}
        real_boost = 0  
        tokenize = self.tokenize_input(text, token_list)
        if linksource is not None:
            extract_source = self.preprocessing.process_links(linksource)
        
            print("SOURCE: ", extract_source)
            
            # print("SOURCES:", self.sources)
            
            if extract_source in self.sources:
                
                real_boost += 100
                
            
            

        for key, values in probab_score_dict.items():
            if not isinstance(values, dict):  
                continue

            total_score = 0
            print(f"n\Class {key}: ")
            for token in tokenize:
                token_score = values["TOKENS"].get(token, 0)
                total_score += token_score
                
                # print(f"  Token '{token}' => {token_score}")
                
            if key == "1":
                total_score += real_boost  


                

            score[key] = total_score
            
            print(f"Total score for class {key}: {total_score}")

        prediction = max(score, key=score.get)
        # print(f"Final prediction: {prediction}")
        
        
        max_score = max(score.values())  # para hindi mag-underflow
        exp_scores = {k: math.exp(v - max_score) for k, v in score.items()}
        total = sum(exp_scores.values())

        if total == 0:  # safeguard
            probs = {k: 0 for k in score}
        else:
            probs = {k: exp_scores[k] / total for k in exp_scores}
        
        final ={}
            
            
        fake_result={}
        fake_result["score"]= probs['0']
        fake_result["percentage"] = probs['0'] * 100
        
        final["fake"] = fake_result
        
        real_result = {}
        real_result["score"] = probs['1']
        real_result["percentage"] = probs['1'] * 100
        
        final["real"] = real_result

        percentage = {}
        for label, p in probs.items():
            label_name = "Fake" if label == "0" else "Real"
            # print(f"Probability {label_name} ({label}): {p:.6f} ({p*100:.2f}%)")
            
            
            

        prediction = max(probs, key=probs.get)
        label_name = "Fake" if prediction == "0" else "Real"
        
        
        
       
        # print(f"Final prediction: {label_name} ({prediction})")

        return prediction,label_name, text ,final
    
    def extract_and_predict(self, link:str):
        post = self.extractor.extract_post(link)
        if not post:
            raise ValueError("Failed to extract from link")
        
        text = f"{[post.get('title', '')]}\n{post.get('body', '')}"
        return self.prediction(text)
            
        
#     def main(self):
            
#         token_list = []
        
#         t = "trump says no more pageants"
#         news = 'The Philippines protested on Thursday China’s announcement that it would establish a “nature reserve” at Bajo de Masinloc (Scarborough) Shoal, which is a violation of international law because it is located within Manila’s exclusive economic and maritime zone. “Bajo de Masinloc is a longstanding and integral part of the Philippines over which it has sovereignty and jurisdiction. The Philippines likewise has the exclusive authority to establish environmental protection areas over its territory and relevant maritime zones,” the Department of Foreign Affairs (DFA) said in a statement. “The Philippines will be issuing a formal diplomatic protest against this illegitimate and unlawful action by China as it clearly infringes upon the rights and interests of the Philippines in accordance with international law,” it added.'
#         news2 = 'China recently approved the establishment of a national nature reserve at Scarborough Shoal, a disputed reef located within the Philippines’ exclusive economic zone. Philippine officials said they lodged a diplomatic protest, and fishermen expressed concern that the move could further restrict their access to traditional fishing grounds. Experts noted that the area has been a flashpoint in the South China Sea for over a decade.However, viral social media posts are now claiming that “all Filipinos will be banned from entering the South China Sea starting next week” and that “any fisherman caught near Scarborough Shoal will be taken to Beijing and jailed.” Authorities clarified that these claims are false and misleading. While tensions remain, there has been no official policy announcing such sweeping restrictions'
#         fn= "A viral post circulating on social media claims that a small vendor in Laguna has been selling a homemade “mango leaf tea” that reportedly cures Type 2 diabetes within seven days. The post includes before-and-after photos of alleged patients, a short testimonial video, and a scanned “certificate” that looks like it came from a private clinic. The vendor is quoted as saying the recipe was passed down through generations and that patients only need to drink the tea three times daily and stop taking prescribed medication."
#         predict = self.prediction(t)
            
#         print(predict[0])
            
            
# app= App()
# app.main()
        
        