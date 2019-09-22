# All the queries

update_data = """ UPDATE LIBRARY SET exittime=?, is_in=? WHERE (sapid,is_in)=(?,?);"""

check_entry_data = """ SELECT * FROM LIBRARY WHERE (sapid,in_date,is_in)=(?,?,?); """

insert_data = """ INSERT INTO LIBRARY ( sapid, in_date, entrytime, is_in, is_teacher) VALUES ( ?,?,?,?,? );"""

retrieve_all_data = """SELECT * FROM LIBRARY"""

count_insertion = """SELECT * FROM LIBRARY WHERE is_teacher=?;"""

# paths

path_to_database = "database/"

path_to_media = "media/"

path_to_pdfs = "pdfs/"