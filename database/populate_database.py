
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "interview_questions.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table'
""")

tables = cursor.fetchall()

print("ResumeIQ Database Tables:")
for table in tables:
    print("-", table[0])



# Add career roles
career_roles = [
    ("Python Developer", "Build applications using Python."),
    ("Data Scientist", "Analyze data and build predictive models."),
    ("Web Developer", "Build and maintain websites and web applications."),
    ("Data Analyst", "Analyze data and create meaningful reports."),
    ("AI / ML Engineer", "Build and deploy AI and machine learning systems.")
]

cursor.executemany("""
    INSERT OR IGNORE INTO career_roles (role_name, description)
    VALUES (?, ?)
""", career_roles)

connection.commit()

# Add skills to the database
skills = [
    ("Python", "Programming", "Python programming fundamentals"),
    ("SQL", "Database", "Querying and managing databases"),
    ("Statistics", "Mathematics", "Statistical analysis and probability"),
    ("Pandas", "Data Science", "Data manipulation using Pandas"),
    ("NumPy", "Data Science", "Numerical computing with NumPy"),
    ("Machine Learning", "AI / ML", "Building predictive models"),
    ("Deep Learning", "AI / ML", "Neural networks and deep learning"),
    ("TensorFlow", "AI / ML", "Deep learning framework"),
    ("HTML", "Web Development", "Structure of web pages"),
    ("CSS", "Web Development", "Styling web pages"),
    ("JavaScript", "Web Development", "Interactive web development"),
    ("React", "Web Development", "Frontend development library"),
    ("Django", "Web Development", "Python web framework"),
    ("Excel", "Data Analysis", "Spreadsheet analysis"),
    ("Power BI", "Data Analysis", "Business intelligence and visualization"),
    ("Git", "Tools", "Version control"),
    ("OOP", "Programming", "Object-oriented programming"),
    ("Data Structures", "Programming", "Organizing and managing data"),
    ("Linear Algebra", "Mathematics", "Mathematical foundations for machine learning"),
    ("APIs", "Web Development", "Application programming interfaces")
]

cursor.executemany("""
    INSERT OR IGNORE INTO skills (skill_name, category, description)
    VALUES (?, ?, ?)
