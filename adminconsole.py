import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kiragg0101",
            database="AutoDealerDB"
        )
        print("Підключення до бази даних успішне!")
        return connection
    except mysql.connector.Error as err:
        print(f"Помилка підключення: {err}")
        return None


def show_tables():
    print("Доступні таблиці:")
    print("1. Vehicles")
    print("2. Customers")
    print("3. Sales")
    print("4. Services")
    print("5. Suppliers")
    print("6. Users")


def view_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        print(f"Записи таблиці {table_name}:")
        print(f"{' | '.join(columns)}")
        for row in rows:
            print(" | ".join(map(str, row)))
    except mysql.connector.Error as err:
        print(f"Помилка під час отримання даних: {err}")


def add_record(connection, table_name):
    try:
        cursor = connection.cursor()
        if table_name == "Vehicles":
            brand = input("Марка: ")
            model = input("Модель: ")
            year = int(input("Рік: "))
            color = input("Колір: ")
            condition = input("Стан (new/used): ")
            price = float(input("Ціна: "))
            vin = input("VIN: ")
            sql = "INSERT INTO Vehicles (brand, model, year, color, condition, price, VIN) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (brand, model, year, color, condition, price, vin)
        elif table_name == "Customers":
            first_name = input("Ім'я: ")
            last_name = input("Прізвище: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            address = input("Адреса: ")
            sql = "INSERT INTO Customers (first_name, last_name, phone, email, address) VALUES (%s, %s, %s, %s, %s)"
            values = (first_name, last_name, phone, email, address)
        elif table_name == "Sales":
            vehicle_id = int(input("ID автомобіля: "))
            customer_id = int(input("ID клієнта: "))
            sale_date = input("Дата продажу (YYYY-MM-DD): ")
            amount = float(input("Сума: "))
            sql = "INSERT INTO Sales (vehicle_id, customer_id, sale_date, amount) VALUES (%s, %s, %s, %s)"
            values = (vehicle_id, customer_id, sale_date, amount)
        elif table_name == "Services":
            vehicle_id = int(input("ID автомобіля: "))
            service_date = input("Дата обслуговування (YYYY-MM-DD): ")
            service_type = input("Тип обслуговування: ")
            parts_used = input("Використані деталі: ")
            cost = float(input("Вартість: "))
            sql = "INSERT INTO Services (vehicle_id, service_date, service_type, parts_used, cost) VALUES (%s, %s, %s, %s, %s)"
            values = (vehicle_id, service_date, service_type, parts_used, cost)
        elif table_name == "Suppliers":
            name = input("Назва постачальника: ")
            contact_info = input("Контактна інформація: ")
            address = input("Адреса: ")
            sql = "INSERT INTO Suppliers (name, contact_info, address) VALUES (%s, %s, %s)"
            values = (name, contact_info, address)
        elif table_name == "Users":
            username = input("Ім'я користувача: ")
            password_hash = input("Хеш пароля: ")
            role = input("Роль (manager/service_specialist/admin): ")
            sql = "INSERT INTO Users (username, password_hash, role) VALUES (%s, %s, %s)"
            values = (username, password_hash, role)
        else:
            print("Таблиця не підтримується для додавання записів.")
            return

        cursor.execute(sql, values)
        connection.commit()
        print("Запис успішно додано!")
    except mysql.connector.Error as err:
        print(f"Помилка під час додавання запису: {err}")


def delete_record(connection, table_name):
    try:
        cursor = connection.cursor()
        record_id = input(f"Введіть ID запису для видалення з таблиці {table_name}: ")
        primary_key = table_name.lower()[:-1] + "_id"  # Генеруємо ім'я первинного ключа (наприклад, vehicle_id)
        sql = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
        cursor.execute(sql, (record_id,))
        connection.commit()
        print("Запис успішно видалено!")
    except mysql.connector.Error as err:
        print(f"Помилка під час видалення запису: {err}")


def main():
    connection = connect_to_database()
    if not connection:
        return

    while True:
        print("\nМеню:")
        print("1. Переглянути таблицю")
        print("2. Додати запис")
        print("3. Видалити запис")
        print("4. Вийти")
        choice = input("Виберіть дію (1-4): ")

        if choice == "1":
            show_tables()
            table_choice = input("Введіть назву таблиці: ")
            view_table(connection, table_choice)
        elif choice == "2":
            show_tables()
            table_choice = input("Введіть назву таблиці: ")
            add_record(connection, table_choice)
        elif choice == "3":
            show_tables()
            table_choice = input("Введіть назву таблиці: ")
            delete_record(connection, table_choice)
        elif choice == "4":
            print("Вихід із програми...")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

    connection.close()


if __name__ == "__main__":
    main()

