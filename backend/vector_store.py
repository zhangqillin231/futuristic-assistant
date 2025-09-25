
# backend/vector_store.py
import os
import faiss
import numpy as np
import pickle
from typing import List, Dict, Any

INDEX_PATH = os.path.join(os.path.dirname(__file__), 'faiss_index.bin')

class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = None
        self.id_map = []
        if os.path.exists(INDEX_PATH):
            self._load()
        else:
            # use IndexFlatIP for cosine (after normalizing vectors)
            self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors: List[List[float]], metadatas: List[Dict[str, Any]]):
        import numpy as np
        vecs = np.array(vectors).astype('float32')
        # normalize for cosine similarity
        faiss.normalize_L2(vecs)
        self.index.add(vecs)
        start_id = len(self.id_map)
        for i, m in enumerate(metadatas):
            self.id_map.append(m)
        self._save()
        return list(range(start_id, start_id + len(vectors)))

    def search(self, vector: List[float], top_k: int = 5):
        import numpy as np
        v = np.array([vector]).astype('float32')
        faiss.normalize_L2(v)
        D, I = self.index.search(v, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.id_map):
                continue
            meta = self.id_map[idx]
            results.append({'score': float(dist), 'metadata': meta})
        return results

    def _save(self):
        faiss.write_index(self.index, INDEX_PATH)
        # save id_map
        with open(INDEX_PATH + '.map', 'wb') as f:
            pickle.dump(self.id_map, f)

    def _load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(INDEX_PATH + '.map', 'rb') as f:
            import pickle
            self.id_map = pickle.load(f)
