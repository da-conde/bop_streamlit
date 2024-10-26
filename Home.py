import streamlit as st
from PIL import Image

st.title('Berlin Open Science Platform')

image = Image.open('bua.jpeg')
st.image(image)