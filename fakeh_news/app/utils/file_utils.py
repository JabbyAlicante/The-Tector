import pickle

import os
import ast



class File_Utility:
    
    def __init__(self):
        print("File Utility Initialized.")
    
    def write_file(self, file, file_name):
    
        with open(file_name, "a") as f:
            for doc in file:
                f.write(f"{doc}\n")
                
        return file_name
    
    def read_file(self, file_path):
        data = []
        with open(file_path, "r") as f:
            for i in f:
                
                
                data.append(i.strip())
        
            
        return data
    
    def read_raw_file(self, file_path):
       
        file_path = os.path.normpath(file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        docs = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                parts = s.split(maxsplit=1)
                if len(parts) == 2:
                    label, content = parts
                else:
                    label = parts[0]
                    content = ""
                    
                # doc = f"{label}, {content}"
                docs.append((label, content))
        return docs

    def write_modified_file(self, docs, file_path, mode="w"):
        file_path = os.path.normpath(file_path)
        dirname = os.path.dirname(file_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        with open(file_path, mode, encoding="utf-8") as f:
            for item in docs:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    label, content = item[0], item[1]
                    # write as tuple with quotes around content/label
                    f.write(f"({repr(content)}, {repr(label)}),\n")
                elif isinstance(item, str):
                    f.write(repr(item) + "\n")
                else:
                    f.write(repr(item) + "\n")
        return True


            
        
        
    
    def write_pickle_file(self,file, file_name):
        
        
        with open(file_name, "ab") as pf:
            pickle.dump(file, pf)
            
        return file_name
    
    def read_pickle_file(self,file_name):
        with open (file_name, "rb") as pf:
            
            dataset = pickle.load(pf)
            
        return dataset
    

    def load_multiwords(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        
        multi_words = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    multi_words.append(word)
        
        return multi_words
    
    def load_stopwords(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")
        
        stopwords = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.append(word)
        
        return stopwords
            

# fake_docs ={}

# fake_docs=[("Aliens landed in the desert and spoke to local farmers.", "fake"),
#     ("Marshalls landed in the desert and spoke to local fisher.", "fake"),
#     ("Drinking only coffee for a week cures all diseases.", "fake"),
#     ("A man turned invisible after eating a rare fruit.", "fake"),
#     ("Secret government tunnels lead directly to the moon.", "fake"),
#     ("Scientists confirm time travel will be available next year.", "fake"),
#     ("Eating chocolate three times a day makes you live forever.", "fake"),
#     ("A celebrity adopted a dragon as a pet.", "fake"),
#     ("Newly found crystal can control people’s thoughts.", "fake"),
#     ("The world will end on the 13th of next month.", "fake"),
#     ("Dinosaurs still live in a hidden island in the Pacific.", "fake"),
#     ("A smartphone app can make you fly for ten minutes.", "fake"),
#     ("The government is hiding proof of mermaids in the ocean.", "fake"),
#     ("Magical herbs discovered in the mountains heal any illness.", "fake"),
#     ("Aliens are controlling weather patterns around the globe.", "fake"),
#     ("The Eiffel Tower secretly produces free electricity.", "fake"),
#     ("A new mineral allows humans to breathe underwater.", "fake"),
#     ("Ancient ruins show humans were once 20 feet tall.", "fake"),
#     ("Secret potion discovered that grants eternal youth.", "fake"),
#     ("The moon is actually hollow and filled with gold.", "fake"),
#     ("Robots have already taken over a hidden city underground.", "fake")
    
    
# ]




# fu = File_Utility()
# # # fu.write_file(fake_docs, "fu.txt")
# # # pwf=fu.write_pickle_file(fake_docs, "pfu.pkl")
# # # prf=fu.read_pickle_file(pwf)

# rfu = fu.read_file("../dataset/files/real.txt")
# print(rfu)

# # print(prf)