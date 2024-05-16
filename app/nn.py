import tensorflow as tf
import PyPDF2
from keras.models import load_model
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
model=load_model("app/neuralNetwork.h5")
tokenizer = Tokenizer()
import PyPDF2


from app import summary


# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
def extract_preprocess_lines(filepath, page_num):
    text_lines = []

    with open(filepath, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if the PDF has at least 10 pages
        if len(pdf_reader.pages) >= page_num:
            page = pdf_reader.pages[page_num-1]  # Access page 10
            page_text = page.extract_text()
            
            
            if page_text:  # Check if text extraction returned any text
                text_lines = page_text.split()
        else:
            return []  # Return an empty list if there are fewer than 10 pages
        
    # Clean and filter the extracted text lines
    
    words = summary.main(filepath.replace('uploads/', ''), True, page_num-1)

   

    cleaned_lines = []
    for line in text_lines:
        # Keep only alphabetic characters and spaces, and remove leading/trailing spaces
        clean_line = ''.join(c for c in line if c.isalpha() or c.isspace()).strip()
        # Split the line into words and remove stopwords
        words_filtered = [word for word in clean_line.split() if word.lower() not in stop_words]
        # Rejoin words to form the cleaned line
        cleaned_line = ' '.join(words_filtered)
        cleaned_lines.append(cleaned_line)
    return words, cleaned_lines
  


def make_prediction(text_list, model):
   
    # Ensure the input is not empty
    if not text_list:
        raise ValueError("Input text list is empty.")

    # Update internal vocabulary based on the text list
    tokenizer.fit_on_texts(text_list)
    
    # Convert texts to sequences of integers
    sequences = tokenizer.texts_to_sequences(text_list)
    
    
    # Pad sequences to ensure consistent input size for the model
    padded_sequences = pad_sequences(sequences, maxlen=50)
    
    # Make predictions using the provided model
    predictions = model.predict(padded_sequences)
    
    return predictions

def generate_questions(text_list):
  
    # Templates for generating questions
    question_template = [
        "What is {text}?",
        "How does {text} work?",
        "Why is {text} important?",
        "Can you explain {text}?"
    ]

    questions = []
    # Generate a question for each text
    for text in text_list:
        question_pattern = random.choice(question_template)
        question = question_pattern.format(text=text)
        questions.append(question)

    return questions

import numpy as np

def headings(new_texts, predictions, words):
  
    result_lst = []
    count = 0

    # Process each text and its corresponding prediction
    for text, prediction in zip(new_texts, predictions):
        # Determine the predicted label using argmax
        predicted_label = np.argmax(prediction)

        # Collect text if predicted as relevant and limit to 5 entries
        if predicted_label == 1 and count < 5:
            result_lst.append(text)
            count += 1

    # Generate and return questions for the selected texts
    common_words = []
    print(result_lst)
    for word in result_lst:
        if word in words:
            common_words.append(word)
    common_words = set(common_words)
    common_words = list(common_words)
    

    if len(common_words) == 0:
        result_lst = set(result_lst)
        result_lst = list(result_lst)
        return generate_questions(result_lst)
    else:
        return generate_questions(common_words)
    




def main(name, page_num):
    file_path = './uploads/' + name
    words, processed_text = extract_preprocess_lines(file_path, page_num)

  
   
    predictions = make_prediction(processed_text, model)
    
    heading = headings(processed_text,predictions, words)
    return heading[0:2]

  