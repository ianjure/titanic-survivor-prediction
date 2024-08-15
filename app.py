import streamlit as st
import pandas as pd
import pickle
import time
from streamlit_lottie import *
from preprocess import preprocess
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Can You Survive the Titanic?", page_icon="🚢", layout="centered")

top = """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            margin-top: 1rem;
        }
        </style>
        """
st.markdown(top, unsafe_allow_html=True)

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide, unsafe_allow_html=True)

toast = """
        <style>
        div[data-testid=stToast] {
                position: relative;
                width: 100%;
                background-color: #344c5c;
                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
        }

        [data-testid=toastContainer] {
                position: absolute;
                margin: 0 auto;
                margin-inline: auto;
                min-width: 300px;
                max-width: 300px;
                display: flex;
                justify-content: center;
        }
        [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 18px;
                display: flex;
                justify-content: center;
        }
        </style>
        """
st.markdown(toast, unsafe_allow_html=True)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

ship_anim = load_lottiefile('ship.json')
st_lottie(ship_anim, loop = True, quality = 'high', height = 100)

# TITLE
st.markdown("<h1 style='text-align: center; color: white;'>Can You Survive the Titanic?</h1>", unsafe_allow_html=True)

with stylable_container(
        key = "titanic_form",
        css_styles = """
        div[data-testid="stForm"] {
                background-color: #5c94af;
        }
        """
        ):
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

                with stylable_container(
                        key = "form_button",
                        css_styles = """
                        button[data-testid="baseButton-secondaryFormSubmit"] {
                                    width: inherit;
                                    color: white;
                                    background-color: #5c94af;
                                    border-color: white;
                        }
                        """
                ):
                        submitted = st.form_submit_button("SUBMIT")
                
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
                                st.toast(f"{name.split(" ")[0]}, you will not survive!", icon="😭")
                                time.sleep(8)
                        else:
                                st.toast(f"{name.split(" ")[0]}, you will survive!", icon="😄")
                                time.sleep(8)
