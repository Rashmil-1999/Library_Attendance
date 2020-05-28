# Primary imports
import sqlite3
from datetime import datetime
from sqlite3 import Error
from playsound import playsound
import os


from query import create_table, check_entry_data, insert_data, update_data
from create_pdf import pdf_generation
import constants


if not os.path.exists("media"):
    os.mkdir("media")

if not os.path.exists("database"):
    os.mkdir("database")

if not os.path.exists("pdfs"):
    os.mkdir("pdfs")


def validate_sap_id(sap_id):
    """
    Validation of the SAP_ID to be entered by ID Card Scanner
    """
    size = len(sap_id)
    if size == 7 and sap_id[0] is not "0" and sap_id[0] == 9:
        return "1" + sap_id, 1
    elif size == 3 and sap_id[0] is not "0":
        return sap_id, 1
    elif size == 11:
        return sap_id, 0
    else:
        playsound(constants.path_to_media + "Try_again.mp3")
        return None, -1


def create_table_connection():
    """
    Create Table and establish connection
    """
    str_date = datetime.now().strftime("%b-%Y")
    file_name = constants.path_to_database + "library-" + str_date + ".db"
    conn = sqlite3.connect(file_name)
    try:
        c = conn.cursor()
        c.execute(create_table)
        return conn
    except Error as e:
        print(e)


def data_entry(conn, sap_id):
    """
    Entry of SAP_ID and check if entry already exists with Out time as none
    then update it else create a new entry.Also checks if entered SAP_ID is of student
    or teacher
    """
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    sap_id, is_teacher = validate_sap_id(sap_id)
    c = conn.cursor()
    if sap_id is not None:
        c.execute(check_entry_data, (sap_id, date, 1))
        row = c.fetchall()

        if is_teacher == -1:
            return
        else:
            if row:
                c.execute(update_data, (time, 0, sap_id, 1))
            else:
                c.execute(insert_data,
                          (sap_id, date, time, 1, is_teacher))
            conn.commit()


def main():
    """
    Main function to start the system
    """
    c = create_table_connection()
    sap_id = ""
    while sap_id is not "q":
        sap_id = input("Enter the SAP ID:")

        if sap_id not in ["q", "p", "r", ""]:
            data_entry(c, sap_id)
        elif sap_id is "p":
            str_date = datetime.now().strftime("%b-%Y")
            pdf_generation(str_date, c)
        elif sap_id is "r":
            name = input("Enter database month:\nfor example Aug-2019:").strip()
            if name is not "q":
                file_name = "library-" + name + ".db"
                conn = sqlite3.connect(file_name)
                c = conn.cursor()
                pdf_generation(name, c)
                c.close()
                c = create_table_connection()


if __name__ == "__main__":
    main()
