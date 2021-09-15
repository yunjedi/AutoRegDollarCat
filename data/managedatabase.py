import subprocess

import psutil
import psycopg2
import sqlite3 as db

# error code 2 : can not find elemenent , error code 3: network error
# [('id',), ('username',), ('password',), ('location',), ('create_date',)] -   table account
def select_data():
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute("SELECT * from account where registered = 0")
    list_tb = cur.fetchall()
    cur.close()
    conn.close()
    return list_tb


def insert_data(username, password):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute("insert into account (username, password) values ('" + username + "', '" + password + "')")
    conn.commit()
    cur.close()
    conn.close()


def update_data(username, location, create_date):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute(
        "update account set location = '" + location + "', create_date = '" + create_date + "' where username = '" + username + "'")
    conn.commit()
    cur.close()
    conn.close()


def update_registered(username):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute(
        "update account set registered = 1 where username = '" + username + "'")
    conn.commit()
    cur.close()
    conn.close()

def update_error_code_2(username):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute(
        "update account set registered = 2 where username = '" + username + "'")
    conn.commit()
    cur.close()
    conn.close()

def update_error_code_3(public_ip):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute(
        "update account set registered = 3 where public_ip = '" + public_ip + "'")
    conn.commit()
    cur.close()
    conn.close()

# def delete_user(username):
#     conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
#     cur = conn.cursor()
#     cur.execute(
#         "delete from account where username = '" + username + "'")
#     conn.commit()
#     cur.close()
#     conn.close()

def update_user_agent(useragent,username):
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute(
        "update account set user_agent = '" + useragent + "' where username = '" + username + "'")
    conn.commit()
    cur.close()
    conn.close()



def show_data():
    # print(select_data())
    print(len(select_data()))
    conn = psycopg2.connect(host="192.168.1.150", dbname='catcoin', user='cat', password='123456')
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'account'")
    data = cur.fetchall()
    print(data)

def kill(proc_pid):
    try:
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except:
        return

def connect_SSH(hostip, username, password):
    command = r'cmd.exe /c echo y | plink  -D 1337  -N ' + username + r'@' + hostip + ' -pw ' + password
    # my_env = os.environ.copy()
    cmd = subprocess.Popen(command)

    return cmd.pid

# show_data()