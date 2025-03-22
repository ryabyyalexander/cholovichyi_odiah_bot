import sqlite3


class BotDatabase:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(query, params)
            db.commit()
            return cursor

    def drop_table_if_exists(self, table_name):
        self.execute_query(f"DROP TABLE IF EXISTS {table_name}")

    def create_products(self, product_id=0):
        # self.drop_table_if_exists("products")

        self.execute_query(f'''
                CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT default 0,
                '30' INTEGER default 0,
                '31' INTEGER default 0,
                '32' INTEGER default 0,
                '33' INTEGER default 0,
                '34' INTEGER default 0,
                '35' INTEGER default 0,
                '36' INTEGER default 0,
                '38' INTEGER default 0,
                '40' INTEGER default 0,
                '42' INTEGER default 0,
                '46' INTEGER default 0,
                '48' INTEGER default 0,
                '50' INTEGER default 0,
                '52' INTEGER default 0,
                '54' INTEGER default 0,
                '56' INTEGER default 0,
                '58' INTEGER default 0,
                '60' INTEGER default 0,
                price REAL default 0,
                cena REAL default 0,
                sale INTEGER default 0,
                category TEXT default 0,
                brand TEXT default 0,
                article TEXT default 0,
                model TEXT default 0,
                sw INTEGER default 0,
                seasons TEXT default 0
                    )
                ''')
        self.execute_query(f'INSERT INTO products (product_id) VALUES ({product_id})')

    def get_last_product_id(self):
        cursor = self.execute_query('select product_id from products')
        return cursor.fetchall()[-1][0]

    def get_publish(self, product_id):
        cursor = self.execute_query(f'select publish from products where product_id={product_id}')
        return cursor.fetchall()

    def get_param_product(self, product_id, param):
        cursor = self.execute_query(f'select {param} from products where product_id={product_id}')
        result = cursor.fetchall()
        if result:  # проверка, что результат не пуст
            pole = result[0][0]  # извлечение строки из кортежа
            return pole
        return None  # на случай, если продукт с таким ID не найден

    def get_sizes_product(self, product_id):
        cursor = self.execute_query(
            f'SELECT "32", "33", "34", "35", "36", "38", "40", "42", '
            f'"46", "48", "50", "52", "54", "56", "58", "60"  FROM products WHERE product_id={product_id}')
        result = cursor.fetchall()
        if result:  # проверка, что результат не пуст
            return result[0]
        return None  # на случай, если продукт с таким ID не найден

    def get_category_product(self, category):
        cursor = self.execute_query("SELECT * FROM products WHERE category=?", (category,))
        result = cursor.fetchall()
        return result

    def photo_is_product(self, photo_id):
        cursor = self.execute_query("select product_id from products where product_id=?", (photo_id,))
        result = cursor.fetchall()
        if result:  # проверка, что результат не пуст
            return True
        return False

    def get_total_products(self):
        query = '''
        SELECT category, 
               name, 
               ("30" + "31" + "32" + "33" + "34" + "35" + "36" + 
                "38" + "40" + "42" + "46" + "48" + "50" + "52" + 
                "54" + "56" + "58" + "60") AS total_quantity,
               price,
               price * ("30" + "31" + "32" + "33" + "34" + "35" + "36" + 
                        "38" + "40" + "42" + "46" + "48" + "50" + "52" + 
                        "54" + "56" + "58" + "60") AS total_cost
        FROM products

        UNION ALL

        SELECT 'ИТОГО' AS category, 
               NULL AS name, 
               SUM("30" + "31" + "32" + "33" + "34" + "35" + "36" + 
                   "38" + "40" + "42" + "46" + "48" + "50" + "52" + 
                   "54" + "56" + "58" + "60") AS total_quantity, 
               NULL AS price,
               SUM(price * ("30" + "31" + "32" + "33" + "34" + "35" + "36" + 
                            "38" + "40" + "42" + "46" + "48" + "50" + "52" + 
                            "54" + "56" + "58" + "60")) AS total_cost
        FROM products;
        '''
        cursor = self.execute_query(query)
        return cursor.fetchall()

data_product = BotDatabase('ClothForYou.db')
# data_product.create_products()
