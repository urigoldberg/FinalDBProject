from mainDAL import *

def addNewUserDAL(username, password):
    query = """insert into DbMysql12.users_table values ('"""+username+"""','"""+password+"""');"""
    con = DBconnection()
    if (con.insertQuery(query)):
        con.close()
        return True
    
    con.close()
    print(con._exception)
    return False


def getUserPasswordUsernameDAL(username):
    query = "select password from DbMysql12.users_table where user_name = '"+username+"';";
    con = DBconnection()
    if (con.selectQuery(query) and con._rowsReturned == 1):
        con.close()
        return con._results[0][0]
    return None
        

    
    con.close()
    print(con._exception)
    return False