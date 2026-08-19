import asyncio
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import engine, AsyncSessionLocal, Base
from app.models.entities import (
    User, StudentProfile, Skill, CareerProfile, CareerSkill, Resume, ResumeAnalysis,
    Roadmap, RoadmapTask, JobAnalysis, ProjectRecommendation, MockInterview,
    InterviewQuestion, InterviewResponse, InterviewReport, ProgressMetric, KnowledgeDoc
)
from app.middleware.auth import get_password_hash
from app.rag.knowledge_data import KNOWLEDGE_DOCUMENTS

CAREER_SEED_DATA = [
    {
        "title": "AI/ML Engineer",
        "category": "Artificial Intelligence",
        "description": "Designs, develops, and deploys scalable machine learning models and AI applications into production systems.",
        "average_salary": "$125,000 - $175,000",
        "growth_outlook": "35% (Extremely High)",
        "responsibilities": [
            "Train, fine-tune, and evaluate deep learning models on large datasets",
            "Optimize model inference latency and memory footprints",
            "Build robust REST/gRPC API microservices for real-time model serving",
            "Implement MLOps CI/CD pipelines with model monitoring and drift detection"
        ],
        "typical_technologies": ["Python", "PyTorch", "TensorFlow", "FastAPI", "Docker", "AWS SageMaker", "ChromaDB", "MLflow"],
        "skills": [
            {"name": "Python", "importance": "High", "min_proficiency": "Advanced", "category": "Languages"},
            {"name": "NumPy", "importance": "High", "min_proficiency": "Intermediate", "category": "Data Science"},
            {"name": "Pandas", "importance": "High", "min_proficiency": "Intermediate", "category": "Data Science"},
            {"name": "Machine Learning", "importance": "High", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "PyTorch", "importance": "High", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "TensorFlow", "importance": "Medium", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "Deep Learning", "importance": "High", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "Docker", "importance": "High", "min_proficiency": "Intermediate", "category": "DevOps"},
            {"name": "AWS", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Cloud"},
            {"name": "FastAPI", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Frameworks"},
            {"name": "SQL", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Databases"}
        ]
    },
    {
        "title": "Data Scientist",
        "category": "Data Science",
        "description": "Applies statistical modeling, machine learning, and data analysis to solve complex business challenges and extract predictive insights.",
        "average_salary": "$120,000 - $160,000",
        "growth_outlook": "28% (Very High)",
        "responsibilities": [
            "Perform exploratory data analysis and feature engineering on massive datasets",
            "Design and analyze statistical A/B tests to validate product hypotheses",
            "Develop predictive classification, regression, and forecasting models",
            "Present data-driven insights and strategic recommendations to executive stakeholders"
        ],
        "typical_technologies": ["Python", "R", "SQL", "Scikit-Learn", "Pandas", "Tableau", "XGBoost", "PostgreSQL"],
        "skills": [
            {"name": "Python", "importance": "High", "min_proficiency": "Advanced", "category": "Languages"},
            {"name": "SQL", "importance": "High", "min_proficiency": "Advanced", "category": "Databases"},
            {"name": "Statistics", "importance": "High", "min_proficiency": "Intermediate", "category": "Math"},
            {"name": "Pandas", "importance": "High", "min_proficiency": "Advanced", "category": "Data Science"},
            {"name": "Machine Learning", "importance": "High", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "Scikit-Learn", "importance": "High", "min_proficiency": "Intermediate", "category": "AI / ML"},
            {"name": "Tableau", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Data Visualization"},
            {"name": "A/B Testing", "importance": "High", "min_proficiency": "Intermediate", "category": "Analytics"}
        ]
    },
    {
        "title": "Full Stack Developer",
        "category": "Software Engineering",
        "description": "Architects and develops end-to-end web applications, encompassing intuitive user interfaces, robust backend APIs, and scalable databases.",
        "average_salary": "$105,000 - $150,000",
        "growth_outlook": "25% (Very High)",
        "responsibilities": [
            "Build responsive, high-performance web UIs with React and modern CSS",
            "Design secure, RESTful and GraphQL backend microservices",
            "Manage relational and NoSQL database schemas, queries, and migrations",
            "Configure authentication, containerization, and automated CI/CD deployments"
        ],
        "typical_technologies": ["JavaScript", "TypeScript", "React", "Next.js", "Node.js", "Express", "PostgreSQL", "TailwindCSS", "Docker", "Git"],
        "skills": [
            {"name": "JavaScript", "importance": "High", "min_proficiency": "Advanced", "category": "Languages"},
            {"name": "TypeScript", "importance": "High", "min_proficiency": "Intermediate", "category": "Languages"},
            {"name": "React", "importance": "High", "min_proficiency": "Advanced", "category": "Frontend"},
            {"name": "Node.js", "importance": "High", "min_proficiency": "Intermediate", "category": "Backend"},
            {"name": "HTML/CSS", "importance": "High", "min_proficiency": "Advanced", "category": "Frontend"},
            {"name": "TailwindCSS", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Frontend"},
            {"name": "SQL", "importance": "High", "min_proficiency": "Intermediate", "category": "Databases"},
            {"name": "PostgreSQL", "importance": "High", "min_proficiency": "Intermediate", "category": "Databases"},
            {"name": "Docker", "importance": "Medium", "min_proficiency": "Intermediate", "category": "DevOps"},
            {"name": "Git", "importance": "High", "min_proficiency": "Advanced", "category": "Tools"}
        ]
    },
    {
        "title": "Backend Developer",
        "category": "Software Engineering",
        "description": "Specializes in building high-throughput, low-latency server-side business logic, distributed data pipelines, and scalable APIs.",
        "average_salary": "$115,000 - $160,000",
        "growth_outlook": "22% (High)",
        "responsibilities": [
            "Architect high-concurrency RESTful and asynchronous event-driven backend systems",
            "Optimize database indexing, query execution plans, and caching layers with Redis",
            "Implement secure authentication, authorization, and rate limiting protocols",
            "Monitor system performance, logging, and error tracing in production"
        ],
        "typical_technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker", "Kafka", "Linux", "Git"],
        "skills": [
            {"name": "Python", "importance": "High", "min_proficiency": "Advanced", "category": "Languages"},
            {"name": "FastAPI", "importance": "High", "min_proficiency": "Intermediate", "category": "Frameworks"},
            {"name": "SQL", "importance": "High", "min_proficiency": "Advanced", "category": "Databases"},
            {"name": "PostgreSQL", "importance": "High", "min_proficiency": "Intermediate", "category": "Databases"},
            {"name": "Redis", "importance": "High", "min_proficiency": "Intermediate", "category": "Databases"},
            {"name": "Docker", "importance": "High", "min_proficiency": "Intermediate", "category": "DevOps"},
            {"name": "System Design", "importance": "High", "min_proficiency": "Intermediate", "category": "Architecture"},
            {"name": "Git", "importance": "High", "min_proficiency": "Advanced", "category": "Tools"}
        ]
    },
    {
        "title": "Data Analyst",
        "category": "Data Science",
        "description": "Transforms raw transactional and business data into actionable dashboards, KPIs, and executive reporting.",
        "average_salary": "$80,000 - $115,000",
        "growth_outlook": "23% (High)",
        "responsibilities": [
            "Write complex SQL queries to clean, aggregate, and join disparate data tables",
            "Design executive interactive dashboards in Tableau and PowerBI",
            "Perform variance analysis and business cohort tracking",
            "Collaborate with product and finance teams on KPI reporting"
        ],
        "typical_technologies": ["SQL", "Excel", "Tableau", "PowerBI", "Python", "Pandas"],
        "skills": [
            {"name": "SQL", "importance": "High", "min_proficiency": "Advanced", "category": "Databases"},
            {"name": "Excel", "importance": "High", "min_proficiency": "Advanced", "category": "Tools"},
            {"name": "Tableau", "importance": "High", "min_proficiency": "Intermediate", "category": "Visualization"},
            {"name": "PowerBI", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Visualization"},
            {"name": "Python", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Languages"},
            {"name": "Pandas", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Data Science"}
        ]
    },
    {
        "title": "Cloud / DevOps Engineer",
        "category": "Infrastructure",
        "description": "Automates cloud infrastructure deployment, manages container orchestration, and optimizes CI/CD delivery pipelines.",
        "average_salary": "$120,000 - $170,000",
        "growth_outlook": "30% (Very High)",
        "responsibilities": [
            "Provision cloud resources declaratively using Terraform Infrastructure as Code",
            "Manage Kubernetes cluster deployments, scaling policies, and ingress controllers",
            "Build automated CI/CD pipelines with GitHub Actions and automated test gates",
            "Enforce security compliance, cloud networking VPCs, and cost optimization"
        ],
        "typical_technologies": ["Linux", "Docker", "Kubernetes", "AWS", "Terraform", "GitHub Actions", "Bash"],
        "skills": [
            {"name": "Linux", "importance": "High", "min_proficiency": "Advanced", "category": "OS"},
            {"name": "Docker", "importance": "High", "min_proficiency": "Advanced", "category": "DevOps"},
            {"name": "Kubernetes", "importance": "High", "min_proficiency": "Intermediate", "category": "DevOps"},
            {"name": "AWS", "importance": "High", "min_proficiency": "Intermediate", "category": "Cloud"},
            {"name": "Terraform", "importance": "High", "min_proficiency": "Intermediate", "category": "IaC"},
            {"name": "CI/CD", "importance": "High", "min_proficiency": "Intermediate", "category": "DevOps"},
            {"name": "Git", "importance": "High", "min_proficiency": "Advanced", "category": "Tools"}
        ]
    },
    {
        "title": "Cybersecurity Analyst",
        "category": "Security",
        "description": "Safeguards digital infrastructure, networks, and applications by detecting vulnerabilities and responding to security incidents.",
        "average_salary": "$110,000 - $155,000",
        "growth_outlook": "32% (Extremely High)",
        "responsibilities": [
            "Monitor Security Operations Center (SOC) telemetry and investigate alerts",
            "Perform vulnerability assessments and web application penetration testing",
            "Enforce zero-trust architecture and identity management (IAM) policies",
            "Conduct incident response, forensic analysis, and compliance reporting"
        ],
        "typical_technologies": ["Wireshark", "Splunk", "Linux", "OWASP Top 10", "Python", "Nmap", "Metasploit"],
        "skills": [
            {"name": "Network Security", "importance": "High", "min_proficiency": "Intermediate", "category": "Security"},
            {"name": "OWASP Top 10", "importance": "High", "min_proficiency": "Intermediate", "category": "Security"},
            {"name": "Linux", "importance": "High", "min_proficiency": "Intermediate", "category": "OS"},
            {"name": "Wireshark", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Tools"},
            {"name": "Cryptography", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Security"},
            {"name": "Python", "importance": "Medium", "min_proficiency": "Intermediate", "category": "Languages"}
        ]
    }
]

async def seed_database():
    """Seed initial demo user, student profile, career taxonomy, and knowledge base."""
    async with AsyncSessionLocal() as db:
        # 1. Create Tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # 2. Check if Careers already exist
        q_c = select(CareerProfile)
        res_c = await db.execute(q_c)
        if not res_c.scalars().first():
            print("[SEED] Seeding Career Profiles and taxonomy...")
            for c_data in CAREER_SEED_DATA:
                career = CareerProfile(
                    title=c_data["title"],
                    category=c_data["category"],
                    description=c_data["description"],
                    average_salary=c_data["average_salary"],
                    growth_outlook=c_data["growth_outlook"],
                    responsibilities=c_data["responsibilities"],
                    typical_technologies=c_data["typical_technologies"]
                )
                db.add(career)
                await db.flush()

                for s_data in c_data["skills"]:
                    c_skill = CareerSkill(
                        career_id=career.id,
                        skill_name=s_data["name"],
                        category=s_data["category"],
                        importance_level=s_data["importance"],
                        min_proficiency=s_data["min_proficiency"],
                        learning_resources=[
                            {"title": f"Official {s_data['name']} Docs", "url": f"https://docs.google.com/search?q={s_data['name']}"},
                            {"title": f"Interactive {s_data['name']} Tutorial", "url": "https://coursera.org"}
                        ]
                    )
                    db.add(c_skill)

            await db.commit()

        # 3. Seed Knowledge Base Docs
        q_k = select(KnowledgeDoc)
        res_k = await db.execute(q_k)
        if not res_k.scalars().first():
            print("[SEED] Seeding RAG Knowledge Base...")
            for doc in KNOWLEDGE_DOCUMENTS:
                db_doc = KnowledgeDoc(
                    category=doc["category"],
                    title=doc["title"],
                    content=doc["content"],
                    metadata_json=doc.get("metadata", {})
                )
                db.add(db_doc)
            await db.commit()

        # 4. Seed Demo User (Rahul)
        q_u = select(User).where(User.email == "demo@skillbridge.ai")
        res_u = await db.execute(q_u)
        demo_user = res_u.scalar_one_or_none()

        if not demo_user:
            print("[SEED] Seeding Demo User (Rahul)...")
            demo_user = User(
                email="demo@skillbridge.ai",
                hashed_password=get_password_hash("password123"),
                full_name="Rahul Sharma",
                role="student",
                is_active=True
            )
            db.add(demo_user)
            await db.flush()

            # Profile
            demo_profile = StudentProfile(
                user_id=demo_user.id,
                college="National Institute of Technology",
                degree="B.E.",
                branch="Computer Science & Engineering",
                semester=6,
                graduation_year=2026,
                cgpa=7.8,
                target_career="AI/ML Engineer",
                interests=["Artificial Intelligence", "Machine Learning", "Web Development", "Cloud Computing"],
                coursework=[
                    "Data Structures & Algorithms",
                    "Database Management Systems",
                    "Operating Systems",
                    "Computer Networks",
                    "Object-Oriented Programming",
                    "Probability & Statistics"
                ],
                certifications=[
                    {"name": "Python for Data Science", "issuer": "Coursera", "year": 2025},
                    {"name": "SQL Foundations", "issuer": "HackerRank", "year": 2025}
                ],
                experience=[
                    {
                        "role": "Web Development Intern",
                        "company": "TechStart Solutions",
                        "duration": "May 2025 - July 2025",
                        "description": "Developed REST API endpoints using Python and built responsive dashboards with React."
                    }
                ],
                achievements=[
                    "Finalist at University Hackathon 2025 (Smart Campus AI project)",
                    "Solved 150+ LeetCode problems in Python and C++"
                ],
                onboarding_completed=True
            )
            db.add(demo_profile)
            await db.flush()

            # Skills
            initial_skills = [
                {"name": "Python", "category": "Languages", "proficiency_level": "Intermediate"},
                {"name": "SQL", "category": "Databases", "proficiency_level": "Intermediate"},
                {"name": "HTML", "category": "Frontend", "proficiency_level": "Intermediate"},
                {"name": "CSS", "category": "Frontend", "proficiency_level": "Intermediate"},
                {"name": "JavaScript", "category": "Languages", "proficiency_level": "Intermediate"},
                {"name": "Machine Learning", "category": "AI / ML", "proficiency_level": "Beginner"}
            ]
            for s in initial_skills:
                db_skill = Skill(
                    profile_id=demo_profile.id,
                    name=s["name"],
                    category=s["category"],
                    proficiency_level=s["proficiency_level"],
                    verified=True
                )
                db.add(db_skill)

            # Sample Resume
            sample_resume = Resume(
                user_id=demo_user.id,
                filename="Rahul_Sharma_Resume.pdf",
                file_path="./uploads/demo_rahul_resume.pdf",
                raw_text=(
                    "Rahul Sharma\nEmail: demo@skillbridge.ai | Phone: +91 9876543210\n"
                    "Education: B.E. in Computer Science & Engineering, National Institute of Technology (2022-2026), CGPA: 7.8/10\n"
                    "Skills: Python, SQL, HTML, CSS, JavaScript, Basic Machine Learning, Git\n"
                    "Projects:\n"
                    "1. Student Academic Risk Predictor: Developed a machine learning classification model using Scikit-Learn to identify students at academic risk.\n"
                    "2. Full Stack Portfolio & Blog: Built a responsive personal web application with React and Python FastAPI with JWT authentication.\n"
                    "Experience: Web Dev Intern at TechStart Solutions (Summer 2025) - Contributed to backend API endpoints and bug fixing."
                )
            )
            db.add(sample_resume)
            await db.flush()

            sample_resume_analysis = ResumeAnalysis(
                resume_id=sample_resume.id,
                user_id=demo_user.id,
                overall_score=74.0,
                ats_score=76.0,
                skills_score=72.0,
                experience_score=68.0,
                project_score=75.0,
                formatting_score=84.0,
                strengths=[
                    "Clear standard single-column layout readable by ATS scanners",
                    "Strong foundational skills in Python and SQL clearly stated",
                    "Practical internship experience listed with relevant timeline"
                ],
                weaknesses=[
                    "Project bullets explain what was built but lack quantitative metrics and impact numbers",
                    "Missing live demo links and GitHub repository URLs",
                    "Missing deep learning and containerization tools required for AI/ML Engineer roles"
                ],
                suggestions=[
                    "Rewrite project bullets using the Google XYZ formula ('Accomplished [X] as measured by [Y] by doing [Z]')",
                    "Highlight metrics such as model accuracy %, dataset volume, and API response latency",
                    "Add PyTorch and Docker to your skills section as you complete roadmap modules"
                ],
                improved_bullets=[
                    {
                        "original": "Developed a machine learning classification model using Scikit-Learn to identify students at academic risk.",
                        "improved": "Engineered an end-to-end classification pipeline with Scikit-Learn on 10,000+ student academic records, achieving 88% ROC-AUC and reducing identification latency by 35%.",
                        "rationale": "Quantifies dataset volume, accuracy metric, and performance improvement."
                    }
                ],
                missing_elements=["Live hosted portfolio URLs", "Quantified performance metrics", "PyTorch / Deep Learning projects"]
            )
            db.add(sample_resume_analysis)

            # Sample Roadmap
            demo_roadmap = Roadmap(
                user_id=demo_user.id,
                career_title="AI/ML Engineer",
                title="AI/ML Engineer Personalized Career Roadmap",
                target_duration_months=6,
                completion_percentage=43.0,
                overview_summary="A targeted 6-month roadmap designed to transition from core Python skills to production-ready AI/ML engineering."
            )
            db.add(demo_roadmap)
            await db.flush()

            demo_tasks = [
                {
                    "phase_number": 1, "phase_name": "Phase 1: Python & Math Foundations",
                    "task_title": "Advanced Python & Linear Algebra for ML", "estimated_hours": 20,
                    "is_completed": True, "sort_order": 1,
                    "skills_covered": ["Python", "NumPy", "Linear Algebra"],
                    "description": "Master vector math, matrix decomposition, autograd basics, and performant NumPy array manipulations."
                },
                {
                    "phase_number": 2, "phase_name": "Phase 2: Core Machine Learning Mastery",
                    "task_title": "Applied Scikit-Learn & Feature Engineering", "estimated_hours": 25,
                    "is_completed": True, "sort_order": 2,
                    "skills_covered": ["Scikit-Learn", "Pandas", "Feature Engineering"],
                    "description": "Build classification, regression, and cross-validation pipelines with hyperparameter tuning."
                },
                {
                    "phase_number": 3, "phase_name": "Phase 3: Deep Learning Frameworks",
                    "task_title": "PyTorch Neural Networks & Transformers", "estimated_hours": 35,
                    "is_completed": False, "sort_order": 3,
                    "skills_covered": ["PyTorch", "Deep Learning", "Transformers"],
                    "description": "Implement custom loss functions, training loops, CNNs, and fine-tune Transformer architectures."
                },
                {
                    "phase_number": 4, "phase_name": "Phase 4: MLOps & Production Serving",
                    "task_title": "FastAPI Model Microservices & Docker", "estimated_hours": 30,
                    "is_completed": False, "sort_order": 4,
                    "skills_covered": ["FastAPI", "Docker", "MLOps"],
                    "description": "Containerize deep learning models, configure batching, and serve REST endpoints with sub-80ms latency."
                },
                {
                    "phase_number": 5, "phase_name": "Phase 5: Capstone GenAI Portfolio Project",
                    "task_title": "End-to-End RAG System with Vector Database", "estimated_hours": 40,
                    "is_completed": False, "sort_order": 5,
                    "skills_covered": ["RAG", "ChromaDB", "LangChain", "React"],
                    "description": "Design an autonomous research assistant with document chunking, semantic retrieval, and citations."
                },
                {
                    "phase_number": 6, "phase_name": "Phase 6: Technical Interview Preparation",
                    "task_title": "Mock Interviews & System Design Practice", "estimated_hours": 15,
                    "is_completed": False, "sort_order": 6,
                    "skills_covered": ["Interview Prep", "System Design", "STAR Method"],
                    "description": "Complete 5 mock technical interview rounds and practice behavioral STAR answers."
                }
            ]

            for t in demo_tasks:
                db_t = RoadmapTask(
                    roadmap_id=demo_roadmap.id,
                    phase_number=t["phase_number"],
                    phase_name=t["phase_name"],
                    task_title=t["task_title"],
                    description=t["description"],
                    skills_covered=t["skills_covered"],
                    learning_resources=[
                        {"title": f"Official {t['skills_covered'][0]} Guide", "url": "https://docs.python.org"},
                        {"title": "Interactive Hands-on Practice", "url": "https://coursera.org"}
                    ],
                    project_checkpoint="Build and verify working demonstration module.",
                    estimated_hours=t["estimated_hours"],
                    is_completed=t["is_completed"],
                    completed_at=datetime.datetime.utcnow() if t["is_completed"] else None,
                    sort_order=t["sort_order"]
                )
                db.add(db_t)

            # Sample Mock Interview
            demo_interview = MockInterview(
                user_id=demo_user.id,
                career_title="AI/ML Engineer",
                interview_type="Technical",
                difficulty="Intermediate",
                total_questions=3,
                status="completed",
                current_question_index=3,
                overall_score=76.0,
                technical_score=74.0,
                communication_score=80.0,
                completed_at=datetime.datetime.utcnow()
            )
            db.add(demo_interview)
            await db.flush()

            demo_report = InterviewReport(
                interview_id=demo_interview.id,
                user_id=demo_user.id,
                overall_score=76.0,
                technical_score=74.0,
                communication_score=80.0,
                rubric_breakdown={
                    "Problem Solving": {"score": 75.0, "comment": "Good grasp of bias-variance tradeoff and regularization."},
                    "Technical Depth": {"score": 73.0, "comment": "Solid understanding of ML foundations; strengthen deep learning details."},
                    "Clarity & Delivery": {"score": 82.0, "comment": "Clear, structured technical communication."}
                },
                strengths=[
                    "Accurate explanation of bias-variance tradeoff and L1/L2 penalties",
                    "Strong communication using proper technical terminology",
                    "Good structured thought process on debugging model drift"
                ],
                weaknesses=[
                    "Could explain attention computational complexity in greater depth",
                    "Practice discussing memory constraints on GPU batching"
                ],
                improvement_suggestions=[
                    "Review Transformer self-attention mathematical matrix operations",
                    "Practice dry-running algorithms before stating final conclusions"
                ],
                recommended_topics=["PyTorch Autograd", "Transformer Attention", "MLOps Model Monitoring"]
            )
            db.add(demo_report)

            # Progress Metrics Timeline
            progress_history = [
                {"date": "Month 1", "readiness": 42.0, "skill": 45.0, "resume": 58.0, "interview": 40.0, "roadmap": 15.0},
                {"date": "Month 2", "readiness": 51.0, "skill": 58.0, "resume": 65.0, "interview": 48.0, "roadmap": 28.0},
                {"date": "Month 3", "readiness": 63.0, "skill": 70.0, "resume": 71.0, "interview": 55.0, "roadmap": 38.0},
                {"date": "Month 4 (Current)", "readiness": 68.0, "skill": 78.0, "resume": 74.0, "interview": 61.0, "roadmap": 43.0}
            ]
            for p in progress_history:
                db_p = ProgressMetric(
                    user_id=demo_user.id,
                    recorded_date=p["date"],
                    career_readiness=p["readiness"],
                    skill_completion=p["skill"],
                    resume_score=p["resume"],
                    interview_readiness=p["interview"],
                    roadmap_progress=p["roadmap"],
                    active_career_match=82.0
                )
                db.add(db_p)

            await db.commit()
            print("[SEED] Database successfully seeded with Rahul demo profile and career taxonomy!")

if __name__ == "__main__":
    asyncio.run(seed_database())
