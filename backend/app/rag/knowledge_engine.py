import logging
import math
from typing import List, Dict, Any, Optional
import numpy as np

from app.rag.knowledge_data import KNOWLEDGE_DOCUMENTS
from app.ai.factory import get_llm_provider

logger = logging.getLogger("skillbridge.rag.engine")

class KnowledgeEngine:
    """
    Retrieval-Augmented Generation (RAG) Engine for SkillBridge AI.
    Performs vector indexing, semantic search, and context grounding.
    """

    def __init__(self):
        self.documents: List[Dict[str, Any]] = list(KNOWLEDGE_DOCUMENTS)
        self.embeddings: Dict[str, List[float]] = {}
        self._is_indexed = False

    async def initialize_index(self):
        """Precompute or load embeddings for knowledge base documents."""
        if self._is_indexed:
            return

        provider = get_llm_provider()
        texts = [f"{doc['title']}: {doc['content']}" for doc in self.documents]
        
        try:
            vectors = await provider.get_embeddings(texts)
            for doc, vec in zip(self.documents, vectors):
                self.embeddings[doc["id"]] = vec
            self._is_indexed = True
            logger.info(f"RAG Knowledge Engine indexed {len(self.documents)} documents successfully.")
        except Exception as e:
            logger.warning(f"Embedding indexing fallback enabled: {e}")
            self._is_indexed = True

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        a = np.array(v1, dtype=np.float32)
        b = np.array(v2, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def _keyword_similarity(self, query: str, content: str) -> float:
        import re
        q_tokens = set(re.findall(r"\w+", query.lower()))
        c_tokens = set(re.findall(r"\w+", content.lower()))
        if not q_tokens or not c_tokens:
            return 0.0
        stop_words = {"a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of", "with", "is", "are", "what", "how", "do", "i", "my", "me", "should", "can", "tell"}
        meaningful_q = {t for t in q_tokens if t not in stop_words and len(t) > 1}
        if not meaningful_q:
            meaningful_q = q_tokens
        overlap = meaningful_q.intersection(c_tokens)
        return len(overlap) / math.sqrt(len(meaningful_q) * len(c_tokens))

    async def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for most relevant knowledge documents given a query string.
        Combines vector semantic similarity with keyword matching.
        """
        if not self._is_indexed:
            await self.initialize_index()

        provider = get_llm_provider()
        query_vector = None
        try:
            q_vectors = await provider.get_embeddings([query])
            if q_vectors:
                query_vector = q_vectors[0]
        except Exception as e:
            logger.warning(f"Could not compute query vector, using keyword search: {e}")

        scored_results = []
        for doc in self.documents:
            doc_id = doc["id"]
            combined_text = f"{doc['title']} {doc['content']}"
            
            score = 0.0
            if query_vector and doc_id in self.embeddings:
                sim = self._cosine_similarity(query_vector, self.embeddings[doc_id])
                score += sim * 0.7
            
            kw_sim = self._keyword_similarity(query, combined_text)
            score += kw_sim * 0.3

            scored_results.append({
                "id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "content": doc["content"],
                "metadata": doc.get("metadata", {}),
                "score": round(score, 4)
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]

    async def get_grounded_context(self, query: str, top_k: int = 3) -> str:
        """Format retrieved search results into a clean context string for LLM prompts."""
        results = await self.search(query, top_k=top_k)
        if not results:
            return "No specific knowledge base context found."

        context_blocks = []
        for idx, r in enumerate(results, 1):
            context_blocks.append(
                f"[Source {idx}: {r['title']} ({r['category']})]\n{r['content']}"
            )
        return "\n\n".join(context_blocks)

# Global singleton
knowledge_engine = KnowledgeEngine()
