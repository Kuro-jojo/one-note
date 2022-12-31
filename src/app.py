import datetime
from markupsafe import escape
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

from db import db
from mapper.NoteMapper import NoteMapper
from mapper.TagMapper import TagMapper
from model.note import Note
from model.tag import Tag

DB_FILE = "db/app.db"
SQL_SCRIPT = "db/scheme.sql"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/note/")
def note_index():
    notes = NoteMapper.find_all(DB_FILE)
    
    return render_template("note/index.html",notes=notes)

@app.route("/note/add/", methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        data = request.form
        if is_data_valid(data.listvalues()):
            tag = Tag("Tag 1", "black")
            TagMapper.find(0)
            note = Note(data['title'], data['content'], datetime.date.today(), tag)
            note.tag = tag
            NoteMapper.add_note(note)
            return note_index()
        
    return render_template("note/add.html")

@app.route("/note/<int:id>")
def get_note(id:int):
    note = NoteMapper.find(id, DB_FILE)
    print(note)
    
    return escape(note)

@app.route("/todo/")
def todo_index():

    return render_template("note/index.html")


def is_data_valid(data:list)->bool:
    for d in data:
        if not d[0]:
            return False
    return True

# with app.app_context():
#     db.init_db(DB_FILE, SQL_SCRIPT)