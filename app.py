import streamlit as st
import pandas as pd
import pickle
from preprocess import preprocess

st.set_page_config(page_title="Can You Survive the Titanic?", page_icon="🚢", layout="centered")

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide, unsafe_allow_html = True)

# TITLE
st.markdown("<h1 style='text-align: center; color: white;'>🚢 Can You Survive the Titanic?</h1>", unsafe_allow_html=True)

with st.form("my_form"):
    name = st.text_input("NAME", "John Smith")
    pclass = st.selectbox("CLASS", ("1", "2", "3"))
    sex = st.selectbox("SEX", ("Male", "Female"))
    age = st.slider("AGE", 0, 100, 18)
    sib = st.slider("SIBLINGS", 0, 15, 0)
    sp = st.checkbox("DO YOU HAVE A SPOUSE?")
    if sp:
        sibsp = sib + 1
    else:
        sibsp = sib
    par = st.slider("PARENTS", 0, 2, 0)
    ch = st.slider("CHILDREN", 0, 15, 0)
    parch = par + ch
    cabin = st.selectbox("CABIN", ("A", "B", "C", "D", "E", "F", "G", "T"))
    embarked = st.selectbox("WHERE ARE YOU EMBARKED FROM?", ("Cherbourg", "Queenstown", "Southampton"))

    submitted = st.form_submit_button("Submit")

    if submitted:
        input = {'PassengerId': [1],
                    'Pclass': [pclass],
                    'Name': [name],
                    'Sex': [sex],
                    'Age': [age],
                    'SibSp': [sibsp],
                    'Parch': [parch],
                    'Ticket': ['A'],
                    'Fare': [32.20],
                    'Cabin': [cabin],
                    'Embarked': [embarked[0]]
                    }
        input_df = pd.DataFrame(input)
        input_final = preprocess(input_df)

        model = pickle.load(open('model.pkl', 'rb'))
        pred = model.predict(input_final)

        if pred[0] == 0:
            st.error(f"{name.split(" ")[0]}, you will not survive!")
        else:
            st.success(f"{name.split(" ")[0]}, you will survive!")
