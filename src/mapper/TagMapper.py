import sqlite3
from db import db
from model.tag import Tag

class TagMapper:
    
    @staticmethod
    def add_tag(tag:Tag, db_file:str):
        """
        Add a new Tag
        :param Tag:
        :return:
        """ 
        conn = db.get_db(db_file) 
     
        sql_query = "INSERT INTO tag (title, color) VALUES (?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag.title, tag.color))
        conn.commit()
        conn.close()

    @staticmethod        
    def find(tag_id:int, db_file:str)->Tag:
        """Return a specific Tag 

        Args:
            Tag_id (int): the id of the Tag

        Returns:
            Tag: the full Tag object
        """
        conn = db.get_db(db_file) 

        sql_query = "SELECT title, color FROM tag WHERE id=?"
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag_id,))
        
        r = cursor.fetchone()
        tag = None
        if r:
            tag = Tag(r[1], r[2],id=tag_id)
        
        return tag
    
    @staticmethod
    def find_all(db_file:str)->list:
        """Return all Tags

        Returns:
            list: the list of all Tags
        """
        conn = db.get_db(db_file) 

        
        sql_query = "SELECT title, color FROM tag"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        return cursor.fetchall()

    @staticmethod        
    def update(tag:Tag, db_file:str):
        """update a tag

        Args:
            tag (Tag): the current tag object
        """ 
        conn = db.get_db(db_file) 

        
        sql_query = '''UPDATE tag SET 
                        title=?, color=?
                    '''
        cursor = conn.cursor()
        cursor.execute(sql_query, (tag.title, tag.color))
        conn.commit()
        conn.close()