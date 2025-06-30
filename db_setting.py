import pymysql
from database import MyDB

# MyDB class 생성 
mydb = MyDB(
    _host = 'Jay00.mysql.pythonanywhere-services.com',
    _port = 3306,
    _user = 'Jay00',
    _pw = '1234',
    _db_name = 'Jay00$default'
)


# table 생성 쿼리문 
create_user = """
    create table  
    if not exists 
    user (
    id varchar(32) primary key,
    password varchar(64) not null, 
    name varchar(32) 
    )
"""
# sql 쿼리문을 실행
mydb.sql_query(create_user)
# db server에 동기화하고 연결을 종료 
mydb.commit_db()





# _db = pymysql.connect(
#     host = 'moons9303.mysql.pythonanywhere-service.com', 
#     port = 3306, 
#     user = 'moons9303', 
#     password = 'moon1234', 
#     db = 'moons9303$ubion'
# )