""", skills)

connection.commit()

print("20 skills added successfully!")

# Connect career roles with their required skills
role_skill_mapping = {
    "Python Developer": ["Python", "OOP", "Data Structures", "Django", "SQL", "Git"],
    "Data Scientist": ["Python", "Statistics", "Pandas", "NumPy", "Machine Learning", "SQL"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "APIs", "Git"],
    "Data Analyst": ["Excel", "SQL", "Python", "Pandas", "Power BI", "Statistics"],
    "AI / ML Engineer": ["Python", "Linear Algebra", "Statistics", "Machine Learning", "Deep Learning", "TensorFlow"]
}

for role_name, skill_names in role_skill_mapping.items():

    cursor.execute(
        "SELECT id FROM career_roles WHERE role_name = ?",
        (role_name,)
    )
    role_id = cursor.fetchone()[0]

    for skill_name in skill_names:

        cursor.execute(
            "SELECT id FROM skills WHERE skill_name = ?",
            (skill_name,)
        )
        skill_result = cursor.fetchone()

        if skill_result:
            skill_id = skill_result[0]

            cursor.execute("""
                INSERT OR IGNORE INTO role_skills
                (role_id, skill_id, importance)
                VALUES (?, ?, ?)
            """, (role_id, skill_id, "High"))

connection.commit()

print("Career roles connected with their skills successfully!")

# Add personalized learning roadmap
roadmap_data = {
    "Python Developer": [
        ("Python", 1, 5),
        ("OOP", 2, 4),
        ("Data Structures", 3, 7),
        ("SQL", 4, 5),
        ("Django", 5, 10),
        ("Git", 6, 3)
    ],
    "Data Scientist": [
        ("Python", 1, 5),
        ("Statistics", 2, 7),
        ("NumPy", 3, 4),
        ("Pandas", 4, 5),
        ("SQL", 5, 5),
        ("Machine Learning", 6, 14)
    ],
    "Web Developer": [
        ("HTML", 1, 3),
        ("CSS", 2, 5),
        ("JavaScript", 3, 10),
        ("React", 4, 10),
        ("APIs", 5, 5),
        ("Git", 6, 3)
    ],
    "Data Analyst": [
        ("Excel", 1, 5),
        ("Statistics", 2, 7),
        ("SQL", 3, 5),
        ("Python", 4, 7),
        ("Pandas", 5, 5),
        ("Power BI", 6, 7)
    ],
    "AI / ML Engineer": [
        ("Python", 1, 5),
        ("Linear Algebra", 2, 10),
        ("Statistics", 3, 7),
        ("NumPy", 4, 5),
        ("Machine Learning", 5, 14),
        ("Deep Learning", 6, 14),
        ("TensorFlow", 7, 10)
    ]
}

for role_name, roadmap_items in roadmap_data.items():

    cursor.execute(
        "SELECT id FROM career_roles WHERE role_name = ?",
        (role_name,)
    )
    role_id = cursor.fetchone()[0]

    for skill_name, order, days in roadmap_items:

        cursor.execute(
            "SELECT id FROM skills WHERE skill_name = ?",
            (skill_name,)
        )
        skill_result = cursor.fetchone()

        if skill_result:
            cursor.execute("""
                INSERT OR IGNORE INTO learning_roadmap
                (role_id, skill_id, learning_order, estimated_days)
                VALUES (?, ?, ?, ?)
            """, (role_id, skill_result[0], order, days))

connection.commit()

print("Personalized career roadmaps added successfully!")

# Add learning resources
resources = [
    ("Python", "Python Official Tutorial", "https://docs.python.org/3/tutorial/", "Documentation"),
    ("SQL", "W3Schools SQL Tutorial", "https://www.w3schools.com/sql/", "Tutorial"),
    ("Statistics", "Khan Academy Statistics", "https://www.khanacademy.org/math/statistics-probability", "Course"),
    ("Pandas", "Pandas Getting Started", "https://pandas.pydata.org/docs/getting_started/", "Documentation"),
    ("NumPy", "NumPy Quickstart", "https://numpy.org/doc/stable/user/quickstart.html", "Documentation"),
    ("Machine Learning", "Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course", "Course"),
    ("Deep Learning", "DeepLearning.AI", "https://www.deeplearning.ai/", "Course"),
    ("TensorFlow", "TensorFlow Tutorials", "https://www.tensorflow.org/tutorials", "Documentation"),
    ("HTML", "MDN HTML Guide", "https://developer.mozilla.org/en-US/docs/Web/HTML", "Documentation"),
    ("CSS", "MDN CSS Guide", "https://developer.mozilla.org/en-US/docs/Web/CSS", "Documentation"),
    ("JavaScript", "JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "Documentation"),
    ("React", "React Official Learn Guide", "https://react.dev/learn", "Documentation"),
    ("Django", "Django Official Tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "Documentation"),
    ("Excel", "Microsoft Excel Help", "https://support.microsoft.com/excel", "Documentation"),
    ("Power BI", "Microsoft Power BI Learning", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "Course"),
    ("Git", "Git Official Book", "https://git-scm.com/book/en/v2", "Book"),
    ("OOP", "Python Classes Tutorial", "https://docs.python.org/3/tutorial/classes.html", "Documentation"),
    ("Data Structures", "GeeksforGeeks Data Structures", "https://www.geeksforgeeks.org/data-structures/", "Tutorial"),
    ("Linear Algebra", "Khan Academy Linear Algebra", "https://www.khanacademy.org/math/linear-algebra", "Course"),
    ("APIs", "MDN HTTP Overview", "https://developer.mozilla.org/en-US/docs/Web/HTTP", "Documentation")
]

for skill_name, resource_name, url, resource_type in resources:

    cursor.execute(
        "SELECT id FROM skills WHERE skill_name = ?",
        (skill_name,)
    )
    skill_result = cursor.fetchone()

    if skill_result:
        cursor.execute("""
            INSERT OR IGNORE INTO learning_resources
            (skill_id, resource_name, resource_url, resource_type)
            VALUES (?, ?, ?, ?)
        """, (skill_result[0], resource_name, url, resource_type))

connection.commit()

print("Learning resources added successfully!")

# Add career project recommendations
projects = [
    ("Python Developer", "Personal Expense Tracker", "Build a Python application to record and analyze expenses.", "Beginner"),
    ("Python Developer", "Library Management System", "Create a system to manage books, users, and borrowing records.", "Intermediate"),
    ("Python Developer", "REST API Application", "Develop a REST API using Django and Python.", "Advanced"),

    ("Data Scientist", "House Price Prediction", "Build a machine learning model to predict house prices.", "Intermediate"),
    ("Data Scientist", "Customer Segmentation", "Group customers using clustering algorithms.", "Intermediate"),
    ("Data Scientist", "Sales Prediction", "Analyze historical sales and build predictive models.", "Advanced"),

    ("Web Developer", "Personal Portfolio Website", "Build a responsive personal portfolio using HTML, CSS, and JavaScript.", "Beginner"),
    ("Web Developer", "Task Management App", "Create a task management application using React.", "Intermediate"),
    ("Web Developer", "E-commerce Website", "Build an online shopping application with product pages and APIs.", "Advanced"),

    ("Data Analyst", "Sales Dashboard", "Create an interactive sales dashboard using Power BI.", "Beginner"),
    ("Data Analyst", "Customer Data Analysis", "Analyze customer behavior using Python and Pandas.", "Intermediate"),
    ("Data Analyst", "Business Performance Report", "Analyze business KPIs and present actionable insights.", "Advanced"),

    ("AI / ML Engineer", "Spam Email Classifier", "Train a machine learning model to classify spam emails.", "Beginner"),
    ("AI / ML Engineer", "Image Classification", "Build an image classification model using TensorFlow.", "Intermediate"),
    ("AI / ML Engineer", "Sentiment Analysis System", "Build a deep learning model to analyze text sentiment.", "Advanced")
]

for role_name, project_name, description, difficulty in projects:

    cursor.execute(
        "SELECT id FROM career_roles WHERE role_name = ?",
        (role_name,)
    )
    role_result = cursor.fetchone()

    if role_result:
        cursor.execute("""
            INSERT OR IGNORE INTO career_projects
            (role_id, project_name, description, difficulty)
            VALUES (?, ?, ?, ?)
        """, (role_result[0], project_name, description, difficulty))

connection.commit()

print("Career project recommendations added successfully!")


# Python Developer Interview Questions
python_questions = [
    ("What is Python?", "Python is a high-level, interpreted programming language.", "Technical", "Beginner"),
    ("What are Python's main features?", "Python is readable, dynamically typed, interpreted, and supports multiple programming paradigms.", "Technical", "Beginner"),
    ("What is PEP 8?", "PEP 8 is the official Python style guide.", "Conceptual", "Beginner"),
    ("What are variables?", "Variables are names that refer to stored values.", "Technical", "Beginner"),
    ("Name common Python data types.", "Common types include int, float, str, bool, list, tuple, set, and dict.", "Technical", "Beginner"),
    ("What is a list?", "A list is an ordered, mutable collection of elements.", "Technical", "Beginner"),
    ("What is a tuple?", "A tuple is an ordered, immutable collection.", "Technical", "Beginner"),
    ("What is a dictionary?", "A dictionary stores data as key-value pairs.", "Technical", "Beginner"),
    ("What is a set?", "A set is an unordered collection of unique elements.", "Technical", "Beginner"),
    ("What is type casting?", "Type casting converts a value from one data type to another.", "Technical", "Beginner"),
    ("What is indentation?", "Indentation defines code blocks in Python.", "Conceptual", "Beginner"),
    ("What is a function?", "A function is a reusable block of code that performs a task.", "Technical", "Beginner"),
    ("What is a lambda function?", "A lambda is a small anonymous function created using the lambda keyword.", "Technical", "Intermediate"),
    ("What is recursion?", "Recursion occurs when a function calls itself.", "Technical", "Intermediate"),
    ("What is the return statement?", "It sends a result back from a function.", "Technical", "Beginner"),
    ("What are *args and **kwargs?", "*args accepts variable positional arguments; **kwargs accepts variable keyword arguments.", "Technical", "Intermediate"),
    ("What is a module?", "A module is a Python file containing reusable code.", "Technical", "Beginner"),
    ("What is a package?", "A package organizes related Python modules.", "Technical", "Beginner"),
    ("What is exception handling?", "It handles runtime errors using try, except, else, and finally.", "Technical", "Intermediate"),
    ("What is the finally block?", "The finally block executes whether an exception occurs or not.", "Technical", "Intermediate"),
    ("What is object-oriented programming?", "OOP organizes code using classes and objects.", "Conceptual", "Beginner"),
    ("What is a class?", "A class is a blueprint for creating objects.", "Technical", "Beginner"),
    ("What is an object?", "An object is an instance of a class.", "Technical", "Beginner"),
    ("What is inheritance?", "Inheritance allows one class to reuse features of another class.", "Technical", "Intermediate"),
    ("What is polymorphism?", "Polymorphism allows the same interface to have different implementations.", "Technical", "Intermediate"),
    ("What is encapsulation?", "Encapsulation bundles data and methods and controls access to them.", "Technical", "Intermediate"),
    ("What is abstraction?", "Abstraction hides implementation details and exposes essential features.", "Technical", "Intermediate"),
    ("What is the __init__ method?", "__init__ initializes an object's attributes when it is created.", "Technical", "Beginner"),
    ("What is self in Python?", "self refers to the current object instance.", "Technical", "Beginner"),
    ("What is method overriding?", "A child class provides its own implementation of a parent class method.", "Technical", "Intermediate"),
    ("What is list comprehension?", "It is a concise way to create lists from iterables.", "Technical", "Intermediate"),
    ("What is a generator?", "A generator produces values lazily, usually using yield.", "Technical", "Intermediate"),
    ("What is an iterator?", "An iterator returns values one at a time using next().", "Technical", "Intermediate"),
    ("Difference between append() and extend()?", "append adds one item; extend adds items from an iterable.", "Technical", "Beginner"),
    ("What is slicing?", "Slicing extracts part of a sequence using start, stop, and step.", "Technical", "Beginner"),
    ("Difference between == and is?", "== compares values; is checks object identity.", "Technical", "Intermediate"),
    ("What is a decorator?", "A decorator modifies or extends a function's behavior.", "Technical", "Advanced"),
    ("What is a virtual environment?", "It isolates project dependencies from other Python projects.", "Tools", "Intermediate"),
    ("What is pip?", "pip installs and manages Python packages.", "Tools", "Beginner"),
    ("What is file handling?", "File handling reads from and writes to files.", "Technical", "Beginner"),
    ("Difference between read() and readline()?", "read() reads file content; readline() reads one line.", "Technical", "Beginner"),
    ("What is the GIL?", "The Global Interpreter Lock in CPython controls execution of Python bytecode by threads.", "Technical", "Advanced"),
    ("What is multithreading?", "Multithreading runs multiple threads within one process.", "Technical", "Advanced"),
    ("What is multiprocessing?", "Multiprocessing uses separate processes to run tasks in parallel.", "Technical", "Advanced"),
    ("How do you debug Python code?", "Use print statements, logging, breakpoints, and debugging tools.", "Practical", "Intermediate"),
    ("How do you manage project dependencies?", "Use requirements files or project tools to record and install dependencies.", "Practical", "Intermediate"),
    ("How would you optimize slow Python code?", "Profile the code, choose efficient algorithms, and reduce unnecessary work.", "Practical", "Advanced"),
    ("How would you handle invalid user input?", "Validate inputs and show clear error messages or suitable recovery options.", "Practical", "Intermediate"),
    ("How do you test Python code?", "Write unit and integration tests using tools such as pytest or unittest.", "Practical", "Intermediate"),
    ("Tell me about a Python project you built.", "Explain its purpose, technologies, your contribution, challenges, and results.", "HR", "Beginner"),
    ("Why should we hire you as a Python Developer?", "Connect your Python skills, problem-solving ability, projects, and willingness to learn to the role.", "HR", "Beginner")
]

cursor.execute(
    "SELECT id FROM career_roles WHERE role_name = ?",
    ("Python Developer",)
)
python_role = cursor.fetchone()

if python_role:
    cursor.executemany("""
        INSERT INTO interview_questions
        (role_id, question, answer, category, difficulty)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (python_role[0], q, a, category, difficulty)
        for q, a, category, difficulty in python_questions
    ])

