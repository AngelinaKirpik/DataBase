import psycopg2
from settings import postgres_password
conn = psycopg2.connect(database = 'additional_task_1', user='postgres', password=postgres_password);


def creation_db(conn):
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS phones CASCADE")
        cur.execute("DROP TABLE IF EXISTS orders CASCADE")
        cur.execute("DROP TABLE IF EXISTS clients CASCADE")

        cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL);         
        """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                phone_id SERIAL PRIMARY KEY,
                phone VARCHAR(20) CHECK (phone ~ '^[\+\d][\d\-\s\(\)]{8,20}$'),
                client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE);      
        """)
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS orders(
                        order_id SERIAL PRIMARY KEY,
                        order_name VARCHAR(20) NOT NULL,
                        order_date DATE NOT NULL,
                        total_amount NUMERIC(10, 2) NOT NULL,
                        client_id INTEGER NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE);      
        """)
        conn.commit()

def add_client(conn, client_first_name, client_last_name, client_email):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO clients(first_name, last_name, email)
                VALUES (%s, %s, %s)
                RETURNING client_id;          
        """, (client_first_name, client_last_name, client_email))
        client_id = cur.fetchone()[0]
        conn.commit()
        print(f'Клиент добавлен с ID {client_id}')
        return client_id

def add_phone(conn, client_id, client_phone):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO phones(phone, client_id)
                VALUES (%s, %s)
                RETURNING client_id;          
        """, (client_phone, client_id))
        conn.commit()
        print(f'Клиенту с ID {client_id} добавлен номер телефона {client_phone}')

def update_info(conn, client_id, client_first_name=None, client_last_name=None, client_email=None):
    with conn.cursor() as cur:
        set_parts = []
        values = []
        if client_first_name is not None:
            set_parts.append('first_name = %s')
            values.append(client_first_name)
        if client_last_name is not None:
            set_parts.append('last_name = %s')
            values.append(client_last_name)
        if client_email is not None:
            set_parts.append('email = %s')
            values.append(client_email)
        if not set_parts:
            print('Вы не внесли новых изменений')
        else:
            set_clause = ', '.join(set_parts)
            values.append(client_id)
        cur.execute(f"""
                UPDATE clients SET {set_clause} 
                WHERE client_id = %s;""", values)
        conn.commit()
        print(f'Данные клиента с ID {client_id} обновлены на {values}')
      
def delete_phone(conn, client_id, phone_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM phones 
                WHERE client_id = %s AND phone_id = %s
                RETURNING client_id, phone_id;     
        """, (client_id, phone_id))
        deleted = cur.fetchone()
        if deleted:
            print(f'У клиента с ID {client_id} телефон с ID {phone_id} удалён ')
        else:
            print(f'У клиента с ID {client_id} телефон с ID {phone_id} не найден')

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                DELETE FROM clients 
                WHERE client_id = %s 
                RETURNING client_id;     
        """, (client_id, ))
        delet = cur.fetchone()
        if delet:
            print(f'Клиент с ID {client_id} удалён ')
        else:
            print(f'Клиент с ID {client_id} не найден')

def find_clients(conn, client_first_name=None, client_last_name=None, client_email=None, client_phone=None):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT DISTINCT c.client_id, c.first_name, c.last_name, c.email, string_agg(p.phone, ', ') AS phones
                FROM clients c
                LEFT JOIN phones p ON c.client_id = p.client_id
                WHERE (c.first_name  ILIKE %s OR %s IS NULL) OR
                      (c.last_name  ILIKE %s OR %s IS NULL) OR
                      (c.email  ILIKE %s OR %s IS NULL) OR
                      (p.phone  ILIKE %s OR %s IS NULL)
                GROUP BY c.client_id, c.first_name, c.last_name, c.email""",
                    (f'%{client_first_name}%' if client_first_name else None, client_first_name,
                     f'%{client_last_name}%' if client_last_name else None, client_last_name,
                     f'%{client_email}%' if client_email else None, client_email,
                     f'%{client_phone}%' if client_phone else None, client_phone))
        result = cur.fetchall()
        if not result:
            print('Клиент не найден')
            return []
        for row in result:
            print(f'ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Email: {row[3]}, Телефон(ы): {row[4] or "нет"} ')
        return result

