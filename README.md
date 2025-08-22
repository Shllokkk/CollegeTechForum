# 📘 DBIT TechForum

A **Q&A web application** built with **Django**, **Bootstrap**, and **jQuery**.  
Students can post queries, answer others' queries, and interact through features like **leaderboards, search, and ratings**.  

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
- **Authentication**: Django's built-in user auth + sessions  
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

## 🖼️ Screenshots & User Flow

### 🔐 **Authentication Flow**

#### 1. **Signup Page**
![Signup Page](screenshots/SignupPage.png)
*New users can create accounts with their name, email, year, and branch information.*

#### 2. **Login Page**
![Login Page](screenshots/LoginPage.png)
*Existing users can securely log in to access the forum features.*

### 🏠 **Main Application**

#### 3. **Homepage**
![Homepage](screenshots/Homepage.png)
*The main dashboard showing recent queries, categories, and leaderboard information.*

#### 4. **Ask Query Page**
![Ask Query Page](screenshots/AskQueryPage.png)
*Users can post new queries with descriptions and select appropriate categories.*

### 🔍 **Query Management & Discovery**

#### 5. **Search Page**
![Search Page](screenshots/SearchPage.png)
*Full-text search functionality to find specific queries across the forum.*

#### 6. **Category Page**
![Category Page](screenshots/CategoryPage.png)
*Browse queries organized by categories like Attendance, Exams, Mini-projects, etc.*

#### 7. **Unanswered Queries Page**
![Unanswered Queries Page](screenshots/UnansweredQueriesPage.png)
*View queries that haven't received answers yet, encouraging community participation.*

### 💬 **Answering & Interaction**

#### 8. **Answer Query Page**
![Answer Query Page](screenshots/AnswerQueryPage.png)
*Users can provide detailed answers to queries posted by others.*

#### 9. **Answers For Query Page**
![Answers For Query Page](screenshots/AnswersForQueryPage.png)
*View all answers for a specific query with user information and response details.*

### ⭐ **Rating & Feedback**

#### 10. **Rating Page**
![Rating Page](screenshots/RatingPage.png)
*Users can rate answers to help identify the most helpful responses and contributors.*

### ℹ️ **Information Pages**

#### 11. **About Us Page**
![About Us Page](screenshots/AboutUsPage.png)
*Information about the platform and its purpose.*

#### 12. **Contact Us Page**
![Contact Us Page](screenshots/ContactUsPage.png)
*Contact information and support details for users.*

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.x
- pip (Python package manager)

### Installation
1. Clone the repository
2. Run migrations: `python manage.py migrate`
3. Start the server: `python manage.py runserver`
4. Open `http://localhost:8000` in your browser

### Default Admin Access
- Username: `admin`
- Password: `admin123`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request