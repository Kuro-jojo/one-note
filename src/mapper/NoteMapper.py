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
        tag_id = "null"
        if note.tag:
            tag_id = note.tag.id
            
        cursor.execute(sql_query, (note.title, note.content, note.createdAt, tag_id))
        conn.commit()
        conn.close()
        print("INSERTION REUSSIE")
    
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
        
        return NoteMapper.to_Note_object(r, db_file)
    
    @staticmethod
    def find_all(db_file:str)->list:
        """Return all notes

        Returns:
            list: the list of all notes
        """
        conn = db.get_db(db_file) 
        
        sql_query = "SELECT * FROM note"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        r = cursor.fetchall()
        notes = []
        for note in r:
            notes.append(NoteMapper.to_Note_object(note, db_file))
        
        return notes
    
    @staticmethod    
    def update(note:Note, db_file:str):
        """update a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(db_file) 

        sql_query = '''UPDATE note SET 
                        title=?, content=?, createdAt=?, tag_id=? WHERE id=?
                    '''
        cursor = conn.cursor()
        
        tag_id = "null"
        if note.tag:
            tag_id = note.tag.id
            
        cursor.execute(sql_query, (note.title, note.content, note.createdAt, tag_id, note.id))
        conn.commit()
        conn.close()
    
    
    
    @staticmethod    
    def delete(id:int, db_file:str):
        """delete a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(db_file) 

        sql_query = '''DELETE FROM note WHERE id=?
                    '''
        cursor = conn.cursor()
        
        cursor.execute(sql_query, (id,))
        conn.commit()
        conn.close()
        print("DELETION COMPLETE")
    
    
    @staticmethod  
    def to_Note_object(note:tuple, db_file)->Note:
        tag = None
        if note[4] != "null":
            tag = TagMapper.find(int(note[4]), db_file)
        
        return Note(note[1], note[2], note[3], tag , note[0])