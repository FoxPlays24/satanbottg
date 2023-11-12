import mysql.connector
from mysql.connector import Error, Warning

db = mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_devil",
        password="2y6m*BqEcEKKc@b",
        database="freedb_lamborgini"
    )

cursor = db.cursor(buffered=True)

def execute(query,*value):
    try:
        cursor.execute(query,value)
        db.commit()
    except (Error, Warning) as e:
        print(e)
        
print("БД успешно подключена!")