import mysql.connector
import time

conn = mysql.connector.connect(host="localhost", port="3306", user="pyshop", password="pyshop", database="pyshop")
cursor = conn.cursor()
time_local = time.localtime()



                                                # ВОЗВРАЩЕНИЕ В МЕНЮ

def goNext():
    print("\n=========================")
    print("Вернуться в меню?")
    goNext = int(input("1 - да // 2 - выйти: "))
    print("========================")
    if goNext == 1:
        print("")
    else:
        quit()






                                                #  ДОБАВЛЕНИЕ КЛИЕНТА

def addClient():
    print("")
    print("////////////////////////")
    print("Добавление пользователя:")
    print("////////////////////////")
    print("")
    print("Введите имя: ")
    firstName = input()
    
    print("Введите фамилию: ")
    lastName = input()
    
    print("Введите мобилу: ")
    phone = input()

    print("Введите бабки: ")
    money = float(input())
    
    try:
        cursor.execute('CREATE TABLE tClient(clientID int AUTO_INCREMENT primary key, firstName varchar(25) not null, lastName varchar(25) not null, phone varchar(8) not null, money float not null)')
        conn.commit()
    except:
        print("")
    try:
        cursor.execute("INSERT INTO tClient VALUES (null, %s, %s, %s, %s)", (firstName, lastName, phone, money))
        conn.commit()
        print("Пользователь", firstName, lastName, "добавлен в базу")
        print("=======================================")
    except:
        print("Авария! Нет электричества! Ждём!")
        print("==================================")






                                            #  ДОБАВЛЕНИЕ ПРОДУКТА

def addProduct():
    print("")
    print("////////////////////")
    print("Добавление продукта:")
    print("////////////////////")
    print("")
    print("Введите название продукта: ")
    productName = input()
    
    print("Введите вес товара в граммах: ")
    productWeight = float(input())

    print("Введите цену: ")
    productPrice = float(input())
    try:
        cursor.execute('CREATE TABLE tProduct(productID int AUTO_INCREMENT primary key, productName varchar(25) not null, productWeight float not null, productPrice float not null)')
        conn.commit()
    except:
        print("")
    try:
        cursor.execute("INSERT INTO tProduct VALUES (null, %s, %s, %s)", (productName, productWeight, productPrice))
        conn.commit()
        print(productName, "добавлен в магазин")
        print("=======================================")
    except:
        print("Авария! Нет электричества! Ждём!")






                                                #  СПИСОК КЛИЕНТОВ

def listClients():
    print("")
    print("=====================")
    print("Список пользователей: ")
    print("=====================")
    print("")
    record = cursor.execute('SELECT * FROM tClient limit 1')
    if not record:
        print("Пользователи отсутсвуют!")
    else:
        try:
            cursor.execute('SELECT * FROM tClient')
            record = cursor.fetchall()
            print("==================================================================================")
            for row in record:
                print("Пользователь номер -", row[0])
                print("Имя: ", row[1], "//", "Фамилия: ", row[2], "//", "Телефон: ", row[3], "//", "Кошелек: ", row[4], "$")
                print("==================================================================================")
        except:
            print("В наличии нет ни одного клиента!")






                                            #   СПИСОК ПРОДУКТОВ

def listProducts():
    print("")
    print("=================")
    print("Список продуктов: ")
    print("=================")
    print("")

    record = cursor.execute('SELECT *  FROM tProduct limit 1')
    if not record:
        print("Товары отсутсвуют!")
    else:
        try:
            cursor.execute('SELECT * FROM tProduct')
            record = cursor.fetchall()
            print("==================================================================================")
            for row in record:
                print("Продукт номер -", row[0])
                print("Название: ", row[1], "//" , "Вес: ", row[2], "г", "//", "Цена: ", row[3], "$")
                print("==================================================================================")
        except:
            print("В наличии нет ни одного продукта!")






                                                    #  ПОКУПКА

