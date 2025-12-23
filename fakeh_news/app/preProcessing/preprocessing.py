import re
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.file_utils import File_Utility



class Preprocessing:
    def __init__(self, neg_scope=3):
        self.file_util = File_Utility()
        self.NEGATED_WORDS = ["not", "no", "never", "n't", "cannot", "can't", "cant", "don't", "dont", "doesn't", "doesnt", "won't", "wont", "shouldn't", "shouldnt", "wouldn't", "wouldnt", "couldn't", "couldnt"]
        self.neg_scope = neg_scope  # max words to tag after negation (to avoid over tagging negated words)
        self.STOPWORDS = self.file_util.load_stopwords("src/files/stopwords.txt")
        self.MULTI_WORDS = self.file_util.load_multiwords("src/files/multi_words.txt")
        self.NEGATED_NAMES = self.file_util.read_file("src/files/names.txt")

        # print(self.MULTI_WORDS)
    def normalize(self, text):
        
        
        # handle case for "U.S." and "U.S.A." (problem: nattokenize per letter because of periods)
        ACRONYMS = {
            r"\bU\.S\.A\.?\b": "united_states", 
            r"\bU\.S\.?\b": "united_states", # para ma differentiate sa US (United States) vs us (tayo) ???? IDKKK
            r"\bUS\b": "united_states", # capitalized 'US' will be consider as united_states (para di magka conflict sa 'us'(we))
            r"\bUSA\b": "united_states",
            r"\bu\.s\.?\b": "united_states",
            r"\bu\.s\.a\.?\b": "united_states",
            r"\bUnited States( of America)?\b": "united_states",
            r"\bunited states( of america)?\b": "united_states",

            r"\bPH\.?\b": "philippines",
            
            r"\bU\.K\.?\b": "united_kingdom",
            r"\bu\.k\.?\b": "united_kingdom",
            r"\bUK\b": "united_kingdom",

            r"\bE\.U\.?\b": "european_union",
            r"\bU\.N\.?\b": "united_nations",

            r"\bgovt\b": "government",
            r"\bdept\b": "department",
            r"\binfo\b": "information",
            r"\bSen\.\b": "senator",
            r"\bRep\.\b": "representative",
            r"\bGov\.\b": "governor",

        }

        for pattern, replacement in ACRONYMS.items():
            text = re.sub(pattern, replacement, text)

        text = text.lower()

        text = re.sub(r"\b([a-z]+)'s\b", r"\1", text)
        
        text = re.sub(r"http\S+|www\S+|https\S+", " ", text) # remove urls
        text = re.sub(r"\S+@\S+", " ", text) # remove emails
        text = re.sub(r"\d+", " <NUM> ", text) # remove numbers
        text = re.sub(r"[^a-z0-9.,?!'_]", " ", text) # keep . , ? !
        text = re.sub(r"([.,?!])\1+", r"\1", text) # remove repeated punctuation
        text = re.sub(r"\s+", " ", text).strip()
        
        
        # return text, links
        return text


    def tag_negation(self, tokens):
        updated_tokens = []
        negated = False
        scope_count = 0

        for token in tokens:
            if token in self.NEGATED_WORDS:
               
                negated = True
                scope_count = 0
                updated_tokens.append(token)
            elif token in self.NEGATED_NAMES:
                if negated and scope_count < self.neg_scope:
                    updated_tokens.append(f"NOT_PERSON_NAME_{token}")
                    scope_count += 1
                else:
                    updated_tokens.append(f"PERSON_NAME_{token}")

            elif token in [".", ",", "?", "!"]:
                negated = False
                scope_count = 0
                updated_tokens.append(token)  # still append for negation tagging (stop tagging at punctuation)

            else:
                if negated and scope_count < self.neg_scope:
                    updated_tokens.append(f"NOT_{token}")
                    scope_count += 1
                else:
                    updated_tokens.append(token)
        # print(updated_tokens)

        return updated_tokens


    def tokenize(self, text, special_tokens=False, bigrams=False, remove_stopwords=True):
        text = self.normalize(text)
        
     
        text = self.merge_multiwords(text)  # merge multi-word expressions first
        text = re.sub(r"([.,?!])", r" \1 ", text) # separate punctuation
        tokens = text.split()
        tokens= self.tag_negation(tokens)
        
        # print(tG)

        # remove punctuation tokens after neg tagging
        tokens = [t for t in tokens if t not in [".", ",", "?", "!"]]

        if remove_stopwords: # STOP WORDS
            for t in self.STOPWORDS:
                while t in tokens:
                    tokens.remove(t)

        if special_tokens:
            tokens = ["<s>"] + tokens + ["</s>"]

        if bigrams: # NGRAMS HERE
            bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens)-1)]
            tokens = tokens + bigrams

        return tokens
    def process_links(self, link=None):
   
        pattern = re.compile(r'^(?:https?:\/\/)?(?:www\.)?([a-z0-9-]+)')

        match = pattern.search(link)
        
        if match:
            return match.group(1)
  
            
        return None
            

    # def remove_stopword(self, tokens):
    #     for word in self.STOPWORDS:
    #         while word in tokens:
    #             tokens.remove(word)
    #     return tokens
    
    def merge_multiwords(self, text):
        for mw in sorted(self.MULTI_WORDS, key=len, reverse=True):
            escaped_mw = re.escape(mw.lower())
            underscore = mw.lower().replace(" ", "_")
            text = re.sub(rf"\b{escaped_mw}\b", underscore, text)

        return text



if __name__ == "__main__":
    preprocessor = Preprocessing(neg_scope=3)
#     # read_file = File_Utility()
#     # docs = read_file.read_raw_file("./dataset/files/real.txt")  

#     # for label, content in docs[233:234]:
#     #     print("Original:", content)

    content = "not bts blackpink kardashian jenner and lily rose depp"
    tokens = preprocessor.tokenize(content)
    print("Tokens:", tokens)

  

#     # text = "UK and U.S.A. are allies. U.K is different from us. I don't like the United States of America!"
#     # print("Original:", text)
    
#     text= "The latest update can be read at https://www.cnn.com/2025/09/17/world/news-article.html. Another source is http://gmanews.tv/story/12345, http://fakenews.tv/story/12345 which has a local take. You can also stream live at www.nbc.com/live right now!"
    
#     tokens, links = preprocessor.normalize(text)
#     print(links)
    
#     link =preprocessor.process_links(links)
#     print(link)