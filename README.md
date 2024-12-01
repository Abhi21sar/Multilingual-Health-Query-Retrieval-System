# Multilingual-Health-Query-Retrieval-System

### Running the System

Install the dependencies  \
**pip install -r requirements.txt** 

Run train.py to train the BERT Model \
**python train.py**

Launch the website using \
**python main.py**

Enter your query in the search box to get top K (10 by default) similar queries in the database. 

The value of K can be altered in **test.py**.

A new database for different diseases can be created by altering the disease and medication names in **Scraping/1mg_scraping.py** and then creating a excel sheet to feed into BERT using **Scraping/data_pre_processing.py**.
