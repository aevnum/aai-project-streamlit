import streamlit as st
st.title('Hello World')
st.subheader('This is a subheader')

name = st.text_input('Enter your name')
st.write('Hello', name)

maths = st.slider('Enter your maths marks', 0, 100)
st.write(name, 'scored', maths, 'in maths')

exam = st.radio('Which exam?', ['GRE', 'GMAT', 'TOEFL'])
st.write(name, 'took', exam)

subjects = st.multiselect('Select subjects', ['Maths', 'Physics', 'Chemistry'])

st.write(name, 'selected', subjects)

import pandas as pd
uploaded_file = st.file_uploader('Upload a file', type='csv')

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)