# EduBook ReadMe

## Overview

EduBook offers a convenient summarization feature for textbooks. It analyzes the text structure, organizing it into sections by chapters. This creates concise summaries for each part, simplifying complex material for users. With EduBook, users can quickly grasp the main points of a textbook without reading it all. Additionally, users can upload PDF files easily and use the chatbot, powered by advanced technologies like the GPT 3.5 Model and the BM25 Algorithm, for accurate answers. The library feature allows exploration of various PDFs, and the system suggests questions based on textbook content, enhancing the search process.

## Images

![image](https://github.com/user-attachments/assets/9480f49d-9422-48d6-9688-93a6be1b7a03)

![Image 2](link-to-image-2)
![Image 3](link-to-image-3)
![Image 4](link-to-image-4)

## Features

### Summarization
- **Text Structure Analysis**: EduBook analyzes the text structure of textbooks, organizing them into sections by chapters.
- **Concise Summaries**: Creates concise summaries for each part, making complex material easier to understand.
- **Quick Grasp**: Users can quickly grasp the main points of a textbook without reading it all.

### PDF Upload
- **Easy Upload**: Users can upload PDF files easily.
- **Chatbot Support**: The chatbot, powered by advanced technologies like the GPT 3.5 Model and the BM25 Algorithm, provides accurate answers.

### Library Feature
- **Exploration**: Allows users to explore various PDFs.
- **Question Suggestions**: The system suggests questions based on textbook content, enhancing the search process.

## Getting Started

1. **Upload a PDF**: Start by uploading your textbook PDF to EduBook.
2. **Summarize**: Use the summarization feature to get concise summaries of each chapter.
3. **Ask Questions**: Utilize the chatbot to ask questions and get accurate answers based on the textbook content.
4. **Explore Library**: Browse through various PDFs available in the library and enhance your learning experience.

## Contact

For any questions or support, please contact us at [support@edubook.com](mailto:tericsimons12@gmail.com).

---


To set up the virtual environment and run the Flask application, follow these steps:

```sh
python -m venv venv  # you may need to use python3 instead
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
flask --app app --debug run
