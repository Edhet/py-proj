import sqlite3

global connection 
global cursor

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def inputOp():
    inputVal = input("Enter product details: \n")

    newProduct = tuple(val for val in inputVal.split())

    if len(newProduct) == 3 and newProduct[2].isdigit():
        cursor.execute("INSERT INTO products (name, seller, price) VALUES (?, ?, ?)", newProduct)
        connection.commit()
    else:
        print("Wrong input, unable to insert\n")

def listOp():
    cursor.execute("SELECT * FROM products")
    print("\n{:<8} {:<15} {:<15} {:<10}".format("ID", "NAME", "SELLER", "PRICE"))
    for row in cursor:
        print("{:<8} {:<15} {:<15} {:<10}".format(row[0], row[1], row[2], row[3]))
    print("\n")

def delOp():
    inputVal = input("Enter product ID: \n")

    if inputVal.isnumeric(): 
        cursor.execute("DELETE FROM products WHERE id = ?", inputVal)
        connection.commit()
    else:
        print("Input is not numeric, unable to select\n")

def updateOp():
    inputId = input("Enter product ID: \n")
    inputProd = input("Enter product details: \n")

    newProduct = tuple(val for val in inputProd.split())
    newProduct = newProduct + (inputId,)

    if len(newProduct) == 4 and newProduct[2].isdigit() and newProduct[3].isdigit():
        try:
            cursor.execute("UPDATE products SET name = ?, seller = ?, price = ? WHERE id = ?)", newProduct)
            connection.commit()
        except:
            print("Wrong id, unable to update\n")
    else:
        print("Wrong input, unable to update\n")    

def main():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name CHAR NOT NULL, 
            seller CHAR NOT NULL, 
            price REAL)
    """)

    print("""
    .:Storage Database System v1.0:.

        Available operations:
            INSERT
            UPDATE
            DELETE
            LIST
            EXIT
            
    """)

    while True:
        usr_input = input("Select operation: \n")
        usr_input = usr_input.upper()

        match usr_input:
            case "INSERT":
                inputOp()
            case "LIST":
                listOp()
            case "UPDATE":
                updateOp()
            case "DELETE":
                delOp()
            case "EXIT":
                connection.close()
                break
            case other:
                print("Not an operation.\n")

if __name__ == "__main__":
    main()