def get_insert_sql_commodity(result={}):
    insert_sql = "insert into  commodity_id(commodity_id,commodity_name, commodity_status) \
                values('%s','%s','%s')" % \
                 (result["commodity_id"], result["commodity_name"], result["commodity_status"])
    return insert_sql


def get_update_sql_commodity(result={}):
    update_sql = "update commodity_id set commodity_status='%s' where commodity_id ='%s'" \
                 % (result["commodity_status"], result["commodity_id"])
    return update_sql


def get_insert_sql_ip(result={}):
    insert_sql = "insert into ippool (id,ip,port,time,status,level) \
                    values('%s','%s','%s','%s','%s','%s')" % \
                 (result["id"], result["ip"], result["port"], result["time"], result["status"], result["level"])
    return insert_sql


def get_update_sql_ip(result={}):
    update_sql = "update ippool set ip='%s',port='%s',time='%s',status='%s',level='%s' where id ='%s'" \
                 % (result["ip"], result["port"], result["time"], result["status"],result["level"] ,result["id"])
    return update_sql


def get_insert_sql_comment(result={}):
    sql = "insert into comments (commodity_name,commodity_id,user_id,comments,productsize)  \
        values('%s','%s','%s','%s','%s')" \
          % ( result["commodity_name"], result["commodity_id"], result["user_id"], result["comments"],
             result["size"])
    return sql
