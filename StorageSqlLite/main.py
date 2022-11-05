import sqlite3

def inputOp(cursor, connection):
    inputVal = input("Enter product details: \n")

    product = tuple(val for val in inputVal.split())

    if  len(product) == 3 and product[2].isdigit():
        cursor.execute("INSERT INTO products (name, seller, price) VALUES (?, ?, ?)", product)
        connection.commit()
    else:
        print("Wrong input, unable to insert\n")

def listOp(cursor):
    cursor.execute("SELECT * FROM products")
    print("\n{:<8} {:<15} {:<15} {:<10}".format("ID", "NAME", "SELLER", "PRICE"))
    for row in cursor:
        print("{:<8} {:<15} {:<15} {:<10}".format(row[0], row[1], row[2], row[3]))
    print("\n")

def delOp(cursor, connection):
    inputVal = input("Enter product ID: \n")

    if inputVal.isnumeric(): 
        cursor.execute("DELETE FROM products WHERE id = ?", inputVal)
        connection.commit()
    else:
        print("Input is not numeric, unable to select\n")

def main():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

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
            LIST
            DELETE
            EXIT
            
    """)

    while True:
        usr_input = input("Select operation: \n")
        usr_input = usr_input.upper()

        match usr_input:
            case "INSERT":
                inputOp(cursor, connection)
            case "LIST":
                listOp(cursor)
            case "DELETE":
                delOp(cursor, connection)
            case "EXIT":
                connection.close()
                break
            case other:
                print("Not an operation.\n")

if __name__ == "__main__":
    main()