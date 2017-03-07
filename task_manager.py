import sqlite3
import os.path
import time

import settings

def start(filename):
    if not os.path.exists(filename):
        create_database(filename)

def create_database(filename):
    category = """
        create table category (
            categoryid integer primary key autoincrement,
            categoryname varchar(30)
        )
    """

    work = """
        create table work (
            workname varchar(30),
            categoryid integer,
            worktype character(3),
            starttime integer primary key,
            endtime integer
        )
    """
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute(category)
    cur.execute(work)
    conn.close()

def database_add(query, values):
    conn = sqlite3.connect(settings.SQLITE)
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    conn.close()

def database_show(query):
    rows = []
    conn = sqlite3.connect(settings.SQLITE)
    cur = conn.cursor()
    for row in cur.execute(query):
        rows.append(row)
    conn.close()
    return rows

def add_category(name):
    print("add category: {}".format(name))
    query = "insert into category (categoryname) values (?)"
    category = (name,)
    database_add(query, category)

def show_category():
    print("show category")
    query = "select * from category"
    return database_show(query)

def add_work(workname, categoryid, worktype):
    query = "update work set endtime = ? where endtime is null"
    work = (int(time.time()),)
    database_add(query, work)
    query = "insert into work (workname, categoryid, worktype, starttime) values (?,?,?,?)"
    work = (workname, categoryid, worktype, int(time.time()))
    database_add(query, work)

def show_work():
    query = """
        select work.starttime, work.workname, work.worktype, work.categoryid, work.starttime, work.endtime, category.categoryname
        from work inner join category
        on work.categoryid = category.categoryid
    """
    return database_show(query)
