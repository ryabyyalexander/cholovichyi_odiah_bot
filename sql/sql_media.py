import sqlite3
from data import name_bot


class BotDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=None):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(query, params or ())
            return cursor

    def sql_add_photo(self, data):
        self.execute_query("""
        CREATE TABLE IF NOT EXISTS photo(
        product_id INT,
        type_photo BOOL DEFAULT TRUE,
        path TEXT,
        caption TEXT
        )""")
        self.execute_query("INSERT INTO photo (product_id, type_photo, path, caption) VALUES (?, ?, ?, ?)", data)

    def table_exists(self, table_name):
        cursor = self.execute_query(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return cursor.fetchone() is not None

    def sql_get_photo_prod_id(self, prod_id):
        if not self.table_exists("photo"):
            return []
        cursor = self.execute_query("SELECT * FROM photo WHERE product_id = ?", (prod_id,))
        return cursor.fetchall()

    def sql_get_all_photo(self):
        if not self.table_exists("photo"):
            return []
        cursor = self.execute_query("SELECT * FROM photo WHERE type_photo = 'photo'")
        return cursor.fetchall()

    def sql_get_main_prod_photo(self, product_id=None):
        if not product_id:
            if not self.table_exists("photo"):
                return []
            cursor = self.execute_query("SELECT * FROM photo WHERE caption='весна-літо 2025'")
        else:
            cursor = self.execute_query("SELECT * FROM photo WHERE product_id=?", (product_id,))

        list_photo = cursor.fetchall()
        seen = set()
        return [photo for photo in list_photo if photo[0] not in seen and not seen.add(photo[0])]

    def sql_get_new_photo(self):
        if not self.table_exists("photo"):
            return []
        cursor = self.execute_query("SELECT * FROM photo WHERE caption='весна-літо 2025'")
        list_photo = cursor.fetchall()
        seen = set()
        return [photo for photo in list_photo if photo[0] not in seen and not seen.add(photo[0])]

    def sql_add_favorite(self, data, user_id):
        self.execute_query(f"""CREATE TABLE IF NOT EXISTS favorites_{user_id}(
            product_id INT,
            type_photo BOOL DEFAULT TRUE,
            path TEXT,
            caption TEXT
        )""")
        self.execute_query(f"INSERT INTO favorites_{user_id} (product_id, type_photo, path, caption) VALUES (?, ?, ?, ?)", data)

    def sql_delete_favorite(self, photo_id, user_id):
        self.execute_query(f"DELETE FROM favorites_{user_id} WHERE path = ?", (photo_id,))

    def sql_get_favorites(self, user_id):
        table_name = f"favorites_{user_id}"
        if not self.table_exists(table_name):
            return []
        cursor = self.execute_query(f"SELECT * FROM {table_name}")
        return cursor.fetchall()

    def sql_add_video(self, data):
        self.execute_query("""CREATE TABLE IF NOT EXISTS video(
            id_video VARCHAR PRIMARY KEY,
            caption TEXT
        )""")
        self.execute_query("INSERT INTO video (id_video, caption) VALUES (?, ?)", data)

    def sql_get_video(self, rowid, table_name):
        if not self.table_exists(table_name):
            return []
        cursor = self.execute_query(f"SELECT * FROM {table_name} WHERE rowid = ?", (rowid,))
        return cursor.fetchall()

    def sql_add_sticker(self, data):
        self.execute_query("""CREATE TABLE IF NOT EXISTS sticker(
            id_sticker VARCHAR PRIMARY KEY
        )""")
        self.execute_query("INSERT INTO sticker (id_sticker) VALUES (?)", (data,))

    def sql_get_sticker(self):
        cursor = self.execute_query("SELECT id_sticker FROM sticker")
        return [i[0] for i in cursor.fetchall()]


data_media = BotDatabase(f'{name_bot}.db')
