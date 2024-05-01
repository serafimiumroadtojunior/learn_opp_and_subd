import psycopg2

class Connect:
    def __init__(self, host, user_name, password, db_name):
        self.host = host
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.conn = None
        self.create_connect()


    def create_connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            user=self.user_name,
            password=self.password,
            dbname=self.db_name
        )


    def create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users_info (
                    id serial PRIMARY KEY,
                    name varchar(50) NOT NULL,
                    surname varchar(50) NOT NULL,
                    age int NOT NULL,
                    phone_number int NOT NULL,
                    address varchar(50) NOT NULL,
                    bio varchar(100)
                );"""
            )
            self.conn.commit()


    def add_info(self, name, surname, age, phone_number, address, bio):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO users_info (name, surname, age, phone_number, address, bio)
                   VALUES (%s, %s, %s, %s, %s, %s);""",
                (name, surname, age, phone_number, address, bio)
            )
            self.conn.commit()


    def delete_info(self, id):
        if id is not None:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM users_info WHERE id = %s;""",
                    (id,)
                )
                self.conn.commit()


    def update_info(self, id, user_el, new):
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users_info SET {user_el} = %s WHERE id = %s;""",
                (new, id)
            )
            self.conn.commit()


    def select_info(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM users_info;"""
            )
            rows = cursor.fetchall()
            for row in rows:
                print(row)  
        self.conn.commit()


    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            print("Соединение с базой данных закрыто")
        else:
            print("Соединение с базой данных не установлено")


if __name__ == "__main__":
    host = input("Введите хост: ")
    user_name = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    db_name = input("Введите имя базы данных: ")

    connector = Connect(host, user_name, password, db_name)
    connector.create_connect()
    connector.create_table()
    connector.add_info(input("Введите имя: "), input("Введите фамилию: "), input("Введите возраст: "),
                       input("Введите номер телефона: "), input("Введите адрес: "), input("Введите биографию: "))
    connector.select_info()
    connector.delete_info(input("Введите ID для удаления: "))
    connector.update_info(input("Введите ID для обновления: "), input("Введите элемент для обновления: "),
                          input("Введите новое значение: "))
    connector.select_info()
    connector.close_connection()