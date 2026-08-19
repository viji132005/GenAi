"""
Knowledge base seed documents for SkillBridge AI RAG system.
Contains verified curricula, career pathways, technology comparisons, and interview guidance.
"""

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "kb_ai_ml_01",
        "category": "career_guide",
        "title": "AI/ML Engineer Career Roadmap & Skill Matrix",
        "content": (
            "An AI/ML Engineer transitions theoretical machine learning models into scalable production software. "
            "Core Mathematical Foundations: Linear Algebra (matrix decomposition, eigenvalues), Multivariable Calculus "
            "(gradients, chain rule), Probability & Statistics (Bayesian inference, hypothesis testing, distributions). "
            "Programming Stack: Python (expert proficiency), NumPy, Pandas, Scikit-learn. "
            "Deep Learning Frameworks: PyTorch (industry standard for research and modern deployment), TensorFlow/Keras. "
            "MLOps & Deployment: Docker, FastAPI for model serving, MLflow/Weights & Biases for experiment tracking, "
            "ONNX runtime, Kubernetes, Cloud ML services (AWS SageMaker, Google Vertex AI). "
            "Key Projects to Stand Out: 1. End-to-End RAG system with vector databases; 2. Computer Vision / NLP pipeline with custom fine-tuning; "
            "3. Deployed Real-time Recommendation Engine with CI/CD."
        ),
        "metadata": {"career": "AI/ML Engineer", "level": "Comprehensive"}
    },
    {
        "id": "kb_data_science_01",
        "category": "career_guide",
        "title": "Data Scientist Industry Competency Framework",
        "content": (
            "Data Scientists utilize statistical analysis, exploratory data analysis (EDA), and machine learning to derive actionable business insights. "
            "Core Skill Hierarchy: 1. Advanced SQL (Window functions, CTEs, self-joins, query optimization); "
            "2. Statistical Modeling (A/B testing, regression analysis, time-series forecasting with ARIMA/Prophet); "
            "3. Machine Learning (classification, clustering, ensemble methods like XGBoost/LightGBM); "
            "4. Business Communication & Data Storytelling (translating p-values and ROC-AUC into revenue impact); "
            "5. BI Tools (Tableau, PowerBI, Streamlit for rapid prototyping). "
            "Portfolio Guidelines: Avoid generic Titanic or MNIST datasets. Use real-world messy datasets from Kaggle, government portals, or web scraping."
        ),
        "metadata": {"career": "Data Scientist", "level": "Comprehensive"}
    },
    {
        "id": "kb_fullstack_01",
        "category": "career_guide",
        "title": "Full Stack Developer Modern Web Architecture Guide",
        "content": (
            "A modern Full Stack Developer builds performant, secure, and responsive web applications from database to UI. "
            "Frontend Ecosystem: React 18+ (Hooks, Context API, state management like Zustand/Redux), Next.js (App Router, Server Components), "
            "TypeScript (type safety, generics), TailwindCSS for scalable utility-first styling, Web Vitals performance optimization. "
            "Backend Ecosystem: Node.js/Express, Python (FastAPI/Django), or Go. API design: RESTful best practices, GraphQL, WebSocket bidirectional streaming. "
            "Database & Storage: PostgreSQL/MySQL (schema design, indexing, transactions), MongoDB/Redis (caching, session store). "
            "DevOps & Security: JWT authentication, OAuth2, Docker containerization, CI/CD workflows, reverse proxies (Nginx), HTTPS and CORS compliance."
        ),
        "metadata": {"career": "Full Stack Developer", "level": "Comprehensive"}
    },
    {
        "id": "kb_backend_01",
        "category": "career_guide",
        "title": "Backend Engineering & Distributed Systems Guide",
        "content": (
            "Backend Engineers architect server-side business logic, high-throughput APIs, and reliable data storage architectures. "
            "Key Focus Areas: Concurrency and async I/O, database normalization and query execution plans, caching strategies (Write-through, Cache-aside), "
            "Message Brokers (Kafka, RabbitMQ for asynchronous event-driven decoupling), Microservices architecture, API Gateway design, "
            "Rate limiting and circuit breaker patterns, Distributed Tracing and Logging (OpenTelemetry, Prometheus, Grafana). "
            "System Design Interview Checklist: Clarify requirements, estimate capacity/QPS, define data models and API endpoints, "
            "design high-level architecture, deep dive on bottlenecks and single points of failure (SPOF)."
        ),
        "metadata": {"career": "Backend Developer", "level": "Comprehensive"}
    },
    {
        "id": "kb_cloud_devops_01",
        "category": "career_guide",
        "title": "Cloud & DevOps Engineer Competency Roadmap",
        "content": (
            "Cloud & DevOps Engineers automate software delivery, infrastructure management, and system resilience. "
            "Core Technologies: Linux command line & Bash scripting, Networking (TCP/IP, DNS, VPC, Subnets, Firewalls, Load Balancers). "
            "Infrastructure as Code (IaC): Terraform (declarative cloud provisioning), Ansible for configuration management. "
            "Containers & Orchestration: Docker containerization, Kubernetes (Pods, Services, Deployments, Ingress, Helm charts). "
            "CI/CD Pipelines: GitHub Actions, GitLab CI, Jenkins. Cloud Platforms: AWS (EC2, S3, RDS, Lambda, ECS, EKS) or GCP / Azure. "
            "Observability: Monitoring metrics, centralized logs, alerting policies."
        ),
        "metadata": {"career": "Cloud / DevOps Engineer", "level": "Comprehensive"}
    },
    {
        "id": "kb_cybersecurity_01",
        "category": "career_guide",
        "title": "Cybersecurity Analyst & Defense Engineering Guide",
        "content": (
            "Cybersecurity Analysts protect networks, infrastructure, and applications from cyber threats and unauthorized access. "
            "Foundational Knowledge: OSI 7-Layer model, TCP/IP handshake, Cryptography (Symmetric/Asymmetric encryption, RSA, AES, SHA-256, PKI). "
            "Application Security: OWASP Top 10 vulnerabilities (SQL Injection, XSS, CSRF, Broken Access Control, SSRF). "
            "Security Operations (SOC): SIEM tools (Splunk, Elastic SIEM), Log analysis, Wireshark packet capture, IDS/IPS (Snort, Suricata). "
            "Certifications for College Students: CompTIA Security+, CEH (Certified Ethical Hacker), Junior Penetration Tester (eJPT)."
        ),
        "metadata": {"career": "Cybersecurity Analyst", "level": "Comprehensive"}
    },
    {
        "id": "kb_resume_prep_01",
        "category": "interview_prep",
        "title": "ATS-Optimized Engineering Resume Standards",
        "content": (
            "Tech resumes must be clear, single-column, ATS-friendly, and impact-driven. "
            "Resume Section Structure: 1. Header (Name, Contact, LinkedIn, GitHub, Portfolio); 2. Education (Degree, College, CGPA if >7.5, Grad Year); "
            "3. Technical Skills (Languages, Frameworks, Databases, Cloud & Tools); 4. Technical Projects (3 high quality projects with GitHub & Live links); "
            "5. Experience/Internships (if any); 6. Achievements & Certifications. "
            "Writing High-Impact Bullet Points: Always use Google's XYZ formula: 'Accomplished [X], as measured by [Y], by doing [Z]'. "
            "Example Weak Bullet: 'Built a sentiment analysis app with Python.' "
            "Example Strong Bullet: 'Engineered an end-to-end sentiment analysis pipeline using PyTorch and RoBERTa on 50K+ reviews, improving classification accuracy by 14% and deploying as a sub-50ms REST API on AWS ECS.'"
        ),
        "metadata": {"category": "Resume Strategy", "level": "All"}
    },
    {
        "id": "kb_interview_star_01",
        "category": "interview_prep",
        "title": "Behavioral & Technical Interview Framework (STAR Method)",
        "content": (
            "Interviews assess problem-solving structured communication, technical depth, and cultural add. "
            "The STAR Method for Behavioral Questions: "
            "- Situation: Set the context briefly (15-20 seconds). "
            "- Task: Describe the specific engineering challenge or responsibility (15 seconds). "
            "- Action: Detail YOUR specific actions, technical trade-offs, and tools utilized (60-90 seconds). "
            "- Result: Quantify the outcome, what was delivered, and what you learned (30 seconds). "
            "Technical Coding Process: 1. Clarify constraints & edge cases; 2. State brute force approach with time/space complexity; "
            "3. Propose optimized algorithm and dry-run with test cases before writing code; 4. Code cleanly with descriptive variable names; "
            "5. Analyze Big-O time and space complexity."
        ),
        "metadata": {"category": "Interview Mastery", "level": "All"}
    }
]
