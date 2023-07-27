import sqlite3



def authorization(login, password, signal):
    global username_connect
    con = sqlite3.connect("./request/users.db")
    cur = con.cursor()
    username_connect = login
    

    # Проверяем существует ли такой пользователь
    cur.execute(f"SELECT user,password FROM users WHERE user ='{login}';")
    value = cur.fetchall()
      
    if value != [] and value[0][1] == password:
        username = value[0][0]
        username_text = "".join(i for i in username)
        signal.emit(f"Привет, {username_text}")
    
    else:
         signal.emit("Проверьте правильность ввода данных")

    cur.close()
    con.close()
def global_username(self):
    return username_connect


def registration(login, password, username,signal):
    con = sqlite3.connect("./request/users.db")
    cur = con.cursor()

    # Проверяем существует ли такой пользователь
    cur.execute(f'SELECT * FROM users WHERE user == "{login}" ')
    value = cur.fetchall()
    flag = True
    for i in value:
        if i[1] == login:
            flag = False
    if flag == False:
        signal.emit("Пользователь с таким логином уже существует")

    if value == []:
        cur.execute(
            f"INSERT INTO users (user, password, username) VALUES ('{login}', '{password}', '{username}')")
        
        con.commit()
    

    cur.close()
    con.close()

def add_product(name_pr,price_pr,amount_pr,type_pr):
    con = sqlite3.connect("./request/users.db")
    cur = con.cursor()

    #Занесем данные в таблицу
    cur.execute(f'SELECT name,type FROM stock WHERE name = "{name_pr}" AND price = "{price_pr}"')
    result = cur.fetchall()
    new_amount = int(amount_pr)/1000
    if result != []:
        if type_pr =='кг.' or type_pr == 'л.' or type_pr == 'шт.':
            cur.execute(f'UPDATE stock SET amount = amount + "{amount_pr}" WHERE name = "{name_pr}" AND price = "{price_pr}" ')
            con.commit()
        else:
            cur.execute(f'UPDATE stock SET amount = amount + "{new_amount}" WHERE name = "{name_pr}" AND price = "{price_pr}" ')
            con.commit()

    else:
        if type_pr == 'г.':
            cur.execute(f'INSERT INTO stock (username,name, price, amount, type, receipt_date) VALUES ("{username_connect}","{name_pr}", "{price_pr}","{new_amount}", "кг.",DATETIME("now","localtime"))  ')
            con.commit()
        elif type_pr == 'мл.':
            cur.execute(f'INSERT INTO stock (username,name, price, amount, type, receipt_date) VALUES ("{username_connect}","{name_pr}", "{price_pr}","{new_amount}", "л.",DATETIME("now","localtime"))  ')
            con.commit()
        else:
            cur.execute(f'INSERT INTO stock (username,name, price, amount, type, receipt_date) VALUES ("{username_connect}","{name_pr}", "{price_pr}","{amount_pr}", "{type_pr}",DATETIME("now","localtime"))  ')
            con.commit()
    
   
    cur.close()
    con.close()


