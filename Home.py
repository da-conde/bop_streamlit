import streamlit as st
from PIL import Image
from streamlit_pandas_profiling import st_profile_report 
#from ydata_profiling import ProfileReport
#import matplotlib.pyplot as plt

import numpy as np
#import base64
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from bs4 import BeautifulSoup
#import pybase64





from functions import scraping_refubium
from functions import scraping_deposit
from functions import scraping_edoc
from functions import scraping_tu_repo
from functions import csv
from functions import excel

#st.set_option('deprecation.showPyplotGlobalUse', False)

image = Image.open('bua.jpeg')
st.image(image)

st.title('Berlin Open Science PlatformNowFinalAAAND')

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
   st.image("data:image/png;base64,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", caption="DepositOnce")

with col2:
      st.image("data:image/png;base64,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", caption="Q&U Lab")


with col3:
   st.image("https://www.hu-berlin.de/@@site-logo/og_logo.png", caption="Edoc")

with col4:
   st.image("https://www.wuv.de/var/wuv/storage/images/werben-verkaufen/themen/tech/kreation-mit-ki-zoff-um-neues-logo-der-fu-berlin/10458335-2-ger-DE/Kreation-mit-KI-Zoff-um-neues-Logo-der-FU-Berlin3_reference.jpg", caption="Refubium")

URL = st.text_input('Link', value="...")

check_refubium = URL[8:16]

check_refubium = 'refubium'
check_depositonce = 'depositonce'
check_edoc = 'edoc'
check_tu = "tu.berlin"


if check_refubium in URL.lower():
   files = scraping_refubium(URL)
   file_section = st.selectbox(
        'Choose File',
        files.Titel.unique(),index=None)