connection.commit()
print("Python Developer: 50 interview questions added!")


# ==========================================
# REMAINING 200 RESUMEIQ INTERVIEW QUESTIONS
# ==========================================

def add_role_questions(role_name, questions):
    cursor.execute(
        "SELECT id FROM career_roles WHERE role_name = ?",
        (role_name,)
    )
    result = cursor.fetchone()

    if not result:
        print(f"Role not found: {role_name}")
        return

    role_id = result[0]
    added = 0

    for question, answer, category, difficulty in questions:
        cursor.execute("""
            SELECT id FROM interview_questions
            WHERE role_id = ? AND question = ?
        """, (role_id, question))

        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO interview_questions
                (role_id, question, answer, category, difficulty)
                VALUES (?, ?, ?, ?, ?)
            """, (role_id, question, answer, category, difficulty))
            added += 1

    connection.commit()
    print(f"{role_name}: {added} new questions added!")


# ==========================================
# DATA SCIENTIST - 50 QUESTIONS
# ==========================================

data_scientist_questions = [
    ("What is Data Science?", "It combines statistics, programming, and domain knowledge to extract insights from data.", "Conceptual", "Beginner"),
    ("What does a Data Scientist do?", "They collect, clean, analyze, model, and interpret data to solve problems.", "Conceptual", "Beginner"),
    ("What is structured data?", "Data organized in a predefined format such as rows and columns.", "Conceptual", "Beginner"),
    ("What is unstructured data?", "Data without a fixed tabular structure, such as images, audio, and text.", "Conceptual", "Beginner"),
    ("What is data preprocessing?", "Preparing raw data by cleaning and transforming it before analysis.", "Technical", "Beginner"),
    ("What is data cleaning?", "Identifying and correcting inaccurate, missing, duplicate, or inconsistent data.", "Technical", "Beginner"),
    ("How do you handle missing values?", "Remove or impute them using suitable statistical or domain-specific methods.", "Practical", "Intermediate"),
    ("What is an outlier?", "An observation that differs significantly from other observations.", "Statistics", "Beginner"),
    ("What is exploratory data analysis?", "Analyzing data through statistics and visualization to understand its patterns.", "Technical", "Beginner"),
    ("What is NumPy?", "A Python library for numerical computing and multidimensional arrays.", "Tools", "Beginner"),
    ("What is Pandas?", "A Python library for data manipulation and analysis.", "Tools", "Beginner"),
    ("What is a DataFrame?", "A two-dimensional labeled data structure in Pandas.", "Technical", "Beginner"),
    ("What is data visualization?", "Presenting data using charts, graphs, and plots.", "Conceptual", "Beginner"),
    ("Name Python visualization libraries.", "Matplotlib, Seaborn, and Plotly are commonly used libraries.", "Tools", "Beginner"),
    ("What is correlation?", "A measure of the strength and direction of association between variables.", "Statistics", "Beginner"),
    ("What is covariance?", "A measure of how two variables change together.", "Statistics", "Intermediate"),
    ("What is mean?", "The arithmetic average of a set of values.", "Statistics", "Beginner"),
    ("What is median?", "The middle value of an ordered dataset.", "Statistics", "Beginner"),
    ("What is mode?", "The most frequently occurring value in a dataset.", "Statistics", "Beginner"),
    ("What is standard deviation?", "A measure of how spread out values are around their mean.", "Statistics", "Intermediate"),
    ("What is variance?", "The average squared deviation from the mean.", "Statistics", "Intermediate"),
    ("What is a normal distribution?", "A symmetric, bell-shaped probability distribution.", "Statistics", "Beginner"),
    ("What is hypothesis testing?", "A statistical method for evaluating a claim using sample data.", "Statistics", "Intermediate"),
    ("What is a p-value?", "A measure of how compatible observed data is with a null hypothesis.", "Statistics", "Intermediate"),
    ("What is a confidence interval?", "An interval produced by a method designed to capture a population parameter at a stated confidence level.", "Statistics", "Intermediate"),
    ("What is sampling?", "Selecting a subset of a population for analysis.", "Statistics", "Beginner"),
    ("What is machine learning?", "A field where algorithms learn patterns from data to make predictions or decisions.", "Machine Learning", "Beginner"),
    ("What are the main types of machine learning?", "Supervised, unsupervised, and reinforcement learning.", "Machine Learning", "Beginner"),
    ("What is supervised learning?", "Learning from labeled examples.", "Machine Learning", "Beginner"),
    ("What is unsupervised learning?", "Finding patterns in data without labeled target values.", "Machine Learning", "Beginner"),
    ("What is classification?", "Predicting a discrete category or class.", "Machine Learning", "Beginner"),
    ("What is regression?", "Predicting a continuous numerical value.", "Machine Learning", "Beginner"),
    ("What is clustering?", "Grouping similar observations without predefined labels.", "Machine Learning", "Intermediate"),
    ("What is linear regression?", "A model that represents a linear relationship between inputs and a continuous target.", "Machine Learning", "Intermediate"),
    ("What is logistic regression?", "A model that estimates probabilities for classification tasks.", "Machine Learning", "Intermediate"),
    ("What is a decision tree?", "A model that makes predictions using feature-based decision rules.", "Machine Learning", "Intermediate"),
    ("What is random forest?", "An ensemble that combines multiple decision trees.", "Machine Learning", "Intermediate"),
    ("What is overfitting?", "When a model learns training data too closely and performs poorly on unseen data.", "Machine Learning", "Intermediate"),
    ("What is underfitting?", "When a model is too simple to capture important patterns.", "Machine Learning", "Intermediate"),
    ("What is cross-validation?", "Evaluating a model using multiple training and validation splits.", "Evaluation", "Intermediate"),
    ("What is feature engineering?", "Creating or transforming input variables to improve a model.", "Machine Learning", "Advanced"),
    ("What is feature selection?", "Selecting the most useful input variables for a model.", "Machine Learning", "Intermediate"),
    ("What is a confusion matrix?", "A table summarizing correct and incorrect classification predictions.", "Evaluation", "Intermediate"),
    ("What is precision?", "The proportion of predicted positives that are actually positive.", "Evaluation", "Intermediate"),
    ("What is recall?", "The proportion of actual positive cases correctly identified.", "Evaluation", "Intermediate"),
    ("What is F1-score?", "The harmonic mean of precision and recall.", "Evaluation", "Intermediate"),
    ("What is data leakage?", "When information unavailable at prediction time improperly enters model training.", "Evaluation", "Advanced"),
    ("How do you approach a new data science project?", "Define the problem, collect and clean data, explore it, build models, evaluate results, and communicate findings.", "Practical", "Advanced"),
    ("How do you handle a large dataset?", "Use efficient data structures, optimized operations, chunking, and suitable processing tools.", "Practical", "Advanced"),
    ("How do you explain technical findings to business teams?", "Use clear language, visualizations, and focus on practical business impact.", "Communication", "Intermediate"),
    ("Why should we hire you as a Data Scientist?", "Highlight analytical thinking, statistics, programming, projects, and willingness to learn.", "HR", "Beginner")
]


# ==========================================
# WEB DEVELOPER - 50 QUESTIONS
# ==========================================

web_developer_questions = [
    ("What is web development?", "Building and maintaining websites and web applications.", "Conceptual", "Beginner"),
    ("What is frontend development?", "Developing the user-facing parts of a website.", "Conceptual", "Beginner"),
    ("What is backend development?", "Developing server-side logic, data processing, and application services.", "Conceptual", "Beginner"),
    ("What is HTML?", "The markup language used to structure web pages.", "Technical", "Beginner"),
    ("What is CSS?", "A stylesheet language used to control webpage presentation.", "Technical", "Beginner"),
    ("What is JavaScript?", "A programming language used to create interactive web experiences.", "Technical", "Beginner"),
    ("What is semantic HTML?", "HTML that uses elements according to their meaning and purpose.", "Technical", "Intermediate"),
    ("What is the DOM?", "The Document Object Model represents a webpage as a tree of objects.", "Technical", "Intermediate"),
    ("What is responsive design?", "Designing interfaces that adapt to different screen sizes.", "Conceptual", "Beginner"),
    ("What is the CSS box model?", "It describes content, padding, border, and margin around an element.", "Technical", "Intermediate"),
    ("What is Flexbox?", "A CSS layout model for arranging items along a row or column.", "Technical", "Intermediate"),
    ("What is CSS Grid?", "A CSS layout system for arranging elements in rows and columns.", "Technical", "Intermediate"),
    ("What is a CSS selector?", "A pattern used to target HTML elements for styling.", "Technical", "Beginner"),
    ("What is the difference between class and ID?", "Classes can be reused; an ID is intended to identify one unique element.", "Technical", "Beginner"),
    ("What is a media query?", "A CSS rule that applies styles under specified device or viewport conditions.", "Technical", "Intermediate"),
    ("What is React?", "A JavaScript library for building component-based user interfaces.", "Tools", "Beginner"),
    ("What is a React component?", "A reusable unit of UI that can accept inputs and render content.", "React", "Beginner"),
    ("What are React props?", "Inputs passed from a parent component to a child component.", "React", "Beginner"),
    ("What is React state?", "Data managed by a component that can change over time and trigger rendering.", "React", "Intermediate"),
    ("What is the useState hook?", "A React hook for adding state to function components.", "React", "Intermediate"),
    ("What is the useEffect hook?", "A hook for synchronizing a component with external systems.", "React", "Intermediate"),
    ("What is JSX?", "A syntax extension that allows HTML-like markup in JavaScript.", "React", "Beginner"),
    ("What is the virtual DOM?", "A representation React uses to reason about UI updates.", "React", "Intermediate"),
    ("What is event handling in JavaScript?", "Responding to events such as clicks, typing, or form submission.", "JavaScript", "Beginner"),
    ("What is event bubbling?", "An event propagates from the target element up through its ancestors.", "JavaScript", "Intermediate"),
    ("What is a JavaScript promise?", "An object representing the eventual result of an asynchronous operation.", "JavaScript", "Intermediate"),
    ("What is async/await?", "Syntax for writing asynchronous JavaScript using promise-based operations.", "JavaScript", "Intermediate"),
    ("What is JSON?", "A lightweight text format for representing structured data.", "Technical", "Beginner"),
    ("What is an API?", "An interface that allows software systems to communicate.", "Backend", "Beginner"),
    ("What is REST?", "An architectural style for networked applications using resources and standard HTTP semantics.", "Backend", "Intermediate"),
    ("What is HTTP?", "A protocol used for communication between web clients and servers.", "Backend", "Beginner"),
    ("What is HTTPS?", "HTTP secured using encryption through TLS.", "Security", "Beginner"),
    ("What is the difference between GET and POST?", "GET requests retrieve data; POST requests submit data for processing.", "Backend", "Beginner"),
    ("What is a status code 404?", "It indicates that the requested resource could not be found.", "Backend", "Beginner"),
    ("What is a status code 500?", "It indicates an internal server error.", "Backend", "Beginner"),
    ("What is authentication?", "Verifying the identity of a user or system.", "Security", "Intermediate"),
    ("What is authorization?", "Determining what an authenticated user is allowed to do.", "Security", "Intermediate"),
    ("What is SQL?", "A language used to query and manage relational databases.", "Database", "Beginner"),
    ("What is a primary key?", "A column or combination of columns that uniquely identifies a database row.", "Database", "Beginner"),
    ("What is database normalization?", "Organizing relational data to reduce redundancy and update anomalies.", "Database", "Intermediate"),
    ("What is Git?", "A distributed version control system for tracking code changes.", "Tools", "Beginner"),
    ("What is GitHub?", "A platform for hosting and collaborating on Git repositories.", "Tools", "Beginner"),
    ("What is website deployment?", "Making a website or application available in a target environment.", "Practical", "Beginner"),
    ("How do you improve website performance?", "Optimize images, reduce unnecessary JavaScript, cache resources, and measure performance.", "Practical", "Advanced"),
    ("How do you make a website accessible?", "Use semantic HTML, keyboard support, labels, contrast, and appropriate alternative text.", "Practical", "Intermediate"),
    ("How do you debug a frontend issue?", "Reproduce it, inspect browser developer tools, check console errors, and isolate the cause.", "Practical", "Intermediate"),
    ("How do you protect a website from common attacks?", "Validate inputs, encode output, use secure authentication, and follow security best practices.", "Security", "Advanced"),
    ("What is cross-browser testing?", "Checking that a website behaves correctly across different browsers.", "Testing", "Intermediate"),
    ("How do you test a web application?", "Use unit, integration, and end-to-end tests where appropriate.", "Testing", "Intermediate"),
    ("Why should we hire you as a Web Developer?", "Explain your web skills, projects, teamwork, problem-solving, and eagerness to learn.", "HR", "Beginner")
]


# ==========================================
# DATA ANALYST - 50 QUESTIONS
# ==========================================

data_analyst_questions = [
    ("What is data analysis?", "Examining data to discover patterns, answer questions, and support decisions.", "Conceptual", "Beginner"),
    ("What does a Data Analyst do?", "They collect, clean, analyze, visualize, and communicate data insights.", "Conceptual", "Beginner"),
    ("What is a dataset?", "A collection of related observations or records.", "Conceptual", "Beginner"),
    ("What is data cleaning?", "Correcting missing, duplicate, inaccurate, and inconsistent records.", "Technical", "Beginner"),
    ("What is data validation?", "Checking whether data meets expected rules and constraints.", "Technical", "Beginner"),
    ("What is a duplicate record?", "A record that repeats information already represented in the dataset.", "Technical", "Beginner"),
    ("What is Excel?", "A spreadsheet application used to organize, analyze, and visualize data.", "Tools", "Beginner"),
    ("What is a spreadsheet formula?", "An expression that calculates a value using cell references and functions.", "Excel", "Beginner"),
    ("What does SUM do in Excel?", "It adds the values in specified cells or ranges.", "Excel", "Beginner"),
    ("What does AVERAGE do?", "It calculates the arithmetic mean of selected numeric values.", "Excel", "Beginner"),
    ("What is VLOOKUP?", "A function that searches the first column of a range and returns a value from another column.", "Excel", "Intermediate"),
    ("What is XLOOKUP?", "A lookup function that searches a range and returns a corresponding value.", "Excel", "Intermediate"),
    ("What is a pivot table?", "A tool for summarizing and analyzing data interactively.", "Excel", "Intermediate"),
    ("What is conditional formatting?", "Formatting cells based on rules or values.", "Excel", "Beginner"),
    ("What is SQL?", "A language for querying and managing relational databases.", "SQL", "Beginner"),
    ("What is SELECT in SQL?", "It retrieves columns and rows from database tables.", "SQL", "Beginner"),
    ("What is WHERE in SQL?", "It filters rows according to a condition.", "SQL", "Beginner"),
    ("What is GROUP BY?", "It groups rows with matching values for aggregation.", "SQL", "Intermediate"),
    ("What is ORDER BY?", "It sorts query results by specified columns.", "SQL", "Beginner"),
    ("What is a SQL JOIN?", "It combines rows from tables using related columns.", "SQL", "Intermediate"),
    ("What is an INNER JOIN?", "It returns rows with matching values in both joined tables.", "SQL", "Intermediate"),
    ("What is a LEFT JOIN?", "It returns all left-table rows and matching right-table rows.", "SQL", "Intermediate"),
    ("What is a primary key?", "A column or group of columns that uniquely identifies a row.", "Database", "Beginner"),
    ("What is a foreign key?", "A column that references a key in another table.", "Database", "Intermediate"),
    ("What is database normalization?", "Organizing tables to reduce redundancy and update anomalies.", "Database", "Intermediate"),
    ("What is Python used for in data analysis?", "Python supports data cleaning, analysis, automation, and visualization.", "Python", "Beginner"),
    ("What is Pandas?", "A Python library for working with structured data.", "Python", "Beginner"),
    ("What is NumPy?", "A Python library for numerical operations and arrays.", "Python", "Beginner"),
    ("What is a Pandas Series?", "A one-dimensional labeled array.", "Python", "Beginner"),
    ("What is a Pandas DataFrame?", "A two-dimensional labeled table-like data structure.", "Python", "Beginner"),
    ("How do you remove missing rows in Pandas?", "Use dropna() when removing those rows is appropriate.", "Python", "Intermediate"),
    ("How do you remove duplicate rows in Pandas?", "Use drop_duplicates() with suitable subset options.", "Python", "Intermediate"),
    ("What is data visualization?", "Presenting data visually to communicate patterns and findings.", "Visualization", "Beginner"),
    ("What is a bar chart used for?", "Comparing values across categories.", "Visualization", "Beginner"),
    ("What is a line chart used for?", "Showing trends or changes over an ordered sequence, often time.", "Visualization", "Beginner"),
    ("What is a scatter plot?", "A chart showing the relationship between two numerical variables.", "Visualization", "Intermediate"),
    ("What is a dashboard?", "A visual display of important metrics and information.", "Visualization", "Beginner"),
    ("What is Power BI?", "A Microsoft platform for data modeling, analysis, and interactive reporting.", "Tools", "Beginner"),
    ("What is a KPI?", "A key performance indicator measures progress toward an important objective.", "Business", "Beginner"),
    ("What is a business metric?", "A measurable value used to assess business performance.", "Business", "Beginner"),
    ("What is descriptive statistics?", "Methods that summarize and describe the main features of data.", "Statistics", "Beginner"),
    ("What is correlation?", "A measure of the strength and direction of association between variables.", "Statistics", "Intermediate"),
    ("What is an average?", "A measure of central tendency, commonly the arithmetic mean.", "Statistics", "Beginner"),
    ("What is sampling?", "Selecting a subset of a population for analysis.", "Statistics", "Beginner"),
    ("How would you investigate a sudden sales decline?", "Validate the data, compare periods and segments, identify changes, and discuss likely causes.", "Practical", "Advanced"),
    ("How do you communicate insights to managers?", "Present concise findings, clear visuals, business implications, and recommended actions.", "Communication", "Intermediate"),
    ("How do you ensure data accuracy?", "Validate sources, check ranges and duplicates, reconcile totals, and document transformations.", "Practical", "Intermediate"),
    ("How do you prioritize analysis requests?", "Consider business impact, urgency, effort, and stakeholder needs.", "Practical", "Intermediate"),
    ("Tell me about a data analysis project.", "Explain the business question, dataset, tools, analysis, findings, and impact.", "HR", "Beginner"),
    ("Why should we hire you as a Data Analyst?", "Highlight analytical thinking, Excel, SQL, visualization, communication, and project experience.", "HR", "Beginner")
]


# ==========================================
# AI / ML ENGINEER - 50 QUESTIONS
# ==========================================

ai_ml_questions = [
    ("What is Artificial Intelligence?", "AI is the field of building systems that perform tasks associated with intelligent behavior.", "Conceptual", "Beginner"),
    ("What is Machine Learning?", "Machine learning develops algorithms that learn patterns from data.", "Conceptual", "Beginner"),
    ("What is Deep Learning?", "Deep learning uses neural networks with multiple layers to learn representations.", "Conceptual", "Beginner"),
    ("How are AI, ML, and Deep Learning related?", "AI is the broad field, ML is a subset of AI, and deep learning is a subset of ML.", "Conceptual", "Beginner"),
    ("What is a neural network?", "A model made of connected computational units that learn patterns from data.", "Technical", "Beginner"),
    ("What is a neuron in a neural network?", "A computational unit that combines inputs, applies weights and bias, and uses an activation function.", "Technical", "Intermediate"),
    ("What is an activation function?", "A function that introduces non-linearity into a neural network.", "Technical", "Intermediate"),
    ("What is ReLU?", "An activation function that returns zero for negative inputs and the input itself for positive inputs.", "Technical", "Intermediate"),
    ("What is sigmoid activation?", "A function that maps real values into a range between zero and one.", "Technical", "Intermediate"),
    ("What is softmax?", "A function that converts a vector of scores into values that sum to one.", "Technical", "Intermediate"),
    ("What is forward propagation?", "Passing input through a network to calculate its prediction.", "Technical", "Intermediate"),
    ("What is backpropagation?", "Computing gradients through a network to update its parameters.", "Technical", "Advanced"),
    ("What is gradient descent?", "An optimization algorithm that updates parameters using gradients to reduce a loss function.", "Technical", "Intermediate"),
    ("What is a learning rate?", "A parameter controlling the step size of optimization updates.", "Technical", "Intermediate"),
    ("What is a loss function?", "A function measuring the difference between model predictions and target values.", "Technical", "Intermediate"),
    ("What is an epoch?", "One complete pass through the training dataset.", "Technical", "Beginner"),
    ("What is batch size?", "The number of training examples processed in one update step.", "Technical", "Intermediate"),
    ("What is an optimizer?", "An algorithm that updates model parameters during training.", "Technical", "Intermediate"),
    ("What is overfitting in deep learning?", "When a model fits training examples too closely and generalizes poorly.", "Technical", "Intermediate"),
    ("How can overfitting be reduced?", "Use regularization, dropout, data augmentation, early stopping, or more representative data.", "Practical", "Advanced"),
    ("What is dropout?", "A regularization technique that randomly disables some units during training.", "Technical", "Advanced"),
    ("What is batch normalization?", "A technique that normalizes intermediate activations during training.", "Technical", "Advanced"),
    ("What is CNN?", "A convolutional neural network commonly used for image and spatial data.", "Architecture", "Intermediate"),
    ("What is an RNN?", "A recurrent neural network designed to process sequential information.", "Architecture", "Intermediate"),
    ("What is an LSTM?", "A recurrent network architecture designed to capture longer-term dependencies.", "Architecture", "Advanced"),
    ("What is a transformer?", "A neural network architecture based on attention mechanisms.", "Architecture", "Advanced"),
    ("What is attention in deep learning?", "A mechanism that lets a model weigh the relevance of different input elements.", "Architecture", "Advanced"),
    ("What is TensorFlow?", "An open-source framework for machine learning and numerical computation.", "Tools", "Beginner"),
    ("What is PyTorch?", "An open-source machine learning framework widely used for deep learning.", "Tools", "Beginner"),
    ("What is a tensor?", "A multidimensional data structure used in numerical computation.", "Technical", "Beginner"),
    ("What is transfer learning?", "Reusing a model trained on one task as a starting point for another task.", "Technical", "Intermediate"),
    ("What is fine-tuning?", "Further training a pretrained model on task-specific data.", "Technical", "Intermediate"),
    ("What is an embedding?", "A vector representation of data that captures useful relationships.", "Technical", "Intermediate"),
    ("What is natural language processing?", "A field focused on enabling computers to process and generate human language.", "AI", "Beginner"),
    ("What is computer vision?", "A field focused on enabling computers to interpret images and videos.", "AI", "Beginner"),
    ("What is image classification?", "Assigning an image to one of several predefined categories.", "AI", "Beginner"),
    ("What is object detection?", "Identifying and locating objects within images or video frames.", "AI", "Intermediate"),
    ("What is model evaluation?", "Measuring model performance on data not used to fit the model.", "Evaluation", "Intermediate"),
    ("What is a training dataset?", "Data used to fit model parameters.", "Evaluation", "Beginner"),
    ("What is a validation dataset?", "Data used to tune models and make development decisions.", "Evaluation", "Beginner"),
    ("What is a test dataset?", "Held-out data used for final evaluation of a model.", "Evaluation", "Beginner"),
    ("What is model deployment?", "Making a trained model available for use in an application or service.", "Deployment", "Intermediate"),
    ("What is model inference?", "Using a trained model to generate predictions on new inputs.", "Deployment", "Beginner"),
    ("What is an API in an ML application?", "An interface that allows other applications to send inputs and receive model predictions.", "Deployment", "Intermediate"),
    ("What is model monitoring?", "Tracking deployed model behavior, performance, and data changes over time.", "Deployment", "Advanced"),
    ("What is data drift?", "A change in the distribution of incoming data compared with training data.", "Deployment", "Advanced"),
    ("How do you handle an imbalanced dataset?", "Use suitable metrics, resampling, class weights, or threshold adjustment.", "Practical", "Advanced"),
    ("How would you build an image classifier?", "Collect and label images, preprocess them, train a suitable model, evaluate it, and deploy it.", "Practical", "Advanced"),
    ("How do you make an ML system reliable?", "Use representative data, testing, monitoring, versioning, and clear failure handling.", "Practical", "Advanced"),
    ("Tell me about an AI or ML project you built.", "Describe the problem, dataset, model, evaluation, your contribution, and the outcome.", "HR", "Beginner"),
    ("Why should we hire you as an AI/ML Engineer?", "Highlight programming, mathematics, ML knowledge, practical projects, and continuous learning.", "HR", "Beginner")
]


# ==========================================
# INSERT ALL FOUR ROLE QUESTION BANKS
# ==========================================

add_role_questions("Data Scientist", data_scientist_questions)
add_role_questions("Web Developer", web_developer_questions)
add_role_questions("Data Analyst", data_analyst_questions)
add_role_questions("AI / ML Engineer", ai_ml_questions)

print("Remaining interview question banks processed!")




print("Five career roles added successfully!")
cursor.execute("""
SELECT
    career_roles.role_name,
    skills.skill_name,
    COUNT(*) AS total
FROM learning_roadmap
JOIN career_roles ON learning_roadmap.role_id = career_roles.id
JOIN skills ON learning_roadmap.skill_id = skills.id
GROUP BY career_roles.role_name, skills.skill_name
HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()

print("Duplicate roadmap entries:", duplicates)
cursor.execute("""
DELETE FROM learning_roadmap
WHERE id NOT IN (
    SELECT MIN(id)
    FROM learning_roadmap
    GROUP BY role_id, skill_id
)
""")

connection.commit()

print("Duplicate roadmap entries cleaned successfully!")
