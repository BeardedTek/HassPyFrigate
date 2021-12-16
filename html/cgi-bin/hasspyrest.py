#!/usr/bin/python
#   HassPyREST - RESTful interface for HassPyFrigate - This is how we insert data
#
#   Copyright (C) 2021  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json

import sys
class hasspyrest:
    def __init__(self):
        self.sql = ""
        self.debug = ""
        print()
    def error_log(self,msg):
        if self.debug:
            sys.stderr.write(f"{str(msg)}\n")
            print(msg)

    def load_json(self,src="POST",file=None):
        if src == 'POST':
            self.input = json.loads(sys.stdin.read())
            self.error_log("RECEIVED\n")
            self.error_log(str(self.input))
        elif src == 'FILE':
            with open(file) as page_json:
                self.input = json.load(page_json)
                
    def parse_json(self):
        self.fields = []
        self.values = []
        self.function = ""
        self.create = []
        if self.input['debug'] == "1" or "true":
            self.debug = True
        else:
            self.debug = False
        self.table = self.input['table']
        self.function = self.input['function']
        for index in self.input['columns']:
            self.fields.append(index)
            value = self.input['columns'][index]
            self.values.append(value)
            if self.function == "CREATE":
                self.create.append([index,value])
        self.error_log(f"table: {self.table}")
        self.error_log(f"function: {self.function}")
        self.error_log(f"fields: {self.fields}")
        self.error_log(f"values: {self.values}")
        return True
    def json2sql(self):
        ##FIXME## Can only handle strings right now...
        # Converts Simple JSON input into SQL string
        #   {
        #     "table": "table_name",
        #     "debug": "1", ## 0 is false 1 is true
        #     "function": "INSERT",
        #     "columns" : {
        #       "event_id": input.getvalue('event_id'),
        #       "camera": input.getvalue('camera'),
        #       "bbox": input.getvalue('bbox')
        #     }
        #  }
        if self.function == "CREATE":
            # CREATE TABLE IF NOT EXISTS events(id integer PRIMARY KEY,
            # event_id text UNIQUE, camera text, bbox text, ack text);
            SQL = f"""CREATE TABLE IF NOT EXISTS {self.table}("""
            for field in self.create:
                if field == self.create[-1]:
                    SQL += f"""{field[0]} {field[1]});"""
                else:
                    SQL += f"""{field[0]} {field[1]},"""
            return SQL
        if self.function == "SELECT":
            # SELECT <{index}>, <{index}>, <{index}>, id from <{input['table']}>
            SQL = """SELECT """
            for field in self.fields:
                if field == self.fields[-1]:
                    SQL += f"""{field} from {self.table}"""
                else:
                    SQL += f"""{field},"""
            return SQL
        elif self.function == "INSERT":
            # INSERT INTO <table> ({index},{index},{index},id) \
            # VALUES ({value}, {value}, {value}, null)
            SQL = f"""INSERT INTO {self.table}("""
            for field in self.fields:
                if field == self.fields[-1]:
                    SQL += f"""{field}) VALUES("""
                else:
                    SQL += f"""{field},"""
            for value in self.values:
                if value == self.values[-1]:
                    SQL += f"""'{value}')"""
                else:
                    SQL += f"""'{value}',"""
            return SQL

            
        

def main():
    from hasspysqlite import hasspysqlite
    #Initial py2jsql
    j2sql=hasspyrest()
    # Print headers in case we're talking to a web browser...
    j2sql.error_log("content-type: text/plain\n\n")
    # First, let's create the database if it doesn't exist
    j2sql.load_json("FILE","/var/www/db/json/events.json")
    j2sql.parse_json()
    sql = j2sql.json2sql()
    hpsql = hasspysqlite()
    hpsql.open("/var/www/db/hasspyfrigate.sqlite")
    if hpsql.error:
        j2sql.error_log(f"Error: {hpsql.error}")
    else:
        temp = hpsql.execute(sql)
        j2sql.error_log(temp)

    # Now Since we know it exists, lets run our SQL...
    j2sql.load_json()
    j2sql.parse_json()
    sql = j2sql.json2sql()
    j2sql.error_log(sql)
    hpsql = hasspysqlite()
    hpsql.open("/var/www/db/hasspyfrigate.sqlite")
    if hpsql.error:
        j2sql.error_log(f"Error: {hpsql.error}")
    else:
        temp = hpsql.execute(sql)
        j2sql.error_log(temp)
    j2sql.error_log("OK")
    

            

main()



#def main():
#    # Print HTTP header
#    print('content-type: text/plain\n\n')
#    hpsql = hasspysqlite()
#    hpsql.open()
#    if hpsql.error:
#        print(f"Error: {hpsql.error}")
#    else:
#        if hpsql.version:
#            print(f"Version: {hpsql.version}")
#        sql_create_events = """
#            CREATE TABLE IF NOT EXISTS events(
#                id integer PRIMARY KEY,
#                event_id text UNIQUE,
#                camera text,
#                bbox text
#            );"""
#        hpsql.write(sql_create_events)
#        if hpsql.insert_event():
#            sql_insert = hpsql.insert_event()
#        else:
#            if hpsql.debug:
#                print(f" {hpsql.insert_event()}")
#            sql_insert = """
#            INSERT INTO events(event_id,camera,bbox)
#            VALUES("1639182727.378887-4zp8bd","driveway","1");
#            """
#        hpsql.write(sql_insert)
#        read_json = {
#            "table": "events",
#            "columns": {
#                "event_id": "Event ID",
#                "camera": "Camera",
#                "bbox": "Bounding Box"
#            }
#        }
#        hpsql.read(read_json)
#    hpsql.close()
#
#main()