Personal Notes Manager:

A Personal Notes Manager is a web application that helps users store and organize their notes online.  
The goal of this project is to create a **simple, secure, and accessible note-taking tool** where users can:  

- Register and log in with their own account  
- Write and save personal notes in the cloud  
- Categorize notes for better organization  
- Archive notes that are not needed but should not be deleted  
- Access notes anytime from any device with an internet connection  

This project was built as a **practice project** to strengthen skills in **Flask, MongoDB, and full-stack web development**.  
It also demonstrates **user authentication, CRUD operations, and session management.

Features:
- User Authentication – Register, Login & Logout with session management  
- Create & Manage Notes – Add, edit, delete, and view notes  
- Categories – Organize notes by categories for easy access  
- Archive System – Archive and restore notes anytime  
- Cloud Database – All notes stored securely in MongoDB Atlas  
- Responsive UI – Clean and modern design with HTML, CSS, JS

  Tech Stack:
- Backend: Flask (Python)  
- Frontend: HTML, CSS, JavaScript  
- Database: MongoDB Atlas  
- Others: Flask Sessions, Flash Messages

1.Clone the repository
```bash
   git clone https://github.com/your-username/notes-manager.git
   cd notes-manager
2.Create virtual environment
  python -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows
3.Install dependencies
  pip install -r requirements.txt
4.Configure MongoDB Atlas:
  Create a free cluster on MongoDB Atlas
  Get your connection string
  Replace <your_connection_string> in app.py

client = pymongo.MongoClient("<your_connection_string>")
db = client["notes_manager"]
notes_collection = db["notes"]
users_collection = db["users"]

5.Run the application
  python app.py

  
