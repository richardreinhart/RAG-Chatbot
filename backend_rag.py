import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


def load_company_rules(filename="PERATURAN PERUSAHAAN ABC.txt", chunk_size=100, overlap_size=50):

    with open(filename, "r", encoding="utf-8") as f:
        policy_text = f.read()
    
    words = policy_text.split()

    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunk_text = ' '.join(chunk)
        chunks.append(chunk_text)
        start = start + chunk_size - overlap_size

    return chunks

def create_embeddings(chunks):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_embeddings = embedder.encode(chunks, convert_to_numpy=True)
    return chunk_embeddings

def create_faiss_index(embeddings):
    embedding_dim = embeddings.shape[1]  
    index = faiss.IndexFlatL2(embedding_dim)  
    index.add(embeddings)  
    return index

company_rules = load_company_rules("PERATURAN PERUSAHAAN ABC.txt")
policy_embeddings = create_embeddings(company_rules)
faiss_index = create_faiss_index(policy_embeddings)

def retrieve_relevant_context(user_input, top_k=3):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = embedder.encode([user_input], convert_to_numpy=True)  
    distances, indices = faiss_index.search(query_embedding, top_k)  
    
    if distances[0][0] <= 1:
        relevant_context = [company_rules[idx] for idx in indices[0]]  
    else:
        relevant_context = []

    return " ".join(relevant_context)

def GenerateResponse(input, history=[]):
    relevant_context = retrieve_relevant_context(input)

    if relevant_context == "":
        prompt_parts = []
        for pair in history:
            prompt_parts.append(f"user: {pair['user']}")
            prompt_parts.append(f"assistant: {pair['assistant']}")

        prompt_parts.append(f"user: {input}")
        prompt_parts.append("assistant:")

        response = model.generate_content(prompt_parts)
        return response.text
    
    else:
        prompt_parts = []
        for pair in history:
            prompt_parts.append(f"user: {pair['user']}")
            prompt_parts.append(f"assistant: {pair['assistant']}")

        prompt_parts.append(f"user: {input}")
        prompt_parts.append(f"context: {relevant_context}")
        prompt_parts.append("assistant:")

        response = model.generate_content(prompt_parts)
        return response.text