def add_order(conn, client_id, order_name, order_date, order_total_amount):
    with conn.cursor() as cur:
        cur.execute("""
                INSERT INTO orders(order_name, order_date, total_amount, client_id)
                VALUES (%s, %s, %s, %s)
                RETURNING order_id;          
               """, (order_name, order_date, order_total_amount, client_id))
        order_id = cur.fetchone()[0]
        conn.commit()
        print(f'Заказ "{order_name}" с ID {order_id} добавлен клиенту с ID {client_id}')
        return order_id

def get_client_orders(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                SELECT order_id, order_name, order_date, total_amount FROM orders
                WHERE client_id = %s
                """, (client_id, ))
        orders = cur.fetchall()

        if not orders:
            print(f'У клиента {client_id} нет заказов')
            return []
        for order in orders:
            print(f'Заказ №{order[0]}:  {order[1]} оформленный {order[2]} на сумму {order[3]}')
        return orders


# Проверка работоспособности
print("===========Тест==========")
# Создание базы данных
creation_db(conn)
with conn.cursor() as cur:
    cur.execute("TRUNCATE TABLE phones, orders, clients RESTART IDENTITY CASCADE")
    conn.commit()
#Добавление клиентов
print("==========Добавление клиентов==========")
client1 = add_client(conn, "Иван", "Иванов", "ivan@mail.ru")
client2 = add_client(conn, "Мария", "Петрова", "maria@mail.ru")
client3 = add_client(conn, "Петр", "Сидоров", "petr@mail.ru")
client4 = add_client(conn, "Кристина", "Иванова", "kris@mail.ru")
client5 = add_client(conn, "Мария", "Иванова", "mari@mail.ru")
client6 = add_client(conn, "Павел", "Сидоров", "pavel@mail.ru")
print("=" * 50)
# Добавление телефонов
print("==========Добавление телефонов==========")
add_phone(conn, client1, "+7-999-123-45-67")
add_phone(conn, client2, "+7-999-890-09-87")
add_phone(conn, client3, "+7-999-654-32-11")
add_phone(conn, client4, "+7-999-123-66-67")
add_phone(conn, client5, "+7-999-555-55-55")
add_phone(conn, client6, "+7-999-111-11-11")
add_phone(conn, client1, "+7-999-222-22-22")
add_phone(conn, client3, "+7-999-333-33-33")
add_phone(conn, client3, "+7-999-444-44-44")
add_phone(conn, client5, "+7-999-666-66-66")
add_phone(conn, client5, "+7-999-777-77-77")
add_phone(conn, client5, "+7-999-888-88-88")
print("=" * 50)
# Обновление данных клиента
print("==========Обновление данных клиента==========")
update_info(conn, client5, client_last_name="Сидорова")
print("=" * 50)
# Поиск клиента
print("==========Поиск клиента 'Мария'==========")
find_clients(conn, client_first_name='Мария')
print("==========Поиск клиента по номеру телефона +7-999-222-22-22==========")
find_clients(conn, client_phone='+7-999-222-22-22')
print("==========Поиск клиента по почте==========")
find_clients(conn, client_email='pavel@mail.ru')
print("=" * 50)
# Добавление заказов
print("==========Добавление заказов==========")
add_order(conn, client1, 'Ноутбук', '2024-01-15', 50000.00)
add_order(conn, client1, 'Мышь', '2024-01-15', 1500.00)
add_order(conn, client3, 'Клавиатура', '2024-01-15', 3000.00)
print("=" * 50)
# Заказы клиентов
print("==========Заказы клиента client1==========")
get_client_orders(conn, client1)
print("==========Заказы клиента client3==========")
get_client_orders(conn, client3)
print("==========Заказы не существующего клиента==========")
get_client_orders(conn, 999)
# Удаление телефонов
print("==========Удаление телефонов==========")
with conn.cursor() as cur:
    cur.execute("SELECT phone_id FROM phones WHERE client_id = %s LIMIT 1", (client5, ))
    phone_id = cur.fetchone()[0]
    delete_phone(conn, client5, phone_id)
print("=" * 50)
# Удаление клиента
print("==========Удаление клиента==========")
delete_client(conn, client2)
print("=" * 50)
# Финальный поиск клиентов
print("==========Финальный поиск клиентов==========")
find_clients(conn, client_first_name='')
conn.close()