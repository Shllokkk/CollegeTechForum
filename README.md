# 📘 DBIT TechForum

A **Q&A web application** built with **Django**, **Bootstrap**, and **jQuery**.  
Students can post queries, answer others’ queries, and interact through features like **leaderboards, search, and ratings**.  

---

## ✨ Features

- 🔑 **User Authentication** (Signup, Login, Logout with session management).  
- ❓ **Ask a Query** – Users can post new queries under different categories.  
- 💬 **Answer Queries** – Other users can provide answers (users cannot answer their own queries).  
- ⭐ **Rating System** – Users can rate answers, leaderboard highlights top contributors.  
- 🔍 **Search Queries** – Full-text search across posted queries.  
- 📌 **Categories** – Queries organized into Attendance, Exams, Mini-projects, etc.  
- 📊 **Leaderboard** – Shows top-rated users.  

---

## 🛠 Tech Stack

- **Backend**: Django 4.x (Python)  
- **Frontend**: Bootstrap 4/5, jQuery, HTML5, CSS3  
- **Database**: SQLite (default, easily swappable to MySQL/Postgres)  
- **Authentication**: Django’s built-in user auth + sessions  
- **Deployment**: Works locally, easily deployable to any Django-compatible server  

---

## 📂 Project Structure

```
CollegeTechForum/
│
├── Home/                  # Main Django app
│   ├── migrations/        
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Common layout (navbar, footer)
│   │   ├── Home.html      # Homepage with queries & leaderboard
│   │   ├── AllAnswer.html # Displays answers for a query
│   │   ├── AllQueries.html
│   │   ├── Answer.html
│   │   ├── AskQuery.html
│   │   ├── Login.html
│   │   ├── SignUp.html
│   │   └── ... etc.
│   ├── views.py           # All app views
│   ├── models.py          # Query, Answers, Rating models
│   ├── urls.py            # App-specific URLs
│   └── ...
│
├── CollegeTechForum/      # Project root
│   ├── settings.py
│   ├── urls.py
│   └── middleware.py      # Custom NoCacheMiddleware
│
├── manage.py
└── README.md
```

---

## ⚡ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/dbit-techforum.git
cd dbit-techforum
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Start the server
```bash
python manage.py runserver
```

Go to **http://127.0.0.1:8000/** 🎉  
