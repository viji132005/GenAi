# SkillBridge AI — Retrieval-Augmented Generation (RAG) Engine

SkillBridge AI incorporates a domain-specific Retrieval-Augmented Generation (RAG) system to ground AI counseling, interview questions, and curriculum advice in verified engineering standards.

---

## Architecture of RAG Engine

```
                                 [ Student Prompt / Question ]
                                              |
                                              v
+-----------------------------------------------------------------------------------+
|                            RETRIEVAL PIPELINE                                     |
|                                                                                   |
|  1. Query Tokenization & Term Vectorization                                       |
|  2. Semantic Cosine Similarity against In-Memory Knowledge Corpus                 |
|  3. Top-K Document Ranking & Threshold Filtering (K=3)                            |
+-------------------------------------+---------------------------------------------+
                                      |
                                      v Retrieved Context Documents
+-----------------------------------------------------------------------------------+
|                            AUGMENTATION PIPELINE                                  |
|                                                                                   |
|  Inject Student Profile (Semester, Target Role, Validated Skills, Deficits)        |
|  + Retrieved RAG Citations & Recommended Frameworks                               |
|  + System Instruction Grounding Rules                                             |
+-------------------------------------+---------------------------------------------+
                                      |
                                      v Enhanced Grounded Prompt
+-----------------------------------------------------------------------------------+
|                            GENERATION PIPELINE                                    |
|                                                                                   |
|  LLM Provider (Google Gemini / OpenAI / SkillBridge-LLM)                          |
|  └── Synthesizes tailored response with transparent citation snippets            |
+-----------------------------------------------------------------------------------+
```

---

## Domain Knowledge Corpus

The RAG index (`backend/app/rag/knowledge_data.py`) contains pre-indexed engineering curricula and placement guides across:
1. **AI/ML Engineering Core Path**: PyTorch, deep learning, data pipelines, model serving (FastAPI/Docker), ML lifecycle.
2. **Full Stack Engineering Roadmap**: React, Node.js/Python backend, PostgreSQL, REST/GraphQL, modern deployment.
3. **Data Science & Analytics Curriculum**: Pandas, SQL aggregation, statistical modeling, Scikit-Learn, data visualization.
4. **Cloud DevOps & Infrastructure Roadmap**: Docker containerization, Kubernetes, CI/CD pipelines, AWS/GCP architecture.
5. **Cybersecurity Operations Guide**: Network security, OWASP Top 10, penetration testing, SIEM logging.
6. **Technical Interview Preparation Guidelines**: Data structures, algorithmic complexity, STAR behavioral responses.
7. **Google XYZ Resume Bullet Writing Guide**: Quantifiable impact formulation for software engineers.
8. **Student Capstone Project Guidelines**: Production project staging from data ingestion to containerized deployment.

---

## Transparent Source Citations

When students ask questions in the Career Assistant, the platform displays the exact knowledge documents cited, enabling transparent, fact-checked learning recommendations.
