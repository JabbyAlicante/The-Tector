import praw # wrapper
from dotenv import load_dotenv
import os, random, time
import requests
from bs4 import BeautifulSoup

# from preprocessing import Preprocessing

'''
REDDIT:
create reddit app: https://www.reddit.com/prefs/apps
redirect uri: link sa github ko nilagay ko idkkk
get the personal use script (client id) and secret (client secret)
put info in .env file

FACEBOOK:
wala pa implementation

OTHER NEWS SITES WE CAN CONSIDER TO SCRAPE (they offer APIs):
- newsapi.org
- nytimes.com
- theguardian.com
'''

class PostExtractor:
    def __init__(self):
        self.HEADERS = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        ]
        load_dotenv()
        self.reddit = praw.Reddit( # REDDIT 
            client_id= os.getenv("REDDIT_CLIENT_ID"),
            client_secret= os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent= os.getenv("REDDIT_USER_AGENT")
        )

    def extract_post(self, url):
        if "reddit.com" in url:
            return self.extract_reddit(url)
        elif "facebook.com" in url:
            return self.extract_facebook(url)
        elif "news" in url or "cnn" in url or "rappler" in url or "pep" in url or "philstar" in url or "inquirer" in url : 
            return self.extract_news(url)
        else:
            print("Unsupported URL.")
            return None



    def extract_reddit(self, url):
        try:
            submission = self.reddit.submission(url=url)
            # title = submission.title
            # body = submission.selftext
            return {
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url
            }
        
        except Exception as e:
            print(f"Error extracting post: {e}")
            return None
        

    def extract_facebook(self, url):
        pass


    def extract_news(self, url): # CURRENTLY WORKS FOR PHILSTAR, PEP, RAPPLER
        try:
            headers = random.choice(self.HEADERS)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')


            # TITLE EXTRACTION
            title = soup.find('h1')
            title_text = title.get_text(strip=True) if title else "No title found"

            # BODY
            content_selectors = [
                'div.article-content',
                'div.story-content', 
                'div.entry-content',
                'itemprop.articleBody'
                'article .content',
                'div[class*="article-body"]',
                'div[class*="story-body"]', 
                'div[class*="post-content"]',
                'div[class*="entry-content"]',
                '.article-text',
                '.story-text',
                'main article',              
                'article'
            ]

            article_content = None
            for selector in content_selectors:
                article_content = soup.select_one(selector)
                if article_content:
                    break

            if not article_content: # LOOK FOR P TAGS
                paragraphs = soup.find_all('p')
                if len(paragraphs) > 3:  
                    article_content = soup.new_tag('div')
                    for p in paragraphs:  
                        article_content.append(p)

            if article_content:
                unwanted_elements = [
                    'script', 'style', 'nav', 'footer', 'header',
                    '.advertisement', '.ad', '.sidebar', '.social-share',
                    '.related-articles', '.comments', '.newsletter-signup',
                    '[class*="ad"]', '[id*="ad"]', '.promo'
                ]
                
                for selector in unwanted_elements:
                    for element in article_content.select(selector):
                        element.decompose()
                
                body_text = article_content.get_text(separator='\n', strip=True)
                
                lines = [line.strip() for line in body_text.split('\n') if line.strip()]
                body_text = '\n'.join(lines)
                
            else:
                body_text = "No article content found"
                            
            return {
                "title": title_text,
                "body": body_text,
                "url": url,
                "word_count": len(body_text.split()) if body_text != "No article content found" else 0
            }

        except Exception as e:
            print(f"Error extracting article from {url}: {e}")
            return {
                "title": "Error",
                "body": f"Failed to extract: {str(e)}",
                "url": url,
                "word_count": 0
            }


# if __name__ == "__main__":
#     # url = "https://www.reddit.com/r/Tech_Philippines/comments/1na9thy/got_reminded_why_i_dont_buy_iphones/"
#     url = input("Enter URL: ")
#     extractor = PostExtractor()
#     preprocess = Preprocessing()
#     post = extractor.extract_post(url)
#     if post:
#         print("Title:", preprocess.tokenize(post["title"]))
#         print("Body:", preprocess.tokenize(post["body"]))
#         print("URL:", post["url"])
#         if "word_count" in post:
#             print("Word Count:", post["word_count"])
#     else:
#         print("Failed to extract post.")
    
    
# load_dotenv()  

# # REDDIT API INFO
# reddit = praw.Reddit(
#     client_id= os.getenv("REDDIT_CLIENT_ID"),
#     client_secret= os.getenv("REDDIT_CLIENT_SECRET"),
#     user_agent= os.getenv("REDDIT_USER_AGENT")
# )

# # get submission by URL
# url = "https://www.reddit.com/r/Tech_Philippines/comments/1na9thy/got_reminded_why_i_dont_buy_iphones/"
# submission = reddit.submission(url=url)

# print("Title:", submission.title)
# print("Body:", submission.selftext)  # text inside the post
