import PyPDF2
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric, remove_stopwords
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import nltk
from nltk.corpus import stopwords
# Download NLTK stop words


# Define stop words set
stop_words = set(stopwords.words('english'))

# Define custom filters including stop words removal
CUSTOM_FILTERS = [
    lambda x: x.lower(),  # Convert to lowercase
    strip_punctuation,   # Remove punctuation
    strip_numeric,       # Remove numeric characters
    lambda x: " ".join(word for word in x.split() if word not in stop_words and len(word) > 1),  # Remove stopwords and single characters
    lambda x: "".join(char for char in x if char.isalnum() or char.isspace()),  # Remove non-alphanumeric characters
]

def extract_text_from_pdf(pdf_path, nn, num):
    pages_text = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        if nn:
            page = pdf_reader.pages[num]
            text = page.extract_text()
            if text:  # Ensure there's text on the page
                pages_text.append(text)
        else:
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:  # Ensure there's text on the page
                    pages_text.append(text)
    return pages_text

def preprocess_texts(texts):
    return [preprocess_string(text, filters=CUSTOM_FILTERS) for text in texts]

def topic_modeling_on_each_page(texts):
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10)
    return lda_model, corpus

def print_topics(lda_model, num_words=10):
    unique_words = set()
    topics_info = lda_model.show_topics(formatted=False, num_words=num_words)
    for idx, topic in topics_info:
        # Create a list of words for each topic
        words = [word.title() for word, _ in topic]
        # Format the output into a dictionary with topic numbers as keys
        unique_words.update(words)
    unique_words_list = list(unique_words)
    return unique_words_list


def main(pdf_path, nn = False, num = None):
    # Extract text from PDF
    pages_text = extract_text_from_pdf('uploads/' + pdf_path, nn, num)
    # Preprocess texts
    preprocessed_texts = preprocess_texts(pages_text)
    # Model topics for each page
    lda_model, corpus = topic_modeling_on_each_page(preprocessed_texts)
    # Display the top words in each topic
    return print_topics(lda_model)
    # Display topics for each page
    










