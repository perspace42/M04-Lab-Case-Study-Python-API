'''
Author: Scott Field
Date: 04/16/2023
Program Name: book_application
Program Purpose:
Create a CRUD API for a Book instead of Drink using the video example: https://www.youtube.com/watch?v=qbLc5a9jdXo
'''

from flask import Flask,request
app = Flask(__name__)
from flask_sqlalchemy import flask_SQLAlchemy

#configure database link
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#create book class
class Book(db.Model):
    #book must have an ID number as primary key
    id = db.Column(db.Integer, primary_key=True)
    #book must have a name (which is not necessarily unique)
    book_name = db.Column(db.String(80), nullable = False) 
    #book must have an author (which is not necessarily unique)
    author = db.Column(db.String(50), nullable = False)
    #book must have a publisher (which is not necessarily unique)
    publisher = db.Column(db.String(50), nullable = False)

    #reproduce the data contained within Book
    def __repr__(self):
        return (f"{self.id} - {self.book_name} - {self.author} - {self.publisher}")

#check if connection has been established
@app.route('/')
def index():
    return 'Connection To Database Is Functioning'

#get all bboks in database
@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher' : book.publisher}

        output.append(book_data)
    return {"books": output}

#get a book from database by querying its ID
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher' : book.publisher}

#post a book to database
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(id=request.json['id'],book_name=request.json['book_name'],author = request.json['author'],publisher = request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

#delete a book from database
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "delete performed successfully"}