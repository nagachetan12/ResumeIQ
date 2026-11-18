
import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path(__file__).parent / "interview_questions.db"


def setup_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # 1. Career roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # 2. Skills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT UNIQUE NOT NULL,
            category TEXT,
            description TEXT
        )
    """)

    # 3. Skills required for each career
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS role_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            skill_id INTEGER,
            importance TEXT,
            FOREIGN KEY (role_id) REFERENCES career_roles(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id),
            UNIQUE(role_id, skill_id)
        )
    """)

    # 4. Personalized learning roadmap
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_roadmap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            skill_id INTEGER,
            learning_order INTEGER,
            estimated_days INTEGER,
            FOREIGN KEY (role_id) REFERENCES career_roles(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id)
        )
    """)

    # 5. Interview questions and answers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT,
            difficulty TEXT,
            FOREIGN KEY (role_id) REFERENCES career_roles(id)
        )
    """)

    # 6. Learning resources
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_id INTEGER,
            resource_name TEXT,
            resource_url TEXT,
            resource_type TEXT,
            FOREIGN KEY (skill_id) REFERENCES skills(id)
        )
    """)

    # 7. Practical project recommendations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            project_name TEXT,
            description TEXT,
            difficulty TEXT,
            FOREIGN KEY (role_id) REFERENCES career_roles(id)
        )
    """)

    
# 8. Resume history and version management
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            resume_filename TEXT NOT NULL,
            ats_score INTEGER,
            skills_count INTEGER,
            resume_text TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Add user_id to existing databases without deleting records
    cursor.execute("PRAGMA table_info(resume_history)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute(
            "ALTER TABLE resume_history ADD COLUMN user_id INTEGER"
        )

# USER REGISTRATION TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           full_name TEXT NOT NULL,
           email TEXT NOT NULL UNIQUE,
           password_hash TEXT NOT NULL,
           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    connection.commit()
    connection.close()

    print("ResumeIQ database created successfully!")


if __name__ == "__main__":
    setup_database()
