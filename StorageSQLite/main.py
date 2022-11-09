import sqlite3
from enum import Enum

class Operation(Enum):
    INSERT = 1
    DELETE = 2
    UPDATE = 3

class SQLiteConnection():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name CHAR NOT NULL, 
            seller CHAR NOT NULL, 
            price REAL)
        """)

    def insertOp(self, newProd):
        if len(newProd) == 3 and newProd[2].isdigit():
            self.cursor.execute("INSERT INTO products (name, seller, price) VALUES (?, ?, ?)", newProd)
            self.connection.commit()
        else:
            print("Wrong input, unable to insert\n")

    def listOp(self):
        self.cursor.execute("SELECT * FROM products")
        print("\n{:<8} {:<15} {:<15} {:<10}".format("ID", "NAME", "SELLER", "PRICE"))
        for row in self.cursor:
            print("{:<8} {:<15} {:<15} {:<10}".format(row[0], row[1], row[2], row[3]))
        print("\n")

    def delOp(self, id):
        if id.isnumeric(): 
            self.cursor.execute("DELETE FROM products WHERE id = ?", id)
            self.connection.commit()
        else:
            print("Input is not numeric, unable to select\n")

    def updateOp(self, newProdAndId):
        if len(newProdAndId) == 4 and newProdAndId[2].isdigit() and newProdAndId[3].isdigit():
            try:
                self.cursor.execute("UPDATE products SET name = ?, seller = ?, price = ? WHERE id = ?", newProdAndId)
                self.connection.commit()
            except:
                print("Wrong id, unable to update\n")
        else:
            print("Wrong input, unable to update\n")   

def readInput(operationType):
    match operationType:
        case operationType.INSERT:
            tupleInput = input("Enter product details: \n")
            tupleInput = tuple(val for val in tupleInput.split())
            return tupleInput
        case operationType.DELETE:
            return input("Insert product ID: \n")
        case operationType.UPDATE:
            id = input("Insert product ID: \n")
            tupleInput = input("Enter product details: \n")
            tupleInput = tuple(val for val in tupleInput.split())
            tupleInput = tupleInput + (id,)
            return tupleInput

def main():
    databaseCon = SQLiteConnection()

    print("""
    .:Storage Database System v1.0:.

        Available operations:
            INSERT
            UPDATE
            DELETE
            LIST
            EXIT
        Or just the first letter.
    """)

    while True:
        usr_input = input("Select operation: \n")
        usr_input = usr_input.upper()

        match usr_input:
            case "INSERT" | "I":
                usr_input = readInput(Operation.INSERT)
                databaseCon.insertOp(usr_input)
            case "LIST" | "L":
                databaseCon.listOp()
            case "UPDATE" | "U":
                usr_input = readInput(Operation.UPDATE)
                databaseCon.updateOp(usr_input)
            case "DELETE" | "D":
                usr_input = readInput(Operation.DELETE)
                databaseCon.delOp(usr_input)
            case "EXIT" | "E":
                databaseCon.connection.close()
                break
            case other:
                print("Not an operation.\n")

if __name__ == "__main__":
    main()