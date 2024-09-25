import streamlit as st
import os
import csv
import json
import datetime
import re
import pandas as pd
import plotly.express as px


def save_to_json(data, filename='users.json'):
    if not os.path.exists(filename):
        with open(filename, mode='w') as file:
            json.dump([], file)

    with open(filename, mode='r+') as file:
        users = json.load(file)
        user_data = {
            "email": data[0],
            "password": data[1],
            "name": data[2],
            "mobile": data[3],
            "dob": data[4]
        }
        users.append(user_data)
        file.seek(0)
        json.dump(users, file, indent=4)

def authenticate(email, password, filename='users.json'):
    if not os.path.exists(filename):
        return False

    with open(filename, mode='r') as file:
        users = json.load(file)
        for user in users:
            if user["email"] == email and user["password"] == password:
                return True
    return False

def email_not_exists(email, filename='users.json'):
    if not os.path.exists(filename):
        return True

    with open(filename, mode='r') as file:
        users = json.load(file)
        for user in users:
            if user["email"] == email:
                return False
    return True

def validate(data, filename='users.json'):
    email, password, name, mobile, dob = data
    
    # Check if email is valid
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        st.error("Invalid email format!")
        return False
    
    # Check if phone number is 10 digits
    if not mobile.isdigit() or len(mobile) != 10:
        st.error("Phone number must be 10 digits!")
        return False
    
    # Check if email already exists
    if not email_not_exists(email, filename):
        st.error("User with email already exists!")
        return False
    
    # Check if password is strong
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    if not re.match(password_regex, password):
        st.error("Password must be at least 8 characters long and contain both letters and numbers!")
        return False
    
    return True

def create_user_folder(name):
    if not os.path.exists(name):
        os.makedirs(name)



























# Initialize session state
if 'form' not in st.session_state:
    st.session_state.form = 'signup'

st.sidebar.title("")
if st.sidebar.button("Signup"):
    st.session_state.form = 'signup'
if st.sidebar.button("Login"):
    st.session_state.form = 'login'

if st.session_state.form == 'signup':
    st.header("Welcome to the Sign Up Page")
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'mobile' not in st.session_state:
        st.session_state.mobile = ''
    if 'dob' not in st.session_state:
        st.session_state.dob = None
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'password' not in st.session_state:
        st.session_state.password = ''

    name = st.text_input("Name", value=st.session_state.name)
    mobile = st.text_input("Phone", value=st.session_state.mobile)
    dob = st.date_input("DOB", value=st.session_state.dob, min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    email = st.text_input("Email", value=st.session_state.email)
    password = st.text_input("Password", type='password', value=st.session_state.password)

    if st.button("Submit"):
        st.session_state.name = name
        st.session_state.mobile = mobile
        st.session_state.dob = dob
        st.session_state.email = email
        st.session_state.password = password

        if name and email and password and mobile and dob:
            if validate([email, password, name, mobile, dob.strftime("%d/%m/%Y")]):
                save_to_json([email, password, name, mobile, dob.strftime("%d/%m/%Y")])  #json
                create_user_folder(name)
                st.success("You have successfully signed up!")
                
                # Reset inputs
                st.session_state.name = ''
                st.session_state.mobile = ''
                st.session_state.dob = None
                st.session_state.email = ''
                st.session_state.password = ''
        else:
            st.error("Please enter all information!")

if st.session_state.form == 'login':
    st.session_state.email = ''
    st.session_state.password = ''
    st.header("Login")
    email = st.text_input("Email", value=st.session_state.email)
    password = st.text_input("Password", type='password', value=st.session_state.password)
    if st   .button("Submit"):
        if email and password:
            if authenticate(email, password):
                st.success("Login successful!")
                with open('users.json', mode='r') as file:
                    users = json.load(file)
                    for user in users:
                        if user["email"] == email:
                            st.session_state.current_user = user["name"]
                            break
                st.session_state.form = 'main'
                st.rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please enter all information!")

if st.session_state.form == 'main':
    if st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({'form': 'login'})):
        st.session_state.form = 'login'
    st.header(f"Welcome {st.session_state.current_user}!")
    subjects = ["Math", "Science", "English", "History", "Geography", "Art", "Physical Education"]
    marks = {}

    for subject in subjects:
        marks[subject] = st.slider(f"{subject} Marks", 0, 100, 50)

    if st.button("Submit Marks"):
        st.success("Marks submitted successfully!")
        user_folder = st.session_state.current_user
        csv_filename = os.path.join(user_folder, 'marks.csv')
        
        # Check if the CSV file exists, if not create it with headers
        if not os.path.exists(csv_filename):
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Subject', 'Marks'])
        
        # Append the marks to the CSV file
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            for subject, mark in marks.items():
                writer.writerow([subject, mark])

        st.session_state.form = 'view'
        st.rerun()

if st.session_state.form == 'view':
    if st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({'form': 'login'})):
        st.session_state.form = 'login'
    st.header("Your report is ready!")
    user_folder = st.session_state.current_user
    csv_filename = os.path.join(user_folder, 'marks.csv')

    if os.path.exists(csv_filename):
        df = pd.read_csv(csv_filename)
        
        # Bar chart for average marks
        avg_marks = df.groupby('Subject')['Marks'].mean().reset_index()
        bar_fig = px.bar(avg_marks, x='Subject', y='Marks', title='Average Marks per Subject')
        st.plotly_chart(bar_fig)
        
        # Line chart for all marks
        line_fig = px.line(df, x='Subject', y='Marks', title='Marks per Subject')
        st.plotly_chart(line_fig)
        
        # Pie chart for marks distribution
        pie_fig = px.pie(df, names='Subject', values='Marks', title='Marks Distribution per Subject')
        st.plotly_chart(pie_fig)
    else:
        st.error("No marks data found.")