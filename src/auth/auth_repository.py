import pymysql.cursors
import db_auth

class MenuRepository:
    def __init__(self) -> None:
        self.login = db_auth.db_login