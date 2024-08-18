import pyodbc

# Настройки подключения
server = 'WIN-5HQEEVML4E9\\CSISSERVER'
database = 'lhk-cs-migration'
username = 'test'
password = 'test'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(connection_string)
    print("Соединение успешно установлено.")
except pyodbc.Error as e:
    print("Ошибка при подключении к базе данных:", e)
    conn = None

if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dbo.patients")
        rows = cursor.fetchall()

        for row in rows:
            print(row)
    except pyodbc.Error as e:
        print("Ошибка при выполнении SELECT запроса:", e)