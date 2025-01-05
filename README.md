# bop_streamlit README


## Zugriff via Internet / Github / Lokal 

https://bopbua.streamlit.app

https://github.com/da-conde/bop_streamlit

streamlit run Home.py

## Home.py Erklärung 

Im Home.py File wird auf Basis der URL geprüft ob es sich um ein DepositOnce, Edoc oder Refubium Repository handelt.
Im Anschluss werden aus dem functions.py File Funktionen aufgerufen welchhe die Datensätze der jeweiligen Repositories scrapen.
Anschließend werden abhängig von Datentypen der ausgewählten Datensätze Funktionen zur Medieninteraktion aufgerufen

## functions.py

Im functions.py File sind zwei Arten von Funktionen definiert. Zuerst sind Funktionen definiert welche auf Basis der bereitgestellten URL die Datensätze und zugrundeliegenden Dateien übergeben. Diese übergebenen Datensätze können durch die verbleibenden Funktionen analysiert werden. Pro Datentyp gibt es eine Analysefunktion. Somit können neue Datentypen hinzugefügt werden.






