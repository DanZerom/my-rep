import sqlite3
from datetime import date
import random

""" Welcome to the password, and not only, manager [CRUD].
    The idea is straight forward. 
    Create sqlite3 database file and then expand it/modify/delete the content.
    Currently the only lacking features are:
    -- Dynamic table mapping. I want it to look symmetrical and aesthetic.
    -- To delete specific rows; 
    -- Define database file location [fhand] which has to be done manually;
"""


def db_connection():
    fhand = r"C:\Users\test\PycharmProjects\pythonProject1\test.db"
    print("Opening file " + fhand)
    global connection
    connection = sqlite3.connect(fhand)
    global cursor
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = cursor.fetchall()
    for table in table_list:
        print("Availiable Tables in database file: ", table)
    print()
    if len(table_list) < 1:
        print("No tables availiable!")
        create_table(input("What is a name of the table you want to create? "))
        main()
    global table_name
    table_name = input("Enter a table name you want to work with or type CREATE/DELETE to create/delete another one: ")
    if len(table_name) < 1:
        print("No input, try again: ")
        db_connection()
    elif table_name == "CREATE":
        create_table(input("What is the name of the table you want to create? "))
    elif table_name == "DELETE":
        delete_table(input("What is the name of the table you want to delete? "))
    print()
    table_info = cursor.execute("PRAGMA table_info" + "(" + "[" + table_name + "]" + ")")
    print("TABLE: " + "[" + table_name + "]", "has following column/s:")
    index = 0
    global column_list
    column_list = list()
    for info in cursor.fetchall():
        index = index + 1
        column_list.append(info[1])
        info = print("[" + str(index) + "]", info[1])
    print()
    if not table_name in str(table_list):
        print("Such table doesn't exist")
        print("[EXITING...]")
        exit()
    main()

def rng():
    rng = random.randint(0, 1000000)
    rng_result = str(rng)
    return rng_result

def delete_table(name):
    print("[DELETING TABLE...]  ",">>> " + name + " <<<")
    rng_result = rng()
    print("The confirmation number is:", rng_result)
    usr_input = input("To confirm table removal type in the confirmation number: ")
    if usr_input == rng_result:
        cursor.execute("DROP TABLE " + "[" + name + "]")
        connection.commit()
        print("Success, the table has been removed!")
        db_connection()
    else:
        print("Wrong number, try again!")
        delete_table(name)

def view_data():
    #Convert user input into a proper SQL syntax.
    output_string = ""
    for n in range(len(column_list)):
        output_string = output_string + " " + "[" + column_list[n] + "]" + ","
    len_output_string = len(output_string) - 1
    output_string = output_string[0:len_output_string]
    #Merge user input and SQL SELECT command.
    output = cursor.execute("SELECT rowid," + output_string + " FROM " + "[" + table_name + "]")
    #Print the content and return to main menu.
    index = 0
    for element in output:
        col_index = 0
        index = index + 1
        view_string = ""
        for shit in element[1:]:
            view_string = view_string + "[" + column_list[col_index] + "]: " + shit + "          "
            col_index = col_index + 1
        print("[" + str(index) + "]",view_string)
    print()
    print("-------------------------------------------------")
    main()
def create_table(name):
    print("[Creating table...] ")
    try:
        x = list()
        while True:
            column_name = input("Insert a column of your choice: ")
            column_name = "[" + column_name + "]"
            if len(column_name) < 1:
                print("ERROR: Empty column")
                exit()
            column_name = column_name + r" VARCHAR(255),"
            x.append(column_name)
            answer = input("Do you want to add another column? y/n ")
            if len(answer) < 1:
                print("Empty answer!")
                exit()
            elif answer == "y" or answer == "Y":
                continue
            elif answer == "n" or answer == "N":
                break
            else:
                exit("Wrong answer, don't try me!")
        x_len = len(x)
        output_string = ""
        for n in range(x_len):
            output_string = output_string + x[n]
        len_output_string = len(output_string) - 1
        output_string = output_string[0:len_output_string]
        print("Columns: ", output_string, "have been created")
        columns = "(" + output_string + ",last_modified VARCHAR(255)" + ")"
        table = "CREATE TABLE IF NOT EXISTS " + "[" + name + "]" + columns
        cursor.execute(table)
        connection.commit()
    except:
        print("Error, invalid syntax")
        print("[EXITING...]")
        exit()
    print("The table has been created")
    db_connection()


def insert_data():
    current_date = date.today()
    current_date = "," + '"' + str(current_date) + '"'
    print("[Creating a new entry...]")
    index = 0
    try:
        index = 0
        output_string = ""
        for n in column_list[0:len(column_list) - 1]:
            print("[" + str(n) + "]")
            element = input("Enter a new value here: ")
            output_string = output_string + '"' + element + '"' + ","
            index = index + 1
        len_output_string = len(output_string) - 1
        output_string = output_string[0:len_output_string]
        data = "INSERT INTO " + "[" + table_name + "]" + " VALUES " + "(" + output_string + current_date + ")"
        cursor.execute(data)
        connection.commit()
    except:
        print(r"Wrong data, you need to insert data in such manner: " + '["var1","var2"] etc.')
    view_data()
    answer = input("Do you want to continue? y/n ")
    if answer == "y" or answer == "Y":
        insert_data()
    else:
        main()

def modify_data():
    print("[Modifying...] ")
    current_date = date.today()
    global temp_table
    temp_table = "[" + table_name + "]"
    index = input("Type index to update: ")
    temp_index = index
    modify = "UPDATE " + temp_table + " SET " + "[" +input("Select the column to update: ") + "]" + " = " + ' "' + input("Type the new value: ") +'" ' + "WHERE rowid=" + index
    modify_2 = "UPDATE " + temp_table + " SET last_modified" + " = " + ' "' + str(current_date) +'" ' + "WHERE rowid=" + temp_index
    cursor.execute(modify)
    cursor.execute(modify_2)
    connection.commit()
    output_string = ""
    for n in range(len(column_list)):
        output_string = output_string + " " + "[" + column_list[n] + "]" + ","
    len_output_string = len(output_string) - 1
    output_string = output_string[0:len_output_string]
    output = cursor.execute("SELECT rowid," + output_string + " FROM " + "[" + table_name + "]")
    view_data()
    print()
    print("-------------------------------------------------")

def main():
    print("[MAIN MENU]")
    print("What you wanna do? ")
    print("[1]: Create a new table")
    print("[2]: Insert data into the table")
    print("[3]: Modify Data")
    print("[4]: View Data")
    print("[5]: Custom SQL command")
    print("[6]: Delete table")
    print("[7]: EXIT")
    user_input = str(input("Select your option: "))
    print("-------------------------------------------------")
    print()
    if user_input == "1":
        create_table(input("What is the name of the table you want to create? "))
    elif user_input == "2":
        insert_data()
    elif user_input == "3":
        modify_data()
    elif user_input == "4":
        view_data()
    elif user_input == "5":
            custom =input("SQLite> ")
            cursor.execute(custom)
            cursor.fetchall()
            print("Custom command:", custom)
    elif user_input == "6":
        delete_table(table_name)
    elif user_input == "7":
        print("See ya laters!")
        connection.commit()
        connection.close()
        exit()
    else:
        print("Wrong input, EXITING...")
        exit()
print("WELCOME TO THE GLORIOUS PASSWORD MANAGER™")
db_connection()
main()










