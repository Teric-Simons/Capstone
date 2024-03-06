import math
import PyPDF2
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

class BM25:
    def __init__(self, book, k1=1.5, b=0.75):
        self.book = book
        self.book_size = len(book)
        self.avg_doc_len = sum(len(doc) for doc in book) / self.book_size
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.k1 = k1
        self.b = b
        self.initialize()

    def initialize(self):
        df = {}
        for page in self.book:
            self.doc_freqs.append(Counter(page))
            self.doc_len.append(len(page))
            for word in set(page):
                df[word] = df.get(word, 0) + 1
        for word, freq in df.items():
            self.idf[word] = math.log(1 + (self.book_size - freq + 0.5) / (freq + 0.5))

    def score(self, page, query):
        score = 0.0
        doc_len = len(page)
        doc_counter = Counter(page)
        for word in query:
            if word not in self.idf:
                continue
            idf = self.idf[word]
            tf = doc_counter[word] * (self.k1 + 1) / (doc_counter[word] + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len))
            score += idf * tf
        return score

    def get_scores(self, query):
        scores = []
        for index, page in enumerate(self.book):
            score = self.score(page, query)
            scores.append((index, score))
        return scores
    

pages_text = []
def extract_text_from_pdf(pdf_name):
    pdf_path = 'uploads/' + pdf_name

    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Loop through each page in the PDF
        for page in pdf_reader.pages:
            # Extract text from the page and append it to the list
            pages_text.append(page.extract_text())

    return pages_text


def prepare_book(pages):
    """
    Cleans up the book by removing common escape sequences from each page, tokenizing the content using NLTK,
    and removing stop words.
    """
    # Compile a pattern to match common escape sequences
    pattern = re.compile(r'[\n\t\r\f\v]+')
    
    # Load stop words
    stop_words = set(stopwords.words('english'))
    
    # Remove escape sequences, tokenize using NLTK, and remove stop words in one step
    cleaned_and_tokenized_pages = [
        [word for word in word_tokenize(re.sub(pattern, ' ', page)) if word.lower() not in stop_words]
        for page in pages
    ]
    
    return cleaned_and_tokenized_pages

def prepare_query(query):
    """
    Cleans the query list by removing escape sequences, special characters,
    symbols, and punctuation, leaving only alphanumeric characters and spaces.
    Then splits it back into a list of words and removes stop words.
    """
    # Join the list into a single string
    query_str = " ".join(query)
    
    # Pattern to match escape sequences, special characters, symbols, and punctuation
    # This pattern keeps alphanumeric characters (letters and numbers) and spaces
    pattern = re.compile(r'[^\w\s]+|[\n\t\r\f\v]+', re.UNICODE)
    
    # Replace matched characters with a space
    cleaned_query_str = re.sub(pattern, ' ', query_str)
    
    # Optionally, remove extra spaces
    cleaned_query_str = re.sub(r'\s+', ' ', cleaned_query_str).strip()
    
    # Tokenize the cleaned string
    tokens = word_tokenize(cleaned_query_str)
    
    # Load English stopwords
    stop_words = set(stopwords.words('english'))
    
    # Remove stopwords from the tokens
    cleaned_query_list = [word for word in tokens if word.lower() not in stop_words]
    
    return cleaned_query_list



def main(pdf_name, query):
    prequery = query
    pages = extract_text_from_pdf(pdf_name)
    book = prepare_book(pages)

    # Instantiate BM25 with the book
    bm25 = BM25(book)

    query = query.split(" ") #tokenize
    query = prepare_query(query)
  
    # Get scores for the query
    scores = bm25.get_scores(query)

    # Sort scores in descending order to see which documents are most relevant
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Display the results
    for doc_index, score in sorted_scores[:1]:
        print(f"Page: {doc_index}, Score: {score}")
    page_num = sorted_scores[0][0]
    page = pages_text[page_num]
    return page, sorted_scores[0][1]












