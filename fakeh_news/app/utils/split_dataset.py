import sys, os
import math
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_utils import File_Utility




class Split_Dataset:
    
    def __init__(self):
        
        self.file_utils = File_Utility()
        
        self.train_path = "dataset/train.txt"
        self.test_path = "dataset/test.txt"
        
        self.real_path = "../dataset/files/real.txt"
        self.fake_path = "../dataset/files/fake.txt"
        
    def _resolve(self, rel_path):
        # get path relative to this file (app/utils/)
        base = os.path.dirname(__file__)            # app/utils
        resolved = os.path.normpath(os.path.join(base, rel_path))
        return resolved
        
        
    def split_ds(self):
        
        real_file = self._resolve(self.real_path)
        fake_file = self._resolve(self.fake_path)

        
        real_docs = self.file_utils.read_raw_file(real_file)
        fake_docs = self.file_utils.read_raw_file(fake_file)
        
       
        
        
        rpercentage = math.ceil(len(real_docs) * 0.2)
        fpercentage = math.ceil(len(fake_docs) * 0.2)
        
        print(rpercentage)
        print(fpercentage)
        
        real_test= real_docs[:rpercentage]
        real_train = real_docs[rpercentage:]
        
        fake_test = fake_docs[:fpercentage]
        fake_train = fake_docs[fpercentage:]
        
        train = real_train + fake_train
        test= real_test + fake_test
        
        random.shuffle(train)
        random.shuffle(test)
        
        wtrain = self.file_utils.write_pickle_file(train, "train.pkl")
        wtest = self.file_utils.write_pickle_file(test, "test.pkl")

        
        


        
        
        
        
        
        



sds = Split_Dataset()

sds.split_ds()