# Capstone

To set up the virtual environment and run the Flask application, follow these steps:

```sh
python -m venv venv  # you may need to use python3 instead
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
flask --app app --debug run
