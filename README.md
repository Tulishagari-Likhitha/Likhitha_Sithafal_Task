# Task_2
Chat with Website Using RAG Pipeline

# Chat with Website Using RAG Pipeline

This project allows you to scrape multiple websites, index their content, and then interact with the indexed data through a question-answer interface powered by a Retrieval-Augmented Generation (RAG) pipeline. The system uses the FAISS library for efficient similarity search, Sentence Transformers for embedding generation, and OpenAI GPT-4 for generating responses to queries.

## Features

- Scrape content from multiple websites.
- Break down content into smaller chunks for indexing.
- Use FAISS for efficient search and retrieval of relevant content.
- Generate context-based responses using OpenAI GPT-4.
- Concurrent processing of multiple websites for faster scraping and indexing.
- Save and load FAISS index and metadata for persistent storage.

## Technologies Used

- **requests**: For scraping content from websites.
- **BeautifulSoup**: For parsing HTML content from the scraped websites.
- **Sentence-Transformers**: For generating sentence embeddings from the website content.
- **FAISS**: For efficient similarity search and indexing of embeddings.
- **OpenAI GPT-4**: For generating answers based on the queried content.
- **Streamlit**: For building a simple user interface.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bunnyrajender55/-Chat-with-Website-Using-RAG-Pipeline.git
   cd chat-with-website-using-rag-pipeline
Install the required dependencies:

2.pip install -r requirements.txt
3.Set up your OpenAI API key by replacing OPENAI_API_KEY in the code with your actual API key.

## Usage
Run the Streamlit app:

streamlit run app.py
Enter one or more website URLs in the provided text area.

After processing and indexing the websites, input a query related to the website content.

The system will return a response based on the indexed content and your query.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


Make sure to update the repository link and other details based on your setup.
