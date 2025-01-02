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
import base64
import pybase64
#from ydata_profiling import ProfileReport


# Function to open and display PDF
def displayPDF(file):
     # Opening file from file path
          with open(file, "rb") as f:
               base64_pdf = base64.b64encode(f.read()).decode('utf-8')
     
               pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

          
     # Displaying File
          st.markdown(pdf_display, unsafe_allow_html=True)


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

def scraping_deposit(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    big_container = soup.find("div", class_="list-group")
    items_box = big_container.find_all("a", class_="list-group-item list-group-item-action")
    data = {}
    deposit_once_url = "https://api-depositonce.tu-berlin.de/server/api/core"
    for count, file in enumerate(items_box):
        name = file.find("h5").getText()
        file_format = name.rpartition('.')[2]
        file_url = file.get('href')
        complete_file_url = deposit_once_url + file_url[:-8] + "content"
        data[count+1] = {"Titel": name, "Link": complete_file_url, "Format": file_format}
        df = pd.DataFrame.from_dict(data).transpose()
    st.write(df)
    
    return df

def scraping_edoc(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    big_container = soup.find("div", class_="col-xs-12 col-sm-12 col-md-9 main-content")
    items_section = big_container.find("div", class_="item-page-field-wrapper file-section word-break ds-artifact-list")
    items = items_section.find_all("div", class_="ds-artifact-item")
    items_box = items_section.find_all("div", class_="ds-artifact-item")
    header = big_container.find("div", class_="simple-item-view-title item-page-field-wrapper").getText()
    author = big_container.find("div", class_="simple-item-view-authors item-page-field-wrapper h4").getText().replace('\n', ' ').replace('\r', '')[2:-2]
    abstract = big_container.find("div", class_="simple-item-view-description item-page-field-wrapper table").getText()

    data = {}
    edoc_url = "https://edoc.hu-berlin.de"
    for count, file in enumerate(items_box):
        titel = file.find("div", class_="file-title").getText()
        format = titel.split('.')[1].split(' ')[0]
        url_box_extract = file.find('a')
        file_url = url_box_extract.get('href')
        complete_file_url = edoc_url + file_url
        data[count+1] = {"Format":format, "Titel":titel, "Link": complete_file_url, "Header": "X",
                         "Author": author, "Year" : "X", "Abstract":"X", "Department":"X", "Language":"X"}
        df = pd.DataFrame.from_dict(data).transpose()
    st.write(df)
    return df

def scraping_tu_repo(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = []
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        rows.append(cols)
    
    df = pd.DataFrame(rows, columns=['Attribut', 'Wert'])
    df = df.set_index("Attribut")
    url_string = df.loc["Datei/URL"][0]
    format_string = url_string.rsplit('.', 1 )[1]
    df = df.reset_index()
    df.loc[len(df.index)] = ["Format",format_string] 
    df = df.set_index("Attribut")
    
    return df

def csv(link):
    tab1, tab2, tab3, tab4= st.tabs(["Preview", "Visualization", "Data Report", "Summary"])

    with tab1: #Preview
        df = pd.read_csv(link, delimiter=',', encoding = "ISO-8859-1") 
        st.dataframe(df)
        #new = files[['Header', 'Author', 'Year' , 'Abstract' , 'Department' , 'Language']].copy().transpose()
        #st.dataframe(new, hide_index=None)

    with tab2: #Visualization
        init_streamlit_comm()
        def get_pyg_renderer() -> "StreamlitRenderer":
            df = pd.read_csv(link, delimiter=',', encoding = "ISO-8859-1") 
            return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
        renderer = get_pyg_renderer()
        renderer.render_explore()

    with tab3:
        df = pd.read_csv(link, delimiter=',', encoding = "ISO-8859-1") 
        pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)
        st_profile_report(pr, navbar=True)

    with tab4:
        st.write("tbd")


def excel(link):
    tab1, tab2, tab3, tab4= st.tabs(["Preview", "Visualization", "Data Report", "Summary"])

    with tab1: #Preview
        df = pd.read_excel(link) 
        st.dataframe(df)
        #new = files[['Header', 'Author', 'Year' , 'Abstract' , 'Department' , 'Language']].copy().transpose()
        #st.dataframe(new, hide_index=None)

    with tab2: #Visualization
        init_streamlit_comm()
        def get_pyg_renderer() -> "StreamlitRenderer":
            df = pd.read_excel(link) 
            return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
        renderer = get_pyg_renderer()
        renderer.render_explore()

    with tab3:
        st.write("Profilereport fehlt")
        #df = pd.read_excel(link) 
        #pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)
        #st_profile_report(pr, navbar=True)

    with tab4:
        st.write("tbd")

def txt(link):
    tab1, tab2, tab3, tab4= st.tabs(["Preview", "Visualization", "Data Report", "Summary"])

    with tab1: #Preview
        df = pd.read_csv(link, sep='\s+', encoding = "ISO-8859-1")
        st.dataframe(df) 
    
    with tab2: #Visualization
        def get_pyg_renderer() -> "StreamlitRenderer":
            df = pd.read_csv(link, sep='\s+', encoding = "ISO-8859-1")
            return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
        renderer = get_pyg_renderer()
        renderer.render_explore()

    with tab3:
        st.write("Profile report fehlt")
        #df = pd.read_csv(link, sep='\s+', encoding = "ISO-8859-1")
        #pr = ProfileReport(df, minimal=True, orange_mode=True, explorative=True)
        #st_profile_report(pr, navbar=True)

    with tab4:
        st.write("tab4 tbd.")


def pdf(link):
    tab1, tab2, tab3, tab4= st.tabs(["Preview", "Visualization", "Data Report", "Summary"])

    with tab1: #Preview
        from pathlib import Path
        import requests
        filename = Path('paper.pdf')
        url = link
        response = requests.get(url)
        filename.write_bytes(response.content)  

        with open("paper.pdf", "rb") as file:
                    btn=st.download_button(
                    label="Download pdf",
                    data=file,
                    #file_name="paper.pdf",
                    file_name="paper.pdf",
                    mime="application/octet-stream")
                    displayPDF('paper.pdf') 
        with tab2:
            st.write("tab2 kommt noch")

        with tab3:
            st.write("tab3 kommt noch")

        with tab4:
            st.write("tab3 kommt noch")
            
            #lang_select = st.selectbox('Select Language for summary',('German', 'English', 'Spanish'), index=None)
            #question_select = st.selectbox('Select Question for summary',('German', 'English', 'Spanish'), index=None)
            
            #col1, col2, col3 = st.columns([3, 1, 1])

            #with col1:
                #question_select = st.selectbox('Select Question',('Erstelle eine Summary', 'Beschreibe das Fachgebiet', 'Nenne Keyfacts des Textes',
                #"Fasse die Introduction zusammen", "Fasse die Methodik zusammen", "Fasse die Results zusammen", "Fasse die Diskussion zusammen"), index=None)
                

            #with col2:
                #lang_select = st.selectbox('Select Language',('German', 'English', 'Spanish'), index=None)

            #with col3:
                #detail_select = st.selectbox('Select Detail',('100 Words', '200 Words', '500 Words'), index=None)

            #if lang_select != "None" and question_select != "None" and detail_select != "None" :
                #doc = fitz.open('paper.pdf')
                #text = "" 
                #for page in doc:
                    #text+=page.get_text() 
                    #st.write(text)
                    #frage = "Beschreibe in maximal 100 Wörtern in welchem Fachgebiet bzw. welcher Domäne sich der Text verorten lässt"
                    #frage = "Erstelle mir eine Zusammenfassung des folgenden Text in der Sprache"
                    #messages = [{"role": "system", "content": "You are a Professor"}]
                #if lang_select != None and question_select != None and detail_select != None:
                    #messages.append({"role": "user", "content":frage + lang_select + text})
                    
                    #messages.append({"role": "user", "content":frage + lang_select + text})


                    #messages.append({"role": "user", "content":question_select + " in maximal " + detail_select + " in der Sprache " + lang_select + text})



                    #answers = client.chat.completions.create(model="gpt-4-0125-preview",messages=messages)
                    #st.write(answers.choices[0].message.content)
                #else:
                    #st.write("Hier kannst du ein LLM nutzen")