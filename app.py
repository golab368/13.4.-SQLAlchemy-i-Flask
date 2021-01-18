#from app import db
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)


class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    book = db.Column(db.String(50))
    availability = db.Column(db.String(50))

    def __repr__(self):
        return "<User(author='%s', book='%s', availability='%s')>" % (self.author, self.book, self.availability)


@app.route("/home")
def home():
    values_in_library = Library.query.order_by(Library.id)
    return render_template("home.html", values_in_library=values_in_library)


@app.route("/addrec", methods=["POST", "GET"])
def addrec():
    title = "Add records to library"

    if request.method == "POST":
        author_name = request.form["author"]
        book_name = request.form["book"]
        availability_yes_or_no = request.form["availability"]

        new_record = Library(author=author_name, book=book_name,
                             availability=availability_yes_or_no)

        try:

            db.session.add(new_record)
            db.session.commit()

            return redirect("/addrec")

        except:
            return "There was an error try againg"
            db.session.rollback()

    else:
        values_in_library = Library.query.order_by(Library.id)
        return render_template("addrec.html", title=title, values_in_library=values_in_library)


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):

    library_to_update = Library.query.get_or_404(id)

    if request.method == "POST":
        library_to_update.author = request.form["author"]
        library_to_update.book = request.form["book"]
        library_to_update.availability = request.form["availability"]

        try:
            db.session.commit()
            return redirect("/home")
        except:
            return "There was a problem with updating"
    else:
        return render_template("update.html", library_to_update=library_to_update)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):

    library_to_delete = Library.query.get_or_404(id)

    try:
        db.session.delete(library_to_delete)
        db.session.commit()
        return redirect("/home")
    except:
        return "There was a problem with deleting"
