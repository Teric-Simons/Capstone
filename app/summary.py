import PyPDF2
import openai
import re

def read_first_10_pages_to_structure(pdf_name):
    # Open the PDF file
    pdf_path = 'uploads/' + pdf_name
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Initialize a list to store the page data
        text = ""
        
        # Determine the number of pages to read (up to 10 or total pages if fewer)
        num_pages = min(30, len(reader.pages))
        
        # Read each of the first 10 pages
        for i in range(num_pages):
            page = reader.pages[i]  # Get the page
            page_text = page.extract_text()  # Extract text from the page
            if "content" in page_text.lower():
                # Create a dictionary for the current page and add it to the list
                text+=page_text
    
    return text


def Ai(text):
    prompt = (
        f"Extract all the subtopics in the table of contents.Make it as detailed as possible.List them comma seperated:\n {text}"
    )

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
  
    answer = response.choices[0].message.content.split(":")[-1].strip().split(",")

    pattern = re.compile(r'[\n\t\r\f\v]+')
    cleaned_answer = [pattern.sub('', text) for text in answer]
    final = [text.title() for text in cleaned_answer if "table of content" not in text.lower()]
    print(final)
    return final


def main(pdf_name):
    text = read_first_10_pages_to_structure(pdf_name)
    print(text)
    if not text:
        return False
    else:
        answer = Ai(text)
    if len(answer) < 4:
        return False
    else:
        return answer

