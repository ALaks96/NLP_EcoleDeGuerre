# Ecole De Guerre Project

This repo automatically extracts text in a given directory for several file formats (pdf,ppt,docx,txt) and saves them in a JSON file. 
The JSON file has several layers, the first layer has an index as key (counter for the number of files).
The second layer has two keys (title and data) referencing the name of the document and its content. 
The third layer has a single key either referencing the page nb, paragraph nb or slide nb.

**To run this code start by installing the packages with the following command in your terminal :**
python3 -m pip install requirements.txt

**Then to launch the code in your current directory, save your file in the nested folder /data/data/ (this format is convenient for the project but unconvenient for other purposes, is bound to change) and launch with the following command in your terminal:**
python3 main.py
