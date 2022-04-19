import requests
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
db_host = str(os.environ.get("MYSQL_HOST"))
db_user = str(os.environ.get("MYSQL_USER"))
db_name = str(os.environ.get("MYSQL_DATABASE"))
token = str(os.environ.get("token"))


def groupLists():
    db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd="",
    database=db_name
)
    cursor = db.cursor()
    sql = "SELECT group_id FROM tb_broadcast WHERE sent = 0"
    cursor.execute(sql)
    hasil = cursor.fetchall()
    return tuple(hasil)

def sendBroadcast(list, msg):
    db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd="",
    database=db_name
)
    try:
        for group_id in list:
            url_req = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML".format(token, group_id[0], msg)
            results = requests.get(url_req)
            print(results.text)
            print("Pesan Sukses Terkirim ke",group_id)
            cursor = db.cursor()
            # cursor.execute("UPDATE tb_broadcast SET sent=%s WHERE group_id=%s",(1,group_id[0]))
            # db.commit()
        print('mantap')
    except:
        print("error")
        
    
list = groupLists()

sendBroadcast(
    list=list,
    msg='Ini adalah Pesan Broadcast'
)

        