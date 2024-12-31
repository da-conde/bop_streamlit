import streamlit as st
import pandas as pd
#import base64
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

#import fitz
from bs4 import BeautifulSoup
import requests
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from streamlit_ydata_profiling import st_profile_report
from ydata_profiling import ProfileReport



    #Refubium 
def scraping_refubium(link):
    #link = "https://refubium.fu-berlin.de/handle/fub188/34966"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    big_container = soup.find_all("div", class_="box box-search-list list-group")
    second_container = big_container[1]
    items_box = second_container.find_all("div", class_="list-group-item")


    meta_data = big_container[0].find_all("div", class_="col-s-12 col-m-9")
    header = meta_data[0].getText()
    author = meta_data[2].getText()
    publication_year = meta_data[3].getText()
    abstract = meta_data[5].getText()
    department = meta_data[11].getText()
    language = meta_data[7].getText()








    data = {}
    refubium_url = "https://refubium.fu-berlin.de"

    for count, file in enumerate(items_box):
        titel = file.find("div", class_="file-name").getText()
        file_format = file.find("div", class_="file-format").getText()
        file_format = titel.rpartition('.')[2]
        url_box = file.find("div", class_="btn-group")
        url_box_extract = url_box.find('a')
        file_url = url_box_extract.get('href')
        complete_file_url = refubium_url + file_url
        data[count+1] = {"Format":file_format, "Titel": titel, "Link": complete_file_url, "Header": header,
                         "Author": author, "Year" : publication_year, "Abstract":abstract, "Department":department, "Language":language}

        #return data




    df = pd.DataFrame.from_dict(data).transpose()


    st.dataframe(df, column_config={
        "Link": st.column_config.LinkColumn(
            "URL",
            
        )
    },
    hide_index=True,)






    #col1, col2, col3 = st.columns([3, 1, 1])
    #with col1:
        #st.subheader("Title")
    
    #with col2:
        #st.subheader("Format")

    #with col3:
        #st.subheader("Action")

    #for index, row in df.iterrows():
        #col1, col2, col3 = st.columns([3, 1, 1])
        #with col1:
            #st.write(row['Titel'])
            
        #with col2:
            #st.write(row['Format'])

        #with col3:
            #if st.button("Bearbeiten", type="primary", key=index-1):
                #st.write(row['Link']) 
          
       # with col4:
            #if st.button("Download", type="primary", key=index+index):
                #st.write(row['Link']) 
        
        
                
            
        #st.divider()
    return df