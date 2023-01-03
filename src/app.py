import datetime
from markupsafe import escape
from flask import Flask,  render_template, request, url_for, redirect

from db import db
from mapper.NoteMapper import NoteMapper
from mapper.TagMapper import TagMapper
from model.note import Note
from model.tag import Tag

DB_FILE = "db/app.db"
SQL_SCRIPT = "db/scheme.sql"

app = Flask(__name__)

# INIT MAPPER'S VARIABLES
NoteMapper.DB_FILE = DB_FILE
TagMapper.DB_FILE = DB_FILE


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/note/")
def note_index():
    
    notes = NoteMapper.find_all()
    tags = TagMapper.find_all()

    return render_template("note/index.html", notes=notes, tags=tags, default_tag="Trier par tag")

@app.route("/note/add/", methods=['GET', 'POST'])
def add_note():
    tags = TagMapper.find_all()
    
    if request.method == 'POST':
        data = request.form
        
        if is_data_valid(data.listvalues()):
            note = Note(data['title'], data['content'], datetime.date.today())
            note.id = NoteMapper.add_note(note)
            for key in data:
                if key.startswith('tag'):
                    NoteMapper.add_tag(note_id=note.id, tag_id=data[key]) # pass the tag id to the function
                    
            
            return redirect(url_for("note_index"))
        
    return render_template("note/add.html", tags=tags)

@app.route("/note/<int:id>")
def get_note(id:int):
    note = NoteMapper.find(id)
    
    return render_template("note/view.html", note=note)

@app.route("/note/edit/<int:id>", methods=['GET', 'POST'])
def edit_note(id:int):
    note = NoteMapper.find(id)
    tags_affected = TagMapper.find_by_note(note.id)
    tags = TagMapper.find_all()
    tags = [tag for tag in tags if tag not in tags_affected]
    
    if request.method == 'POST':
        data = request.form
        if is_data_valid(data.listvalues()):
            note.title = data['title']
            note.content = data['content']
            c=[]
            for key in data:
                if key.startswith('tag'):
                    if int(data[key]) not in [tag.id for tag in tags_affected]:
                        NoteMapper.add_tag(note_id=note.id, tag_id=data[key]) # pass the tag id to the function
                    else:
                        c.append(int(data[key]))
            
            if len(c) < len(tags_affected):
                for t in tags_affected:
                    if t.id not in c:
                        NoteMapper.remove_tag(note.id, t.id)
                        
            NoteMapper.update(note)
            
            return redirect(url_for("get_note", id=id))
    
    return render_template("note/edit.html", note=note, tags=tags, tags_affected=tags_affected)

@app.route("/note/delete/<int:id>")
def delete_note(id:int):
    NoteMapper.delete(id)
    return redirect(url_for("note_index"))

@app.route("/note/tag/<int:id>")
def get_notes_by_tag(id):
    
    tag = TagMapper.find(id)
    tags = TagMapper.find_all()
    notes = NoteMapper.find_by_tag(id)
    
    if len(notes) == 0:
        return redirect(url_for("note_index"))
    return render_template("note/index.html",notes=notes, current_tag=tag, tags=tags)
    
    
@app.route("/tag/add", methods={'GET', 'POST'})
def add_tag():
    if request.method == 'POST':
        data = request.form

        if is_data_valid(data.listvalues()):
            tag = Tag(data['title'], data['color'])
            TagMapper.add_tag(tag)
            
            return redirect(url_for("note_index"))
    return render_template("tag/add.html")
    
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