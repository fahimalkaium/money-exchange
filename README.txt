HelpNao Money Exchange – Flask Project
Author: Md. Kaium

---
## Manual Terminal run process
& "c:\Users\z0042zpd\OneDrive - Siemens AG\My Old Folder\Training\22.1 Coursera\08. Python\Note Exchange\.venv\Scripts\python.exe" "c:\Users\z0042zpd\OneDrive - Siemens AG\My Old Folder\Training\22.1 Coursera\08. Python\Note Exchange\app.py"

User One
Mobile: 01914123412
Pss: 1234
Shop Name: Mrs. Alo Bitan

User Two
Mobile: 01914123443
Pss: 1234
Shop Name: Abdullah Traders

## PROJECT DESCRIPTION

This is a simple Flask-based web application for managing
money change requests. Users can register, login, and create
cash exchange requests.

The goal of this project is to practice:

* Python Flask
* HTML/CSS
* SQLite database
* Login authentication
* Dashboard system

---

## PROJECT STRUCTURE

NOTE EXCHANGE
│
├── app.py                -> Main Flask application
├── database.db           -> SQLite database
│
├── templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── create_request.html
│
├── static
│   └── images
│       ├── HelpNao_logo.png
│       └── Taka.jpg

---

## HOW TO RUN THE PROJECT

1. Open terminal

2. Activate virtual environment

Windows:
venv\Scripts\activate

3. Run the application

python app.py

4. Open browser

http://127.0.0.1:5000

---

## MAIN FEATURES

1. User Registration
2. User Login
3. Session based authentication
4. Dashboard
5. Money exchange request

---

## TECHNOLOGY USED

Backend: Python Flask
Frontend: HTML + CSS
Database: SQLite

---

## MY LEARNING NOTES

Flask uses a folder structure:

templates → HTML files
static → images, CSS, JS

Example image loading in Flask:

<img src="{{ url_for('static', filename='images/HelpNao_logo.png') }}">

Example route in Flask:

@app.route('/login', methods=['GET','POST'])
def login():
pass

---

## FUTURE IMPROVEMENTS

* Admin panel
* Request approval system
* Email notification
* Better UI design
* Deployment on cloud
