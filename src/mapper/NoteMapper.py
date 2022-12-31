import sqlite3
from db import db
from mapper.TagMapper import TagMapper
from model.note import Note

class NoteMapper:
    
    @staticmethod
    def add_note(note:Note, db_file:str):
        """
        Add a new note
        :param note:
        :return:
        """     
        conn = db.get_db(db_file) 
        sql_query = "INSERT INTO note (title, content, createdAt, tag_id) VALUES (?, ?, ?, ?)"
        cursor = conn.cursor()

        cursor.execute(sql_query, (note.title, note.content, note.createdAt, note.tag.id))
        print("INSERTION: " , cursor.lastrowid)
        conn.commit()
        conn.close()
    
    @staticmethod  
    def find(note_id:int, db_file:str)->Note:
        """Return a specific note 

        Args:
            note_id (int): the id of the note
            db_file (str)
        Returns:
            Note: the full note object
        """
        conn = db.get_db(db_file) 
        
        sql_query = "SELECT * FROM note WHERE id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (note_id,))
        r = cursor.fetchone()
        tag = TagMapper.find(int(r[4]), db_file)
        
        note = Note(r[1], r[2], r[3], tag , note_id)
        
        return note
    
    @staticmethod
    def find_all(db_file:str)->list:
        """Return all notes

        Returns:
            list: the list of all notes
        """
        conn = db.get_db(db_file) 
        
        sql_query = "SELECT title, content, createdAt, tag_id FROM note"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        return cursor.fetchall()
    
    @staticmethod    
    def update(note:Note, db_file:str):
        """update a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(db_file) 

        sql_query = '''UPDATE note SET 
                        title=?, content=?, createdAt=?, tag_id=?
                    '''
        cursor = conn.cursor()
        cursor.execute(sql_query, (note.title, note.content, note.createdAt, note.tag.id))
        conn.commit()
        conn.close()