#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

from dbconn import db_cursor

def create_db():
    sqlstr = """
    DROP TABLE IF EXISTS course;

    CREATE TABLE IF NOT EXISTS course  (
        cou_sn   INTEGER,     --序号
        stu_no   TEXT,        --学号
        cou_no   TEXT,        --出生日期
        name     TEXT,        --姓名
        sex    TEXT,          --性别
        grade   TEXT,          --班级
        PRIMARY KEY(cou_sn)
    );
    -- CREATE UNIQUE INDEX idx_course_no ON course(cou_no);

    CREATE SEQUENCE seq_cou_sn 
        START 10000 INCREMENT 1 OWNED BY course.cou_sn;

    """
    with db_cursor() as cur :
        cur.execute(sqlstr) # 执行SQL语句
    
def init_data():
    sqlstr = """
    DELETE FROM course;

    INSERT INTO course (cou_sn, stu_no, cou_no, name, sex,grade)  VALUES 
        (101, '1310650412', '1995-01-02',  '张三', '男','信息1304'), 
        (102, '1310650411',  '1994-03-04',  '李四', '女','会计1302'),
        (103, '1310650413',  '1994-09-12',  '王五', '男','工商1301');

    """
    with db_cursor() as cur :
        cur.execute(sqlstr)    

if __name__ == '__main__':
    create_db()
    init_data()
    print('数据库已初始化完毕！')

