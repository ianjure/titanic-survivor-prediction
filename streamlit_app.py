import streamlit as st
import pandas as pd

hide = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide, unsafe_allow_html = True)

st.title('🚢 Can You Survive the Titanic?')
st.info('Enter your data below to test!')

from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

def preprocess_cred(df):

    """
    DATA PREPROCESSING
    """

    # DROP UNNECESSARY COLUMNS
    df = df.drop(['PassengerId', 'Name', 'Ticket'], axis = 1)

    # CONVERT SEX TO BINARY
    df['Sex'] = (df['Sex'] == 'male').astype(int)

    # CREATE PCLASS CATEGORIES COLUMNS
    df['Pclass_1'] = (df['Pclass'] == "1").astype(int)
    df['Pclass_2'] = (df['Pclass'] == "2").astype(int)
    df['Pclass_3'] = (df['Pclass'] == "3").astype(int)

    # CREATE EMBARKED CATEGORIES COLUMNS
    df['Embarked_C'] = (df['Embarked'] == 'C').astype(int)
    df['Embarked_Q'] = (df['Embarked'] == 'Q').astype(int)
    df['Embarked_S'] = (df['Embarked'] == 'S').astype(int)

    # CREATE CABIN CATEGORIES COLUMNS
    df['Cabin_A'] = (df['Cabin'] == 'A').astype(int)
    df['Cabin_B'] = (df['Cabin'] == 'B').astype(int)
    df['Cabin_C'] = (df['Cabin'] == 'C').astype(int)
    df['Cabin_D'] = (df['Cabin'] == 'D').astype(int)
    df['Cabin_E'] = (df['Cabin'] == 'E').astype(int)
    df['Cabin_F'] = (df['Cabin'] == 'F').astype(int)
    df['Cabin_G'] = (df['Cabin'] == 'G').astype(int)
    df['Cabin_T'] = (df['Cabin'] == 'T').astype(int)

    # DROP ORIGINAL PCLASS AND EMBARKED COLUMNS
    df = df.drop(['Pclass', 'Embarked', 'Cabin'], axis = 1)

    """
    FEATURE ENGINEERING
    """

    # CREATE FAMILY COLUMN BY ADDING PARENT AND SIBLING COLUMNS
    df['Family'] = df['Parch'] + df['SibSp']

    # CREATE ALONE COLUMN
    df['Alone'] = (df['Family'] == 0).astype(int)

    # CREATE FARE CLASSES
    df['Very Low'] = (df['Fare'] <= 4).astype(int)
    df['Low'] = ((df['Fare'] > 4) & (df['Fare'] <= 15)).astype(int)
    df['Moderate'] = ((df['Fare'] > 15) & (df['Fare'] <= 25)).astype(int)
    df['Medium'] = ((df['Fare'] > 25) & (df['Fare'] <= 50)).astype(int)
    df['High'] = ((df['Fare'] > 50) & (df['Fare'] <= 100)).astype(int)
    df['Very High'] = ((df['Fare'] > 100) & (df['Fare'] <= 250)).astype(int)
    df['Luxury'] = (df['Fare'] > 250).astype(int)

    # CREATE AGE CATEGORIES
    df['Baby'] = (df['Age'] <= 5).astype(int)
    df['Child'] = ((df['Age'] > 5) & (df['Age'] <= 14)).astype(int)
    df['Teenager'] = ((df['Age'] > 14) & (df['Age'] <= 18)).astype(int)
    df['Adult'] = ((df['Age'] > 18) & (df['Age'] <= 30)).astype(int)
    df['OldAdult'] = ((df['Age'] > 30) & (df['Age'] <= 60)).astype(int)
    df['Old'] = (df['Age'] > 60).astype(int)

    final_df = df.copy()

    return final_df

# LOAD MODEL
import pickle

with open('titanic.pkl', 'rb') as f:
    model = pickle.load(f)

with st.form("my_form"):
        name = st.text_input("Name", "What is your name?")
        pclass = st.selectbox(
    "Select a class",
    ("1", "2", "3"))
        sex = st.selectbox(
    "Select a sex",
    ("male", "female"))
        age = st.number_input("What is your age?")
        sib = st.number_input("How many of your siblings are aboard?")
        sp = st.checkbox("Is your spouse aboard?")
        if sp:
            sibsp = sib + 1
        else:
                sibsp = sib
        parch = st.number_input("Parents/Children aboard?")
        cabin = st.selectbox(
            "Select a cabin",
            ("A", "B", "C", "D", "E", "F", "G", "T"))
        embarked = st.selectbox(
            "Embarked from?",
            ("Cherbourg", "Queenstown", "Southampton"))

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

        if submitted:
                cred_dict = {
                    'PassengerId': [1],
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
                cred_df = pd.DataFrame(cred_dict)
                creds = preprocess_cred(cred_df)
                ypred = model.predict(creds)
                    
                if ypred[0] == 0:
                  st.write("You will not survive!")
                else:
                  st.write("You will survive!")
