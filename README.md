# Multilingual Health Query Retrieval System

This project is a **Multilingual Health Query Retrieval System** that uses a fine-tuned **BERT model** to retrieve health-related queries based on user input. It supports multiple languages and provides the top **K similar queries** from a database.

---

## Features
- **Multilingual Query Support**: Allows input queries in multiple languages.
- **BERT-based Query Similarity**: Leverages a pre-trained BERT model to compute similarity scores between user queries and a database.
- **Customizable Database**: Easily replace or update the database with new health-related data using the provided scripts.
- **Interactive Web Interface**: A user-friendly interface for query input and retrieval.
- **Scalable Design**: Efficient handling of large query databases for real-time performance.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<Abhi21sar>/Multilingual-Health-Query-Retrieval-System.git
cd Multilingual-Health-Query-Retrieval-System

pip install -r requirements.txt
python train.py
python main.py
