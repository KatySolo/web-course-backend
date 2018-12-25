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

def insert(connection, data):
    # print(data)
    with connection.cursor() as cursor:
        sql = "insert into CardPayments (card_num, expire_date, cvc, amount, comments, email, notSafe)" \
              "values (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       (data['cardNumber'], data['expireDate'], data['cvc'],
                        data['amount'], data['comments'], data['email'],
                        data['notSafe']))
    connection.commit()

def selectAll(connection):
    with connection.cursor() as cursor:
        sql = "select * from CardPayments"
        cursor.execute(sql)

        return cursor.fetchall()

def orderby(connection, field, order):
    with connection.cursor() as cursor:
        sql = "select * from CardPayments order by " + field + " " + order

        cursor.execute(sql)
        return cursor.fetchall()

def filter(connection, field, filter):
    with connection.cursor() as cursor:
        sql = "select * from CardPayments " \
              "where "+ field +" like '%"+filter+"%'"
        print(sql)
        cursor.execute(sql)
        return cursor.fetchall()

def alterTrust(connection, index):
    with connection.cursor() as cursor:
        sql = "select notSafe from CardPayments where id="+str(index)
        cursor.execute(sql)
        result = ''
        if (cursor.fetchone()['notSafe'] == '0'):
            result = '1'
        else:
            result = '0'
        sql = "update CardPayments set notSafe="+result+" where id="+str(index)
        cursor.execute(sql)
    connection.commit()