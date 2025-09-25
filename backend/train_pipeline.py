
# backend/train_pipeline.py
import os
from typing import List
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from vector_store import VectorStore
import glob

# Config
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('TRAIN_DB', 'assistant_db')
EMBED_MODEL = os.environ.get('EMBED_MODEL', 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# initialize model and vector store
model = SentenceTransformer(EMBED_MODEL)
vector_store = VectorStore(dim=model.get_sentence_embedding_dimension())


def read_text_files_from_folder(folder: str):
    texts = []
    for path in glob.glob(os.path.join(folder, '**', '*.txt'), recursive=True):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            texts.append({'text': f.read(), 'source': path})
    return texts


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def index_folder(folder: str):
    docs = read_text_files_from_folder(folder)
    all_chunks = []
    meta = []
    for d in docs:
        chunks = chunk_text(d['text'])
        for i, c in enumerate(chunks):
            all_chunks.append(c)
            meta.append({'source': d['source'], 'chunk_index': i})
    if not all_chunks:
        print('No text files found to index')
        return
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)
    ids = vector_store.add(embeddings.tolist(), meta)
    # store metadata in mongo for search convenience
    entries = []
    for idx, m in zip(ids, meta):
        entries.append({'vector_id': idx, 'metadata': m})
    db.embeddings.insert_many(entries)
    print(f'Indexed {len(all_chunks)} chunks')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, required=True, help='Folder with txt files to index')
    args = parser.parse_args()
    index_folder(args.folder)
