import pymysql.cursors


def connectDB():
    print("ENTER")
    return pymysql.connect(host='den1.mysql2.gear.host',
                             user='sqqql',
                             password='Hp0eP1?vu~yv',
                             db='sqqql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def disconnectDB(connection):
    print("EXIT")
    connection.close()

def insert(connection, data, db):
    with connection.cursor() as cursor:

        if db == 'CardPayments':
            sql = "insert into CardPayments (card_num, expire_date, cvc, amount, comments, email)" \
              "values (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,
                       (data['cardNumber'], data['expireDate'], data['cvc'],
                        data['amount'], data['comments'], data['email']))
        elif db == 'RequirePayments':
            sql = "insert into RequirePayments (name, bik, account_num, nds, amount, tel_number, email)" \
                  "values (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,
                           (data['name'], data['bik'], data['numAccount'],
                            data['nds'], data['amount'], data['tel_number'], data['email']))
    connection.commit()

def selectAll(connection, db):
    with connection.cursor() as cursor:
        sql = "select * from "+db
        print (sql)
        cursor.execute(sql)

        return cursor.fetchall()

def orderby(connection, field, order, db):
    with connection.cursor() as cursor:
        sql = "select * from "+ db +" order by " + field + " " + order
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()

def filter(connection, field, filter,db):
    with connection.cursor() as cursor:
        sql = "select * from "+ db +" " \
              "where "+ field +" like '%"+filter+"%'"
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()

def alterTrust(connection, index):
    with connection.cursor() as cursor:
        sql = "select notSafe from CardPayments where id="+str(index)
        cursor.execute(sql)
        if cursor.fetchone()['notSafe'] == 0:
            result = 1
        else:
            result = 0
        sql = "update CardPayments set notSafe="+str(result)+" where id="+str(index)
        cursor.execute(sql)
    connection.commit()