import mysql.connector
from functions import addClient, addProduct, listClients, listProducts, Buy, editProduct, editClient, goNext, addMoney, removeClient, removeProduct


conn = mysql.connector.connect(host="localhost", port="3306", user="pyshop", password="pyshop", database="pyshop")
cursor = conn.cursor()


operation = 0

while operation == 0:
    print("Выберите операцию: ")
    print("0 - Выйти из программы")
    print("1 - Добавить покупателя")
    print("2 - Список покупателей")
    print("3 - Добавить продукт")
    print("4 - Список продуктов")
    print("5 - Купить продукт")
    print("6 - Изменить продукт")
    print("7 - Имзенить покупателя")
    print("8 - Добавить денег покупателю")
    print("9 - Удалить пользователя")
    print("10 - Удалить продукт")
    choose = int(input())
    
    if choose == 0:
        print("До свидания!")
        conn.close()
        break

    elif choose == 1:
        addClient()
        goNext()

    elif choose == 2:
        listClients()
        goNext()
          
    elif choose == 3:      
        addProduct()
        goNext()
    
    elif choose == 4:
        listProducts()
        goNext()

    elif choose == 5:
        Buy()
        goNext()

    elif choose == 6:
        editProduct()
        goNext()

    elif choose == 7:
        editClient()
        goNext()

    elif choose == 8:
        addMoney()
        goNext()

    elif choose == 9:
        removeClient()
        goNext()

    elif choose == 10:
        removeProduct()
        goNext()