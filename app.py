import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import openai
import numpy as np
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import time
import pickle

openai.api_key = "OPENAI_API_KEY"

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

dimension = 384
index = faiss.IndexFlatL2(dimension)

metadata = []

def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        text = "\n".join([tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li', 'span', 'a'])])
        
        chunk_size = max(200, len(text) // 10)
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        return chunks
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def index_chunks(chunks, doc_name):
    embeddings = embedding_model.encode(chunks)
    index.add(np.array(embeddings))
    for chunk in chunks:
        metadata.append({'content': chunk, 'doc_name': doc_name})

def process_multiple_websites(urls):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_website, url) for url in urls]
        for future, url in zip(futures, urls):
            chunks = future.result()
            if chunks:
                doc_name = url.split("//")[-1]
                index_chunks(chunks, doc_name)

def save_index():
    faiss.write_index(index, "faiss_index.index")
    with open("metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

def load_index():
    global index, metadata
    index = faiss.read_index("faiss_index.index")
    with open("metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

def detect_intent(query):
    if "compare" in query.lower():
        return "comparison"
    elif "summarize" in query.lower():
        return "summary"
    return "general"

def query_content(query):
    intent = detect_intent(query)
    query_embedding = embedding_model.encode(query)
    D, I = index.search(np.array([query_embedding]), k=5)
    results = [metadata[i] for i in I[0] if 0 <= i < len(metadata)]
    return results, intent

def generate_prompt(query, results, intent):
    context = "\n".join([f"Source ({r['doc_name']}): {r['content']}" for r in results])
    if intent == "comparison":
        return f"Compare the following information:\n\nContext:\n{context}\n\nQuery:\n{query}"
    return f"Answer the following query based on the context:\n\nContext:\n{context}\n\nQuery:\n{query}"

def generate_response(query, results, intent):
    prompt = generate_prompt(query, results, intent)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

st.title("Chat with Website Using RAG Pipeline")

urls = st.text_area("Enter website URLs (one per line):").splitlines()
if urls:
    process_multiple_websites(urls)
    save_index()
    st.success("Websites processed and indexed successfully!")

query = st.text_input("Ask a question about the websites:")
if query:
    results, intent = query_content(query)
    response = generate_response(query, results, intent)
    st.write("### Response:")
    st.write(response)
