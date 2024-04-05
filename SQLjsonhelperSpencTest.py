#################################################################################################
#░██████╗░██████╗░██╗░░░░░░░░░░██████╗░░█████╗░████████╗░█████╗░██████╗░░█████╗░░██████╗███████╗#
#██╔════╝██╔═══██╗██║░░░░░░░░░░██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝#
#╚█████╗░██║██╗██║██║░░░░░░░░░░██║░░██║███████║░░░██║░░░███████║██████╦╝███████║╚█████╗░█████╗░░#
#░╚═══██╗╚██████╔╝██║░░░░░░░░░░██║░░██║██╔══██║░░░██║░░░██╔══██║██╔══██╗██╔══██║░╚═══██╗██╔══╝░░#
#██████╔╝░╚═██╔═╝░███████╗░░░░░██████╔╝██║░░██║░░░██║░░░██║░░██║██████╦╝██║░░██║██████╔╝███████╗#
#╚═════╝░░░░╚═╝░░░╚══════╝░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝#
#################################################################################################
#
#   BY SPENCER SU
#
#   Overview:
#   1. When user starts the code it will
#       i.   Connect to 'postDb.db'. If such file doesn't exit, it will create one.
#       ii.  If no table exists in 'postDb.db' yet, it will create a table called redditPosts
#       iii. Move to jump_start_menu() function
#   2. When the code begins running it will
#       i.   Prompt the user to enter a table to access
#       ii.  If no table exists, it will prompt the user to create one. Else, it will move to table_modifier()
#   3. While the code is running it will
#       i.   Keep running until user types 'q'
#
#   Functions:
#       add_post()
#       delete_post()
#       replace_post()
#       display_table()
#       clear_table()
#       drop_table()
#       table_modifier()
#       create_table()
#       ask_new_table()
#       check_table_exists()
#       jump_start_menu()


import sqlite3

# https://docs.python.org/3/library/sqlite3.html
conn = sqlite3.connect('postDB.db')

cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS redditPosts
                  (postId INTEGER PRIMARY KEY, author TEXT, likes INTEGER)''')
conn.commit()

input_dictionary1 = {
    "postId": 12345,
    "author": "JohnSmith",
    "likes": 123
}

input_dictionary2 = {
    "postId": 12345,
    "author": "Greg",
    "likes": 483
}

input_dictionary3 = {
    "postId": 96429,
    "author": "PopStars123",
    "likes": 4032
}
input_dictionary4 = {
    "postId": 32450,
    "author": "Joe",
    "likes": 120
}

input_dictionary5 = {
    "postId": 62349,
    "author": "Mark",
    "likes": 502
}

input_dictionary6 = {
    "postId": 16423,
    "author": "Jacob",
    "likes": 1130
}


# Given an input dictionary, adds a new entry(post) to Table %table_name%
def add_post(table_name, input_dict):
    # Checks if post already exists in database
    sql_prompt = "SELECT 1 FROM "
    sql_prompt += table_name
    sql_prompt += " WHERE postId = "
    sql_prompt += str(input_dict["postId"])
    cursor.execute(sql_prompt)
    result = cursor.fetchall()
    if result:
        print("ERROR: Post already added/ identical postID")
        return

    # Creates the sql prompt to insert a post
    sql_prompt = "INSERT INTO "
    sql_prompt += table_name
    sql_prompt += "("
    sql_prompt += ", ".join(str(v) for v in input_dict.keys())
    sql_prompt += ") VALUES ("
    for x in range(len(input_dict) - 1):
        sql_prompt += "?, "
    sql_prompt += "?)"

    # Executes prompt
    cursor.execute(sql_prompt, list(input_dict.values()))
    conn.commit()


# Deletes the post associated with the given postId in Table %table_name%
def delete_post(table_name, postId):
    # Checks if post exists in database
    sql_prompt = "SELECT 1 FROM "
    sql_prompt += table_name
    sql_prompt += " WHERE postId = "
    sql_prompt += postId
    cursor.execute(sql_prompt)
    result = cursor.fetchall()
    if not result:
        print("ERROR: No post with ", postId, " exists.")
        return

    # Delete post
    sql_prompt = "DELETE FROM "
    sql_prompt += table_name
    sql_prompt += " WHERE postId = ?"
    cursor.execute(sql_prompt, postId)
    conn.commit()


# Replaces a post with another post which has an identical postID in table %table_name%
def replace_post(table_name, old_input_dict, new_input_dict):
    keys = list(old_input_dict.keys())
    keys.pop(0)

    old_id = list(old_input_dict.values())[0]
    new_list = list(new_input_dict.values())
    new_id = new_list[0]
    new_list.pop(0)
    new_list.append(old_id)

    if old_id != new_id:
        print("ERROR: postIds", old_id, "(old) and", new_id, "(new) don't match. Cannot replace post")
        exit(0)

    # create Sql_prompt
    sql_prompt = "UPDATE "+table_name+" SET "
    sql_prompt += "=?, ".join(str(v) for v in keys)
    sql_prompt += "=? WHERE postId=?"

    # Execute command
    cursor.execute(sql_prompt, new_list)
    conn.commit()


# Displays all the contents in Table %table_name%.
def display_table(table_name):
    sql_prompt = "SELECT COUNT(*) FROM "
    sql_prompt += table_name
    cursor.execute(sql_prompt)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print("Table", table_name, "is currently empty")

    else:
        sql_prompt = "SELECT * FROM "
        sql_prompt += table_name
        cursor.execute(sql_prompt)
        rows = cursor.fetchall()
        for row in rows:
            print(row)


# Clears all the contents in table %table_name%.
def clear_table(table_name):
    cursor.execute("DELETE FROM " + table_name)
    conn.commit()


# Drops(deletes) table %table_name% from the database.
def drop_table(table_name):
    sql_prompt = "DROP TABLE if EXISTS "
    sql_prompt += table_name
    cursor.execute(sql_prompt)
    conn.commit()
    print("Dropped table", table_name)
    main()


# Prompts for commands to modify Table %main_table_name%.
def table_modifier(main_table_name):
    action = "0"
    print("Enter an action:\nn - table name\n a - add_post \n d - delete post\n r - replace post\n v - view table\n "
          "c - clear table\nf - drop table\ns - change tables\nh - help\nq - quit\n "
          "----------------------")
    while action != "q":
        action = input()
        print("Action: '", action, "'")
        if action == "h":
            print("Commands:\nn - table name\n a - add_post \n d - delete post\n r - replace post\n v - view table\n "
                  "c - clear table\nf - drop table\ns - change tables\nh - help\nq - quit")
        if action == "n":
            print("Table Name: ", main_table_name)
        if action == "a":
            add_post(main_table_name, input_dictionary1)
            add_post(main_table_name, input_dictionary2)
            add_post(main_table_name, input_dictionary3)
            add_post(main_table_name, input_dictionary4)
            add_post(main_table_name, input_dictionary5)
            add_post(main_table_name, input_dictionary6)
        if action == "d":
            post_to_delete = input("Type the postID to delete or type \"q\" to cancel.\n")
            if post_to_delete != "q":
                delete_post(main_table_name, post_to_delete)
        if action == "r":
            replace_post(main_table_name, input_dictionary1, input_dictionary2)
        if action == "v":
            display_table(main_table_name)
        if action == "c":
            clear_table(main_table_name)
        if action == "f":
            drop_table(main_table_name)
        if action == "q":
            print("Shutting down...")
            conn.close()
            exit(0)
        if action == "s":
            main()
        print("-----------------------------------")


# Creates a new table called %main_table_name%
def create_table(main_table_name):
    sql_prompt = "CREATE TABLE IF NOT EXISTS "
    sql_prompt += main_table_name
    sql_prompt += " (postId INTEGER PRIMARY KEY, author TEXT, likes INTEGER)"
    cursor.execute(sql_prompt)
    conn.commit()


# Asks to create a new table
def ask_new_table(main_table_name):
    print("The table called \"", main_table_name, "\" does not exist.")
    action = input("Do you want to create a new table? Y\\N\n")
    action = action.lower()

    while action != "n" and action != "y":
        action = input("Invalid answer; Enter Y or N.\n").lower()

    if action == "y":
        create_table(main_table_name)
        table_modifier(main_table_name)
    else:
        main()


# Check if Table %main_table_name% exists.
def check_table_exists(main_table_name):
    sql_prompt = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='"
    sql_prompt += main_table_name + "'"
    cursor.execute(sql_prompt)
    result = cursor.fetchall()
    if result[0][0] == 0:
        return False
    else:
        return True


# The first menu the user sees when code runs
def jump_start_menu():
    main_table_name = "l"

    while main_table_name == "l" or main_table_name == "q":
        main_table_name = input("Which table do you want to access? Enter l to list all tables, enter q to quit\n")
        if main_table_name == "q":
            conn.close()
            exit(0)

        if main_table_name == "l":
            sql_prompt = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor.execute(sql_prompt)
            result = cursor.fetchall()
            print(result)

    return main_table_name


def main():
    # Asks which table to work on
    name = jump_start_menu()

    # Checks if table exists
    if check_table_exists(name):
        table_modifier(name)

    # Asks if you want to make a new table
    else:
        ask_new_table(name)


if __name__ == "__main__":
    main()

conn.close()
