from mainDAL import *

def addNewUser(username, password):
    query = """insert into DbMysql12.users_table values ('"""+username+"""','"""+password+"""');"""
    con = DBconnection()
    if (con.insertQuery(query)):
        con.close()
        return True
    
    con.close()
    print(con._exception)
    return False