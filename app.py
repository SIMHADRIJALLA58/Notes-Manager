from flask import Flask,render_template,redirect,request,url_for,session,flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId



app=Flask(__name__)
app.secret_key="secret_key"

bcrypt = Bcrypt(app)


MONGO_URI = "mongodb+srv://simhadri:Password12@cluster1.vuvim.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
client = MongoClient(MONGO_URI)

db = client['personal_notes']
users_collection = db['users']
notes_collection = db["notes"]
notebooks_collection = db["notebooks"]
categories_collection = db["categories"]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        existing_user=users_collection.find_one({"email":email})
        if existing_user:
            flash("Email already exist. Please use a different one","error")
            return redirect(url_for("register"))
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user_data={
            "name":name,
            "email":email,
            "password":hashed_password,
        }

        users_collection.insert_one(user_data)
        flash("registration succussful. Please Login","succuss")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = user["name"]
            session["user_id"] = str(user["_id"])

            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         flash("Please log in first", "error")
#         return redirect(url_for("login"))
#     return render_template("dashboard.html", user=session["user"])

# @app.route("/add_note", methods=["GET", "POST"])
# def add_note():
#     if "user_id" not in session:
#         flash("Please login to add a note", "error")
#         return redirect(url_for("login"))

#     if request.method == "POST":
#         title = request.form["title"]
#         content = request.form["content"]

#         # Save to MongoDB
#         notes_collection.insert_one({
#             "user_id": session["user_id"],
#             "title": title,
#             "content": content
#         })

#         flash("Note added successfully!", "success")
#         return redirect(url_for("dashboard"))

#     return render_template("add_note.html")

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    user_id = session.get("user_id")

    if not user or not user_id:
        flash("Please log in first", "error")
        return redirect(url_for("login"))

    notes = list(notes_collection.find({"user_id": user_id}))
    notebooks = list(notebooks_collection.find({"user_id": user_id}))
    categories = list(categories_collection.find({"user_id": user_id}))

    return render_template(
        "dashboard.html",
        user=user,
        notes=notes,
        notebooks=notebooks,
        categories=categories
    )

# -------------------
# Notes CRUD
# -------------------
@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    if "user_id" not in session:
        flash("Please login to add a note", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        notes_collection.insert_one({
            "user_id": session["user_id"],
            "title": title,
            "content": content
        })

        flash("Note added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_note.html")

@app.route("/edit_note/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        notes_collection.update_one({"_id": ObjectId(note_id)}, {"$set": {"title": title, "content": content}})
        flash("Note updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_note.html", note=note)

@app.route("/delete_note/<note_id>")
def delete_note(note_id):
    notes_collection.delete_one({"_id": ObjectId(note_id)})
    flash("Note deleted successfully!", "success")
    return redirect(url_for("dashboard"))

# -------------------
# Notebooks CRUD
# -------------------
@app.route("/add_notebook", methods=["GET", "POST"])
def add_notebook():
    if request.method == "POST":
        name = request.form["name"]
        notebooks_collection.insert_one({
            "user_id": session["user_id"],
            "name": name
        })
        flash("Notebook added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_notebook.html")

# -------------------
# Categories CRUD
# -------------------
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"]
        categories_collection.insert_one({
            "user_id": session["user_id"],
            "name": name
        })
        flash("Category added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_category.html")

# -------------------
# Archive
# -------------------
@app.route("/archive")
def archive():
    if "user_id" not in session:
        flash("Please log in first", "error")
        return redirect(url_for("login"))

    archived_notes = list(notes_collection.find({"user_id": session["user_id"], "archived": True}))
    return render_template("archive.html", notes=archived_notes)

@app.route("/archive_note/<note_id>")
def archive_note(note_id):
    if "user_id" not in session:
        flash("Please log in first", "error")
        return redirect(url_for("login"))

    # Update note: set archived=True
    notes_collection.update_one(
        {"_id": ObjectId(note_id), "user_id": session["user_id"]},
        {"$set": {"archived": True}}
    )

    flash("Note archived successfully!", "success")
    return redirect(url_for("dashboard"))

# -------------------
# Database (Admin View)
# -------------------
# @app.route("/database")
# def database_view():
#     if "user_id" not in session:
#         flash("Please log in first", "error")
#         return redirect(url_for("login"))

#     # Show raw database counts
#     counts = {
#         "notes": notes_collection.count_documents({}),
#         "notebooks": notebooks_collection.count_documents({}),
#         "categories": categories_collection.count_documents({})
#     }
#     return render_template("database.html", counts=counts)

# -------------------
# Login / Logout Dummy
# -------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         session["user"] = request.form["username"]
#         session["user_id"] = "123"  # Replace with real user ID from DB
#         flash("Logged in successfully!", "success")
#         return redirect(url_for("dashboard"))
#     return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


@app.route("/notes")
def notes():
    if "user_id" not in session:
        flash("Please log in to view notes", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    notes = list(notes_collection.find({"user_id": user_id}))

    return render_template("notes.html", notes=notes)


@app.route("/notebooks")
def notebooks():
    if "user_id" not in session:
        flash("Please log in to view notebooks", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    notebooks = list(notebooks_collection.find({"user_id": user_id}))

    # Optional: Count number of notes in each notebook (if notebook_id is used)
    for notebook in notebooks:
        notebook_id = str(notebook["_id"])
        notebook["note_count"] = notes_collection.count_documents({
            "user_id": user_id,
            "notebook_id": notebook_id  # Only if you're storing this in your notes
        })

    return render_template("notebooks.html", notebooks=notebooks)

@app.route("/categories")
def categories():
    if "user_id" not in session:
        flash("Please log in to view categories", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    categories = list(categories_collection.find({"user_id": user_id}))

    return render_template("categories.html", categories=categories)

# if __name__=="__main__":
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

