# # from datasets import load_from_disk

# # # Load the dataset from your saved folder
# # dataset = load_from_disk("fake_news_filipino_local")

# # # Save the train split to CSV
# # dataset["train"].to_csv("fake_news_filipino.csv", index=False)

# # print("Dataset saved as fake_news_filipino.csv")

# from datasets import load_dataset

# ds = load_dataset("mohammadjavadpirhadi/fake-news-detection-dataset-english")
# from datasets import Dataset

# # Load train/test arrow files directly
# train_ds = Dataset.from_file("fake_news_cache/0.0.0/231b5e5816682d6d2fdd88b3146bbddd3c3b649f/fake-news-detection-dataset-english-train.arrow")
# test_ds  = Dataset.from_file("fake_news_cache/0.0.0/231b5e5816682d6d2fdd88b3146bbddd3c3b649f/fake-news-detection-dataset-english-test.arrow")

# # Convert to pandas
# train_df = train_ds.to_pandas()
# test_df  = test_ds.to_pandas()

# # Save as CSV
# train_df.to_csv("train.csv", index=False)
# test_df.to_csv("test.csv", index=False)

# print(train_df.head())
# print(test_df.head())



import csv

data = []

files = ["gossips.txt", "fake_facts.txt", "tt.txt"]

for i in files:
    with open(i, "r") as f:
        
        reader = csv.reader(f)
        next(reader)  # skip header if there is one
        for row in reader:
            data.append(row) 
        
        
        
def write_file(text, file_name):
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(text + "\n")    
  
def write_file2(text, file_name):
    with open(file_name, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(text) 
  
# c = 0

# for i in data:
#     write_file2(i, "prefake.csv")
    
#     c+=1

#     if c == 5025:
#         break 
    
         

        
for i in data:
    
    # real_doc = f"1 {i[0]} {i[1]}"
    fake_doc = f"0 {i[0]}"
    
 
    
    # if i[-1] == "Credible":
        
    # write_file(real_doc, "real.txt")
        
    # else: 
    write_file(fake_doc, "newfake.txt")

        
    
    