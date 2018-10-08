from flask import Flask, request, redirect, render_template

import cgi 
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True 

@app.route('/')
def index():
    template = jinja_env.get_template('user_signup_form.html')
    return template.render()

@app.route('/welcome', methods=['POST'])
def welcome():
    username = request.form['username']
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

@app.route('/validate-signup')
def display_user_signup_form():
    template = jinja_env.get_template('user_signup_form.html')
    return template.render()

@app.route('/', methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    if username == '': 
        username_error = 'Please enter a valid username'

    if password == '': 
        password_error = 'Please enter a valid password'
    
    if verify_password == '':
        verify_password_error = 'Please enter a valid password'

    if " " in username: 
        username_error = 'Please enter a valid username without spaces' 
    
    if " " in password: 
        password_error = 'Please enter a valid password without spaces' 

    if len(username) <= 3 or len(username) >= 20:
        username_error = 'Please enter a valid username (3-20 characters)'
    
    if len(password) <= 3 or len(password) >= 20:
        password_error = 'Please enter a valid password (3-20 characters)'

    if password != verify_password:
        password_error = 'Passwords must match'

    if " " in email:
        email_error = 'Please enter a valid email address with no spaces'
    
    if "@" not in email:
        email_error = 'Please enter a valid email address in the proper format (missing @)'
    
    if len(email) <= 3 or len(email) >= 20:
        email_error = 'Please enter a valid email address (3-20 characters)'
    
    if "." not in email:
        email_error = 'Please enter a valid email address in the proper format (missing .)'

    if not username_error and not password_error and not verify_password_error and not email_error:
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username)
    else: 
        template = jinja_env.get_template('user_signup_form.html')
        return template.render(username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error, username=username, email=email)

app.run()