def Buy():
    print("")
    print("//////////////////")
    print("Покупка продуктов:")
    print("//////////////////")
    listProducts()

    '''НАХОЖДЕНИЕ ПРОДУКТА ПО ЕГО ID И СРАВНИВАНИЕ С ВЫБОРОМ ПРОГРАММЫ'''
    chooseProduct = int(input("Выберите продукт по его номеру: "))
    cursor.execute('SELECT productID FROM tProduct')
    record = cursor.fetchall()
    for row in record:
        if chooseProduct == row[0]:
            print("")
            break
    if chooseProduct != row[0]:
        print("\n====================")
        print("Нет такого продукта!")
        print("====================")
        return
    
    print("===================")
    listClients()   
    
    '''НАХОЖДЕНИЕ КЛИЕНТА ПО ЕГО ID И СРАВНИВАНИЕ С ВЫБОРОМ ПРОГРАММЫ'''
    chooseClient = int(input("Выберите клиента по его номеру: "))
    cursor.execute('SELECT clientID FROM tClient')
    record = cursor.fetchall()
    for row in record:
        if chooseClient == row[0]:
            print("")
            break
    if chooseClient != row[0]:
        print("\n===================")
        print("Нет такого клиента!")
        print("===================")
        return

    '''НАХОЖДЕНИЕ ДЕНЕГ КЛИЕНТА ПО ЕГО ID '''

    listChooseClient = [chooseClient]
    try:
        cursor.execute('SELECT money FROM tClient WHERE clientID = %s', (listChooseClient))
        record = cursor.fetchall()
    except:
        print("Ошибка!")
        return
    for row in record:
        clientMoney = row[0]


    '''НАХОЖДЕНИЕ ДЕНЕГ ПРОДУКТА ПО ЕГО ID '''
    
    listChooseProduct = [chooseProduct]
    try:
        cursor.execute('SELECT productPrice FROM tProduct WHERE productID = %s', (listChooseProduct))
        record = cursor.fetchall()
    except:
        print("Ошибка!")
        return
    for row in record:
        productPrice = row[0]

    cursor.execute('SELECT * FROM tProduct WHERE productID = %s', (listChooseProduct))
    record = cursor.fetchall()
    for row in record:
        print("==================================================================================")
        print("Название: ", row[1], "//" , "Вес: ", row[2], "г", "//", "Цена: ", row[3], "$")
        print("==================================================================================\n")
    print("Купить этот продукт?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        try:
            cursor.execute('CREATE TABLE tHistory(ID int AUTO_INCREMENT primary key, buy varchar(30), product_id bigint(20) not null, client_id bigint(20) not null)')
            conn.commit()
        except:
            print("")
        if clientMoney >= productPrice:
            purchaseMoney = clientMoney - productPrice
            buyTime = time.strftime("%Y-%d-%m %H:%M:%S", time_local)
            print(buyTime)
            cursor.execute('UPDATE tClient SET money = %s WHERE tClient.clientID = %s', (purchaseMoney, chooseClient))
            conn.commit()
            cursor.execute('INSERT INTO tHistory (ID, buy, product_id, client_id) VALUES(null, %s, %s, %s)', (buyTime, chooseProduct, chooseClient))
            conn.commit()
            print("")
            print("==========================")
            print("Покупка совершена успешно!")
            print("--------------------------")
            print("Текущий остаток: ", purchaseMoney, "$")
        else:
            print("")
            print("======================")
            print("Недостаточно средств!")
            print("======================")
            return
    else:
        print("Авария! Нет электричества! Ждём!")
        return






                                            # ИЗМЕНЕНИЕ ПРОДУКТА

def editProduct():
    print("")
    print("///////////////////")
    print("Изменение продукта:")
    print("///////////////////")
    listProducts()
    print("Выберите продукт по его номеру, который хотите изменить: ")
    chooseEditProduct = int(input())
    try:
        cursor.execute('SELECT productID from tProduct')
        record = cursor.fetchall()
    except:
        print("Нет такого продукта!")
        return
    for row in record:
        if chooseEditProduct == row[0]:
            print("")
            break
    if chooseEditProduct != row[0]:
        print("\nНет такого продукта!")
        print("\n==========================================")
        print("Хотите ли вы добавить новый продукт?")
        print("==========================================")
        booleanAns = int(input("1 - да // 2 - нет"))
        if booleanAns == 1:
            addProduct()
        else:
            return
    listChooseEditProduct = [chooseEditProduct]
    cursor.execute('SELECT * FROM tProduct WHERE productID = %s', (listChooseEditProduct))
    record = cursor.fetchall()
    for row in record:
        print("==================================================================================")
        print("Название: ", row[1], "//" , "Вес: ", row[2], "г", "//", "Цена: ", row[3], "$")
        print("==================================================================================\n")
    print("Изменить этот продукт?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        print("Изменить название товара: ")
        editProductName = input()
        
        print("Изменить вес товара в граммах: ")
        editProductWeight = float(input())

        print("Изменить цену товара: ")
        editProductPrice = float(input())

        try:
            cursor.execute("UPDATE tProduct SET productName = %s, productWeight = %s, productPrice = %s WHERE tProduct.productID = %s", (editProductName, editProductWeight, editProductPrice, chooseEditProduct))
            conn.commit()
        except:
            print("Изменение не удалось!")
            return
        print("\n=====================================================")
        print("Измененный продукт:", editProductName, "//", editProductWeight, "//", editProductPrice)







                                            # ИЗМЕНЕНИЕ КЛИЕНТА

def editClient():
    print("")
    print("///////////////////////")
    print("Изменение пользователя:")
    print("///////////////////////")
    listClients()
    print("Выберите пользователя по его номеру, которого хотите изменить: ")
    chooseEditClient = int(input())
    cursor.execute('SELECT clientID from tClient')
    record = cursor.fetchall()
    for row in record:
        if chooseEditClient == row[0]:
            print("")
            break
    if chooseEditClient != row[0]:
        print("\nНет такого пользователя!")
        print("\n==========================================")
        print("Хотите ли вы добавить нового пользователя?")
        print("==========================================")
        booleanAns = int(input("1 - да // 2 - нет: "))
        if booleanAns == 1:
            addClient()
        else:
            return
    listChooseEditClient = [chooseEditClient]
    try:
        cursor.execute('SELECT * FROM tClient WHERE clientID = %s', (listChooseEditClient))
        record = cursor.fetchall()
    except:
        print("Нет такого пользователя!")
        return
    for row in record:
        print("=====================================================================================")
        print("Имя: ", row[1], "//", "Фамилия: ", row[2], "//", "Телефон: ", row[3], "//", "Кошелек: ", row[4], "$")
        print("=====================================================================================\n")
    print("Изменить этого пользователя?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        print("Введите новое имя: ")
        editFirstName = input()
       
        print("Введите новую фамилию: ")
        editLastName = input()
        
        print("Введите новую мобилу: ")
        editPhone = input()

        print("Изменить бабки: ")
        editMoney = float(input())

        try:
            cursor.execute("UPDATE tClient SET firstName = %s, lastName = %s, phone = %s, money = %s WHERE tClient.clientID = %s", (editFirstName, editLastName, editPhone, editMoney, chooseEditClient))
            conn.commit()
        except:
            print("")
            print("Изменение не удалось!")
            return
        print("\n===========================================================================")
        print("Измененный пользователь:", editFirstName, "//", editLastName, "//", editPhone, "//", editMoney, "$")





                                        #    ДОБАВЛЕНИЕ ДЕНЕГ ПОЛЬЗОВАТЕЛЮ

def addMoney():
    print("")
    print("//////////////////////////////")
    print("Добавление денег пользователю:")
    print("//////////////////////////////")
    listClients()
    print("Выберите пользователя по его номеру, которому хотите добавить денег: ")
    chooseClientToAddMoney = int(input())
    cursor.execute('SELECT clientID from tClient')
    record = cursor.fetchall()
    for row in record:
        if chooseClientToAddMoney == row[0]:
            print("")
            break
    if chooseClientToAddMoney != row[0]:
        print("\nНет такого пользователя!")
        print("\n==========================================")
        print("Хотите ли вы добавить нового пользователя?")
        print("==========================================")
        booleanAns = int(input("1 - да // 2 - нет"))
        if booleanAns == 1:
            addClient()
        else:
            return
    listChooseClientToAddMoney = [chooseClientToAddMoney]
    try:
        cursor.execute('SELECT * FROM tClient WHERE clientID = %s', (listChooseClientToAddMoney))
        record = cursor.fetchall()
    except:
        print("Нет такого пользователя!")
        return
    for row in record:
        print("=====================================================================================")
        print("Имя: ", row[1], "//", "Фамилия: ", row[2], "//", "Кошелек: ", row[4], "$")
        print("=====================================================================================\n")
    print("Добавить денег этому пользователю?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        print("")
        addMoney = 0
        while addMoney == 0:
            addMoney = float(input("Введите сумму больше нуля: "))
            if addMoney > 0:              
                cursor.execute('SELECT money from tClient WHERE tClient.clientID = %s', (listChooseClientToAddMoney))
                record = cursor.fetchall()
                for row in record:
                    checkMoney = row[0]
                finalSum = checkMoney + addMoney
                try:
                    cursor.execute('UPDATE tClient SET money = %s WHERE tClient.clientID = %s', (finalSum, chooseClientToAddMoney))
                    conn.commit()
                except:
                    print("")
                    print("======================")
                    print("Добавление не удалось!")
                    print("======================")
                    return
                print("")
                print("====================================")
                print("Новый баланс пользователя: ", finalSum)
                print("====================================")





                                                # УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ

def removeClient():
    print("\n//////////////////////")
    print("Удаление пользователя:")
    print("//////////////////////")
    listClients()
    print("Выберите пользователя по его номеру, которого хотите удалить: ")
    chooseClient = int(input())
    cursor.execute('SELECT clientID from tClient')
    record = cursor.fetchall()
    for row in record:
        if chooseClient == row[0]:
            print("")
            break
    if chooseClient != row[0]:
        print("Нет такого пользователя!")
        print("========================")
        return
    listChooseClient = [chooseClient]
    try:
        cursor.execute('SELECT * FROM tClient WHERE clientID = %s', (listChooseClient))
        record = cursor.fetchall()
    except:
        return
    for row in record:
        print("=====================================================================================")
        print("Имя: ", row[1], "//", "Фамилия: ", row[2], "//", "Телефон: ", row[3], "//", "Кошелек: ", row[4], "$")
        print("=====================================================================================\n")
    print("Удалить этого пользователя?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        cursor.execute('SELECT firstName, lastName FROM tClient WHERE clientID = %s', (listChooseClient))
        record = cursor.fetchall()
        for row in record:
            firstName = row[0]
            lastName = row[1]
        try:
            cursor.execute('DELETE FROM tClient WHERE clientID = %s', (listChooseClient))
            conn.commit()
            print("\n=============================================")
            print("Удален пользователь", firstName, lastName)
            print("=============================================")
        except:
            print("Авария! Нет электричества! Ждём!")
    else:
        return





                                            #  УДАЛЕНИЕ ПРОДУКТА

def removeProduct():
    print("\n==================")
    print("Удаление продукта:")
    print("==================")
    listProducts()
    print("Выберите продукт по его номеру, который хотите удалить")
    chooseProduct = int(input())
    cursor.execute('SELECT productID FROM tProduct')
    record = cursor.fetchall()
    for row in record:
        if chooseProduct == row[0]:
            print("")
            break
    if chooseProduct != row[0]:
        print("Нет такого продукта!")
        return
    listChooseProduct = [chooseProduct]
    cursor.execute('SELECT * FROM tProduct WHERE productID = %s', (listChooseProduct))
    record = cursor.fetchall()
    for row in record:
        print("==================================================================================")
        print("Название: ", row[1], "//" , "Вес: ", row[2], "г", "//", "Цена: ", row[3], "$")
        print("==================================================================================\n")
    print("Удалить этот продукт?")
    booleanAnswer = int(input("1 - да // 2 - нет: "))
    if booleanAnswer == 1:
        cursor.execute("SELECT productName FROM tProduct WHERE productID = %s", (listChooseProduct))
        record = cursor.fetchall()
        for row in record:
            productName = row[0]
        try:
            cursor.execute('DELETE FROM tProduct WHERE productID = %s', (listChooseProduct))
            conn.commit()
        except:
            print("Авария! Нет электричества! Ждём!")
        print("\n==========================================")
        print(productName, "успешно удален(а)!")
        print("==========================================")
    else:
        return