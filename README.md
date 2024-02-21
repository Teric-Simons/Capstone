# Capstone

python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run



completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]) 
        response = completion.choices[0].message.content.split(":")[-1].strip()   
        print(response)

        return jsonify(response) 







