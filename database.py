import sqlite3 as sql
from os.path import exists
from settings import Settings

class Database:
    def __init__(self):
        self.codec = "utf-8"
        file_exists = exists("base.sqlite")
        self.sql = sql.connect("base.sqlite",check_same_thread=False)
        self.cursor = self.sql.cursor()
        self.cursor.execute("""
        CREATE TABLE if NOT EXISTS user (
        login TEXT,
        user_id TEXT, 
        first_name TEXT, 
        last_name TEXT,
        is_bot INT,
        lang TEXT,
        level INT,
        limits INT)
        """)
        self.cursor.execute("""
        CREATE TABLE if NOT EXISTS admins (
        user_id TEXT)
        """)
        if(not file_exists):
            self.add_admin(Settings.default_admin_id)
    


    def id_exist(self, id):
        return self.cursor.execute(f"SELECT COUNT(*) FROM user WHERE user_id = '{id}'").fetchone()[0]
    
        
    def get_limit(self, user_id:str):
        self.cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
        return self.cursor.fetchone()[7]
        
    def info(self, user_id:str):
        self.cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
        u_data = self.cursor.fetchone()
        _login = u_data[0]
        _user_id = u_data[1]
        _first_name = u_data[2]
        _last_name = u_data[3]
        _isbot = u_data[4]
        _lang = u_data[5]
        _limits = u_data[7]

        if(_isbot == 0):
            _isbot = "User"
        else:
            _isbot = "Bot"
        
        u_info = f"""
        __________________________________
            | Login: {_login}          
            | Kullanıcı id: {_user_id} 
            | Ad: {_first_name}        
            | Soyad: {_last_name}      
            | Durum: {_isbot}          
            | Dil: {_lang}             
            | Limit: {_limits}         
__________________________________
        """
        return u_info


    
    def get_level(self, user_id:str):
        self.cursor.execute(f"SELECT * FROM user WHERE user_id = {user_id}")
        return self.cursor.fetchone()[6]
    
    def all_user_info(self):
        all_user_data = ""
        self.cursor.execute(f"SELECT * FROM user")
        all_user_id = self.cursor.fetchall()
        length = len(all_user_id)
        for userData in range(length):
            all_user_data +=self.info(all_user_id[userData][1])+"\n"
        return all_user_data
    def admins(self):
        admin = ""
        self.cursor.execute(f"SELECT * FROM admins")
        admin = self.cursor.fetchall()
        return admin
    
    def set_limit(self,user_id:str):
        self.cursor.execute(f"UPDATE user SET limits = limits + 1 WHERE user_id = {user_id}")
        self.sql.commit()

    def reset_limit(self,user_id:str):
        self.cursor.execute(f"UPDATE user SET limits = 0 WHERE user_id = {user_id}")
        self.sql.commit()
        
    def reset_all(self):
        self.cursor.execute("UPDATE user SET limits = 0")
        self.sql.commit()

    def register(self, register_data):
        user_id = register_data["id"]
        is_bot = register_data["is_bot"]
        if(is_bot == True):
            is_bot = 1
        else:
            is_bot = 0
        first_name = register_data["first_name"]
        last_name = register_data["last_name"]
        username = register_data["username"]
        lang = register_data["language_code"]
        level = 0
        limits= 0

        query = f"""
         INSERT INTO user VALUES(
        '{username}',
        '{str(user_id)}',
        '{first_name}',
        '{last_name}',
        {is_bot},
        '{lang}',
        {level},
        {limits})
        """
        self.cursor.execute(query)
        self.sql.commit()

    def add_admin(self, user_id):
            query = f"""
            INSERT INTO admins VALUES(
            '{str(user_id)}')
            """
            self.cursor.execute(query)
            self.sql.commit()
    
    def remove_admin(self, user_id):
            query = f"""
            DELETE FROM admins WHERE user_id='{str(user_id)}'
            """
            self.cursor.execute(query)
            self.sql.commit()
