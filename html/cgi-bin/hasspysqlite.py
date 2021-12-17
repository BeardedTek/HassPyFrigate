#!/usr/bin/python
import sqlite3
from sqlite3 import Error
class hasspysqlite:
    def __init__(self,debug=False):
        self.conn = None
        self.error = ""
        self.version = ""
        self.debug = debug

    def open(self,db="default.sqlite"):
        try:
            if self.debug:
                print(f"connecting to {db}.....\n")
            self.conn = sqlite3.connect(db)
        except Error as e:
            self.error = e
            if self.debug:
                print(f"Gathered Error Message: {self.error}\n")

    def close(self):
        if self.debug:
            print("Is the connecion open?\n")
        if self.conn:
            if self.debug:
                print("yes.  yes it is.\n")
            self.conn.commit()
            if self.debug:
                print("committing")
            self.conn.close()
            if self.debug:
                print("closed.\n")
    
    def execute(self,sql):
        retval = []
        e = ""
        try:
            exe = self.conn.execute(sql)
            if self.debug:
                print(f"Executed SQL: {sql}")
            retval = [0,sql,exe]
        except Error as e:
            retval = [1,sql,str(e).split(":")]
        finally:
            self.close()
            print(retval)
            return retval
    
    def retrieve(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close
        return records