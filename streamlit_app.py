import streamlit as st

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
