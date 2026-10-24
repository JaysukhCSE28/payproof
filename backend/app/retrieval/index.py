"""BM25 keyword indexer for policy clauses with native pure-Python fallback."""

import math
import re
from collections import Counter
from typing import List, Dict, Any, Optional

try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None


class FallbackBM25:
    """Pure-Python BM25 implementation when rank-bm25 is not installed."""

    def __init__(self, corpus_tokens: List[List[str]], k1: float = 1.5, b: float = 0.75):
        self.corpus_size = len(corpus_tokens)
        self.avgdl = sum(len(doc) for doc in corpus_tokens) / self.corpus_size if self.corpus_size > 0 else 0
        self.doc_freqs: List[Counter] = [Counter(doc) for doc in corpus_tokens]
        self.doc_lens = [len(doc) for doc in corpus_tokens]
        self.k1 = k1
        self.b = b
        self.nd: Dict[str, int] = {}
        for doc in self.doc_freqs:
            for word in doc.keys():
                self.nd[word] = self.nd.get(word, 0) + 1
        self.idf: Dict[str, float] = {}
        for word, freq in self.nd.items():
            self.idf[word] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def get_scores(self, query: List[str]) -> List[float]:
        scores = [0.0] * self.corpus_size
        for q in query:
            q_idf = self.idf.get(q, 0.0)
            if q_idf <= 0:
                continue
            for idx in range(self.corpus_size):
                freq = self.doc_freqs[idx].get(q, 0)
                if freq == 0:
                    continue
                denom = freq + self.k1 * (1 - self.b + self.b * (self.doc_lens[idx] / (self.avgdl or 1)))
                scores[idx] += q_idf * (freq * (self.k1 + 1)) / (denom or 1)
        return scores


class ClauseIndex:
    def __init__(self, clauses: List[Dict[str, Any]]):
        self.clauses = clauses
        self.corpus_tokens = [self._tokenize(c["text"] + " " + " ".join(c.get("tags", []))) for c in clauses]
        if BM25Okapi is not None and self.corpus_tokens:
            self.bm25 = BM25Okapi(self.corpus_tokens)
        elif self.corpus_tokens:
            self.bm25 = FallbackBM25(self.corpus_tokens)
        else:
            self.bm25 = None

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return top_k matching clauses ranked by BM25 score."""
        if not self.bm25 or not self.clauses:
            return []
        tokens = self._tokenize(query)
        if not tokens:
            return self.clauses[:top_k]
        scores = self.bm25.get_scores(tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self.clauses[i] for i in ranked_indices if scores[i] > 0][:top_k]

