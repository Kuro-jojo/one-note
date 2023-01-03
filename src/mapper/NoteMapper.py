import sqlite3
from db import db
from mapper.TagMapper import TagMapper
from model.note import Note
from model.tag import Tag

class NoteMapper:
    DB_FILE:str
    
    @staticmethod
    def add_note(note:Note):
        """
        Add a new note
        :param note:
        :return:
        """     
        conn = db.get_db(NoteMapper.DB_FILE) 
        sql_query = "INSERT INTO note (title, content, createdAt) VALUES (?, ?, ?)"
        cursor = conn.cursor()            
        cursor.execute(sql_query, (note.title, note.content, note.createdAt))
        conn.commit()
        conn.close()
        print("INSERTION REUSSIE")
        
        return cursor.lastrowid
    
    @staticmethod  
    def find(note_id:int)->Note:
        """Return a specific note 

        Args:
            note_id (int): the id of the note
            db_file (str)
        Returns:
            Note: the full note object
        """
        conn = db.get_db(NoteMapper.DB_FILE) 
        
        sql_query = "SELECT * FROM note WHERE id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (note_id,))
        r = cursor.fetchone()
        
        return NoteMapper.to_Note_object(r)
    
    
    @staticmethod
    def find_all()->list:
        """Return all notes

        Returns:
            list: the list of all notes
        """
        conn = db.get_db(NoteMapper.DB_FILE) 
        
        sql_query = "SELECT * FROM note"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        r = cursor.fetchall()
        notes = []
        for note in r:
            notes.append(NoteMapper.to_Note_object(note))
        
        return notes
    
    @staticmethod
    def find_by_tag(tag_id:int)->list:
        """Return all notes with the same tag

        Returns:
            list: the list of all notes
        """
        conn = db.get_db(NoteMapper.DB_FILE) 
        
        sql_query = "SELECT note_id FROM note_tag WHERE tag_id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag_id,))
        
        r = cursor.fetchall()
        notes = []
        for id in r:
            notes.append(NoteMapper.find(id[0]))
        
        return notes
    
    @staticmethod    
    def update(note:Note):
        """update a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(NoteMapper.DB_FILE) 

        sql_query = '''UPDATE note SET 
                        title=?, content=?, createdAt=? WHERE id=?
                    '''
        cursor = conn.cursor()
            
        cursor.execute(sql_query, (note.title, note.content, note.createdAt, note.id))
        conn.commit()
        conn.close()
    
    
    
    @staticmethod    
    def delete(id:int):
        """delete a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(NoteMapper.DB_FILE) 

        sql_query = '''DELETE FROM note WHERE id=?
                    '''
        cursor = conn.cursor()
        
        cursor.execute(sql_query, (id,))
        conn.commit()
        conn.close()
        print("DELETION COMPLETE")
    
    @staticmethod
    def add_tag(note_id:int, tag_id:int):
        """Add a tag to the note
        Args;
            note_id:
            tag_id:
        """     
        
        conn = db.get_db(NoteMapper.DB_FILE) 
        sql_query = "INSERT INTO note_tag (note_id, tag_id) VALUES (?, ?)"
        cursor = conn.cursor()
        
        cursor.execute(sql_query, (note_id, tag_id))
        conn.commit()
        conn.close()
        print("INSERTION REUSSIE")
    
    @staticmethod    
    def remove_tag(note_id:int, tag_id:int):
        """delete a tag from a note

        Args:
            note (Note): the current note object
        """ 
        conn = db.get_db(NoteMapper.DB_FILE) 

        sql_query = '''DELETE FROM note_tag WHERE note_id=? AND tag_id=?
                    '''
        cursor = conn.cursor()
        
        cursor.execute(sql_query, (note_id, tag_id))
        conn.commit()
        conn.close()
        print("DELETION COMPLETE")
        
    @staticmethod  
    def to_Note_object(note:tuple)->Note:

        return Note(note[1], note[2], note[3] , note[0])