import sqlite3
from db import db
from model.tag import Tag

class TagMapper:
    
    DB_FILE:str
    
    @staticmethod
    def add_tag(tag:Tag):
        """
        Add a new Tag
        :param Tag:
        :return:
        """ 
        conn = db.get_db(TagMapper.DB_FILE) 
     
        sql_query = "INSERT INTO tag (title, color) VALUES (?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag.title, tag.color))
        conn.commit()
        conn.close()

    @staticmethod        
    def find(tag_id:int)->Tag:
        """Return a specific Tag 

        Args:
            Tag_id (int): the id of the Tag

        Returns:
            Tag: the full Tag object
        """
        conn = db.get_db(TagMapper.DB_FILE) 

        sql_query = "SELECT * FROM tag WHERE id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag_id,))
        
        r = cursor.fetchone()
        
        return TagMapper.to_Tag_object(r)
    
    @staticmethod
    def find_all()->list:
        """Return all Tags

        Returns:
            list: the list of all Tags
        """
        conn = db.get_db(TagMapper.DB_FILE) 

        
        sql_query = "SELECT * FROM tag"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        r = cursor.fetchall()
        tags = []
        for tag in r:
            tags.append(TagMapper.to_Tag_object(tag))
            
        return tags

    @staticmethod
    def find_by_note(note_id:int)->list:
        """Return all tag affected to a note

        Returns:
            list: the list of all tags
        """
        conn = db.get_db(TagMapper.DB_FILE) 
        
        sql_query = "SELECT tag_id FROM note_tag WHERE note_id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (note_id,))
        
        r = cursor.fetchall()
        tags = []
        for id in r:
            tags.append(TagMapper.find(id[0]))
        
        return tags

    @staticmethod        
    def update(tag:Tag):
        """update a tag

        Args:
            tag (Tag): the current tag object
        """ 
        conn = db.get_db(TagMapper.DB_FILE) 

        
        sql_query = '''UPDATE tag SET 
                        title=?, color=?
                    '''
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag.title, tag.color))
        conn.commit()
        conn.close()
        
    @staticmethod  
    def to_Tag_object(tag:tuple)->Tag:

        return Tag(tag[1], tag[2], tag[0])