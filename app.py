import streamlit as st
import pandas as pd
import pickle
import time
from preprocess import preprocess
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Can You Survive the Titanic?", page_icon="🚢", layout="centered")

top = """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 3rem;
            margin-top: 0rem;
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
                background-color: #ffffff;
                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
                padding-left: 40px;
        }

        [data-testid=toastContainer] {
                position: absolute;
                margin: 0 auto;
                margin-inline: auto;
                max-width: 350px;
                display: flex;
                justify-content: center;
        }
        [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 18px;
                color: #24252d;
        }
        </style>
        """
st.markdown(toast, unsafe_allow_html=True)

# TITLE
st.markdown("<h1 style='text-align: center; color: white;'>Can You Survive the Titanic?</h1>", unsafe_allow_html=True)

with stylable_container(
        key = "titanic_form",
        css_styles = """
        div[data-testid="stForm"] {
                background-color: #5c94af;
                box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
        }
        """
        ):
        with st.form("my_form"):
                name = st.text_input("NAME", "John Smith")
                class_col, status_col, sex_col = st.columns(3)
                with class_col:
                        pclass = st.selectbox("CLASS", ("1", "2", "3"))
                with status_col:
                        sp = st.selectbox("STATUS", ("Single", "Married"))
                with sex_col:
                        sex = st.selectbox("SEX", ("Male", "Female"))
                cabin_col, embarked_col = st.columns(2)
                with cabin_col:
                        cabin = st.selectbox("CABIN", ("A", "B", "C", "D", "E", "F", "G", "T"))
                with embarked_col:
                        embarked = st.selectbox("EMBARKED", ("Cherbourg", "Queenstown", "Southampton"))
                col1, col2 = st.columns(2)
                with col1:
                        age = st.slider("AGE", 0, 100, 18)
                        par = st.slider("PARENTS", 0, 2, 0)
                with col2:
                        sib = st.slider("SIBLINGS", 0, 15, 0)
                        ch = st.slider("CHILDREN", 0, 15, 0)
                        
                if sp == "Married":
                        sibsp = sib + 1
                else:
                        sibsp = sib
                parch = par + ch

                with stylable_container(
                        key = "form_button",
                        css_styles = """
                        button[data-testid="baseButton-secondaryFormSubmit"] {
                                    width: inherit;
                                    color: white;
                                    background-color: #716144;
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
