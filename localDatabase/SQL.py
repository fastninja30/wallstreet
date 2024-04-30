#################################################################################################
#░██████╗░██████╗░██╗░░░░░░░░░░██████╗░░█████╗░████████╗░█████╗░██████╗░░█████╗░░██████╗███████╗#
#██╔════╝██╔═══██╗██║░░░░░░░░░░██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝#
#╚█████╗░██║██╗██║██║░░░░░░░░░░██║░░██║███████║░░░██║░░░███████║██████╦╝███████║╚█████╗░█████╗░░#
#░╚═══██╗╚██████╔╝██║░░░░░░░░░░██║░░██║██╔══██║░░░██║░░░██╔══██║██╔══██╗██╔══██║░╚═══██╗██╔══╝░░#
#██████╔╝░╚═██╔═╝░███████╗░░░░░██████╔╝██║░░██║░░░██║░░░██║░░██║██████╦╝██║░░██║██████╔╝███████╗#
#╚═════╝░░░░╚═╝░░░╚══════╝░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝#
#################################################################################################
import sqlite3

class SQL:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    ###########################################################
    # Main functions
    def create_table(self, table_name, columns):
        column_defs = ', '.join([f"{col} TEXT" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert(self, table_name, data):
        columns = list(data.keys())
        values = list(data.values())

        if not self.table_exists(table_name):
            self.create_table(table_name, columns)

        placeholders = ', '.join(['?' for _ in values])
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        if not self.is_duplicate(table_name, data):
            self.cursor.execute(insert_query, values)
            self.conn.commit()
        else:
            # print("Duplicate entry. Update table")
            first_column = columns[0]
            first_value = values[0]
            update_data = {col: val for col, val in zip(columns[1:], values[1:])}
            condition = f"{first_column}='{first_value}'"
            self.update(table_name, update_data, condition)

    def update(self, table_name, data, condition):
        set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(update_query, list(data.values()))
        self.conn.commit()

    # Delete from table
    def delete(self, table_name, condition):
        delete_query = f"DELETE FROM {table_name} WHERE {self.quote_condition(condition)}"
        self.cursor.execute(delete_query)
        self.conn.commit()

    # Delete table
    def drop_table(self, table_name):
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(drop_table_query)
        self.conn.commit()

    def search(self, table_name, condition=None, order_by=None, limit=None):
        select_query = f"SELECT * FROM {table_name}"

        if condition:
            select_query += f" WHERE {self.quote_condition(condition)}"

        if order_by:
            select_query += f" ORDER BY {order_by}"

        if limit:
            select_query += f" LIMIT {limit}"

        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]

        results = []
        for row in rows:
            result = {col: val for col, val in zip(column_names, row)}
            results.append(result)

        return results

    #######################################################################
    # Helper fuctions
    def quote_condition(self, condition):
        parts = condition.split('=')
        if len(parts) == 2:
            column, value = parts
            if not self.is_numeric(value.strip()):
                value = f"'{value.strip()}'"
            return f"{column}={value}"
        return condition

    def is_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def print_table(self, table_name, truncate=True, limit=10):
        select_query = f"SELECT * FROM {table_name} LIMIT {limit}"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()

        # Get the column names
        column_names = [description[0] for description in self.cursor.description]

        # Truncate column names if longer than 40 characters
        if truncate:
            column_names = [col[:40] if len(col) > 40 else col for col in column_names]

        print(" | ".join(column_names))
        print("-" * (sum(len(col) for col in column_names) + 3 * (len(column_names) - 1)))

        for row in rows:
            if truncate:
                # Truncate values if longer than 40 characters
                truncated_row = [str(item)[:40] if len(str(item)) > 40 else str(item) for item in row]
            else:
                truncated_row = [str(item) for item in row]
            print(" | ".join(truncated_row))

        if len(rows) == limit:
            print(f"\nShowing first {limit} rows. Use a higher limit to see more rows.")

    def table_exists(self, table_name):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return self.cursor.fetchone() is not None

    def is_duplicate(self, table_name, data):
        first_column = list(data.keys())[0]
        first_value = list(data.values())[0]

        select_query = f"SELECT COUNT(*) FROM {table_name} WHERE {first_column} = ?"

        self.cursor.execute(select_query, (first_value,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def __del__(self):
        self.conn.close()


