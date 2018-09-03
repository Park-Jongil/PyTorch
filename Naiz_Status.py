import urllib.request
import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def select_status_by_key(conn, key):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT seq,status FROM CameraList WHERE seq=?", (key,))
    row = cur.fetchone()
    return row[1]

def update_status_by_key(conn, key , status):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("UPDATE CameraList SET status=? WHERE seq=?", (status, key))        
    conn.commit()


def main():
    database = "NaizDB.db"
    naiz_url = 'http://naiz.re.kr:8001/event/status.cgi?id=admin&password=admin&key=all&method=get'

    conn = create_connection(database)

    file = urllib.request.urlopen( naiz_url ).read().decode('euc-kr')
    root = ET.fromstring(file)
    iCount = 0
    isAlive = 0
    iPrevStatus = 0

    for child in root :
        for sub in child :
            HighStreamConnection = '0'
            LowStreamConnection  = '0'
            iCurrStatus = 0
            for item in sub :
                if (item.tag == 'Key') :      
                    UniqueKey = item.text
                if (item.tag == 'HighStreamConnection') :    
                    HighStreamConnection = item.text  
                if (item.tag == 'LowStreamConnection') :      
                    LowStreamConnection = item.text  
            print("UniqueKey = " + UniqueKey)
#            print("HighStreamConnection  = " + HighStreamConnection)
#            print("LowStreamConnection   = " + LowStreamConnection)
            if (HighStreamConnection=='1') and (LowStreamConnection=='1')  :
                isAlive = isAlive + 1   
                iCurrStatus = 1
            iPrevStatus = select_status_by_key( conn , int(UniqueKey) )
            if (iPrevStatus != iCurrStatus) :
                print(" 상태값 변이가 발생함 Key = " + int(UniqueKey) )
                print("   Prev = " + iPrevStatus ) 
                print("   Current = " + iCurrStatus )                
                update_status_by_key( conn , int(UniqueKey) , iCurrStatus )
            iCount = iCount + 1

    print("\n전체갯수 = " + str(iCount))
    print("\n활성화   = " + str(isAlive))
    conn.close()

if __name__ == '__main__':
    main()

