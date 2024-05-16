from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import *
from app.forms import LoginForm, RegisterForm
from flask import send_from_directory
import openai
from datetime import datetime
import fitz, os
from app import bm25, summary, transformer, nn
import json
from groq import Groq
openai.api_key = app.config['API_KEY']
client = Groq(
    api_key=app.config['API_KEY'],
)
db.create_all()

###
# Routing for your application.
###
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')






#----------------------------------------------------------------------------#



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Render the website's sign up page"""
    form = RegisterForm()
    #stores new credentials to user table in database on submit
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data

        sameEmail = User.query.filter_by(email=email).first()
        if sameEmail:
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))

        if password != confirmPassword:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        user = User(email, password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            flash('Database Error', 'danger')
            return redirect(url_for('home'))

        flash('Registration Successful! You may now proceed to Log In.', 'success')            
        return redirect(url_for('login'))
    else:
        flash_errors(form)        
    return render_template('register.html', form = form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password values from the form.
        email = form.email.data
        password = form.password.data

     
        user = User.query.filter_by(email=email).first()
        print(user)
        print(password)
        print(check_password_hash(password, user.password))
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect login information', 'danger')
            return redirect(url_for('login'))     
        
        # Gets user id, load into session
        login_user(user)
        userid = user.id
        session['uid']=userid
    
        flash('You have succesfully logged in.', 'success')
        return redirect(url_for("library"))  # The user should be redirected to the upload form instead
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Render the website's sign up page"""
    form = RegisterForm()

    #stores new credentials to user table in database on submit
    if form.validate_on_submit():
        email = form.email.data
    
        if form.password.data == form.confirmPassword.data:
            print(form.password.data)

            password = form.password.data
            newuser = User(email, password)
            uemail = User.query.filter_by(email=form.email.data).first()
            if uemail:
                flash('Email already exists', 'danger')
            else:
                db.session.add(newuser)
                db.session.commit()
                flash('Successfully Registered. You may Log In!', 'success')            
                return redirect(url_for('login'))
        else:
            flash('Passwords do not match', 'danger')
    else:
        flash_errors(form)        
    return render_template('signup.html', form = form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
 
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Success')
    return redirect(url_for('login'))

@app.route('/quiz', methods=['POST', 'GET'])
def quiz():
    bookInfo = []
    books = db.session.execute(db.select(Book)).scalars()
    for book in books:
        bookInfo.append({
            "Name" : book.filename,
        })
    selectedbook = request.args.get('selectedbook')
    return render_template("quiz.html", active_page = "quiz", books = bookInfo, selectedbook = selectedbook)

@app.route('/fetch-questions', methods=['POST'])
def fetch_questions():
    data = request.json
    query = data['topic']
    bookName = data['book']
    
   
   
  
    context = bm25.main(bookName, query, more=True)

    prompt = (
    f"Generate 5 multiple-choice questions based on the following context:\n\n"
    f"Context: {context}\n\n"
    f"The answer should be a list of dictionaries where each dictionary looks like this.\n"
    f"""{{
    "question": "What is the capital of France?",
    "options": ["London", "Paris", "Berlin", "Rome"],
    "correctAnswer": "Paris"
}}\n"""
)


    try:
        chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        )
        answer = chat_completion.choices[0].message.content
    except Exception:
        answer = "Unable to generate"
    
   

    import ast

   
    dictionary = ast.literal_eval(answer)
    json_data = jsonify(dictionary)

    return json_data
  

   
    return


@app.route('/chat', methods=['POST', 'GET'])
def chat():  
    bookInfo = []
    
    suggestions = []
    if request.method == 'POST':
        data = request.json
        query = data['message']
        bookName = data['book']
        
        
       
       
        pagenum, context, score = bm25.main(bookName, query, pagenum = None)
        print(bookName, pagenum)

        try:
            suggestions = nn.main(bookName, pagenum)
        except Exception:
            suggestions = nn.main(bookName, 100)
      
        
        if score < 1:
            response = """Unfortunately, I'm unable to provide a direct
              answer to your question due to insufficient information 
              provided. If you could provide more details or specify your
              query further, I would be more than happy to assist. Please
                feel free to ask more questions or let me know how I can 
                assist you in any other way."""
        else:
            try:
                response = Ai(query, context, score)
            except Exception:
                print("api failed")
                response = "fail"
          

        response = {
        "response": response,
        "suggestions": suggestions,
        "pagenum" : pagenum
        }
    
   

        return jsonify(response) 

    else:
        books = db.session.execute(db.select(Book)).scalars()
        for book in books:
            bookInfo.append({
                "Name" : book.filename,
            })       
        selectedbook = request.args.get('selectedbook')


    return render_template("chat.html", active_page = "chat", books = bookInfo, selectedbook = selectedbook)



def Ai(query, context, score):
    prompt = (
        f"Based on the following script, please answer the question at the end. Here is the script:\n {context}\n"
        f"Based on the script provided, please answer the following question:{query}"
    )



    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="mixtral-8x7b-32768",
    )

    answer = chat_completion.choices[0].message.content
     
  
    

    return answer


@app.route('/getSummary', methods=['POST', 'GET'])
def getSummary():
    data = request.json
    book_name = data.get('bookName')
    flag = data.get('flag')
    score = 90

    words = data.get('wordss', [])
   
    if(not flag):
        query = ' '.join(words)
        _, context, score = bm25.main(book_name, query)
        
    else:
       
        context = bm25.main(book_name, "query", pagenum = int(words))
       
    # Extract the bookName, chapter, and nextChapter from the data

    

    summary  = Ai("Summarize this", context, score)
   
    return jsonify(summary) 

@app.route('/get_topics', methods=['POST'])
def get_topics():
    # Example usage, assuming you have a predefined 'lda_model' loaded and ready
    
    data = request.json 
    book_name = data.get('bookName')
    

    book = Book.query.filter_by(filename=book_name).first()
    bookId = book.bookid
   
    book_topics = Topics.query.filter_by(book_id=bookId).first()

    if book_topics is None:
        info = summary.main(book_name)
        topics_string = json.dumps(info)
        topic = Topics(book_id=bookId, topics=topics_string)  # Create new chapter
        db.session.add(topic)
        db.session.commit() 
   
    else:
        info = json.loads(book_topics.topics)
    

    return jsonify(info)

@app.route('/summary', methods=['POST', 'GET'])
def summaryy():
    chapterInfo = []
    bookInfo = []
    
    books = db.session.execute(db.select(Book)).scalars()
    for book in books:
        bookInfo.append({
            "Name" : book.filename,
        })  

    return render_template("summary.html", active_page = "summary",
                            books = bookInfo, chapters = chapterInfo)



@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        book = request.files['file']
        bookname = secure_filename(book.filename)
        book_path = os.path.join(app.config['UPLOAD_FOLDER'], bookname)
        book.save(book_path)
        extract_cover_image(book_path)

        book = Book(bookname)

        try:
            db.session.add(book)
            db.session.commit()
        except:
            print("Database error")
    
        

    return render_template("upload.html", active_page = "upload")

@app.route('/library', methods=['POST', 'GET'])
def library():
    books = db.session.execute(db.select(Book)).scalars()
    bookInfo = []
    for book in books:
        bookInfo.append({
            "Name" : book.filename,
            "Uploaded" : book.dateuploaded
        })    
    return render_template("library.html", books = bookInfo)

@app.route('/library/<bookname>')
def get_image(bookname):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), bookname.replace('.pdf', '.png'))

def extract_cover_image(pdf_path):
    with fitz.open(pdf_path) as doc:
        # Check if the document has pages
        if doc.page_count > 0:
            page = doc.load_page(0)  # first page
            pix = page.get_pixmap()
            image_path = pdf_path.replace('.pdf', '.png')
            pix.save(image_path)