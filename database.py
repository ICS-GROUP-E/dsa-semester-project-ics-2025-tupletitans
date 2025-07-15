import sqlite3

class TaskDatabase:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_task(self, description):
        query = "INSERT INTO tasks (description) VALUES (?)"
        self.conn.execute(query, (description,))
        self.conn.commit()

    def get_all_tasks(self):
        query = "SELECT id, description FROM tasks"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def delete_task(self, description):
        query = "DELETE FROM tasks WHERE description = ?"
        self.conn.execute(query, (description,))
        self.conn.commit()
