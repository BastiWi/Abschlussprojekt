# Module Imports
import mysql.connector
import sys
import time
from glob import * 


dir = "C:\\Users\\sewi273376\Desktop\\Abschlussproject stuff\\AbschlussProjekt\\JIRA_TicketClone\\report\\"
for file in glob(dir + "/*.html"):
   linkname = file



def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

curr_time = time.localtime()

class table_insert_reports():
    # Connect to mySQL Platform
    try:
        conn = mysql.connector.connect(
            user="root",
            password="",
            host="127.0.0.1",
            port=3306,
            database="jtc_db"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to mySQL Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    cur.execute("SHOW TABLES")

    for x in cur:
        print(x)

    link = linkname
    file = convertToBinaryData("Test-Report.txt")
    sql = "INSERT INTO mails (testreport, link) VALUES (%s, %s)"
    val = (file, link)
    cur.execute(sql, val)

    conn.commit()