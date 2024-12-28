import sqlite3


# Функция для создания базы данных и таблицы с тестовыми данными
def create_sample_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы grades, если её нет
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,  -- Предмет
        grade INTEGER NOT NULL,  -- Оценка
        student_id INTEGER NOT NULL  -- Идентификатор студента
    );
    """)

    # Добавление нескольких оценок
    cursor.executemany("""
    INSERT INTO grades (subject, grade, student_id) 
    VALUES (?, ?, ?)
    """, [
        ('Math', 5, 1),
        ('Math', 3, 2),
        ('Math', 4, 3),
        ('Physics', 5, 1),
        ('Physics', 4, 2),
        ('Chemistry', 5, 1),
        ('Chemistry', 2, 2)
    ])

    conn.commit()
    conn.close()


# Функция для создания представления statistic_view
def create_grate_statistics_view(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создаём представление statistic_view
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS statistic_view AS
    SELECT 
        subject,
        AVG(grade) AS average_grade,
        MAX(grade) AS max_grade,
        MIN(grade) AS min_grade
    FROM 
        grades
    GROUP BY 
        subject;
    """)

    conn.commit()
    conn.close()
    print("Представление 'statistic_view' успешно создано!")


# Функция для получения статистики из представления statistic_view
def get_statistic(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Запрос данных из представления statistic_view
    cursor.execute("SELECT * FROM statistic_view")
    statistics = cursor.fetchall()

    conn.close()

    return statistics


# Имя базы данных
db_name = 'school.db'

# Создаём тестовую базу данных и таблицу с тестовыми данными
create_sample_db(db_name)

# Создаём представление statistic_view
create_grate_statistics_view(db_name)

# Получаем статистику по предметам
statistics = get_statistic(db_name)

# Выводим результаты
print("Статистика по предметам:")
for stat in statistics:
    print(f"Предмет: {stat[0]}, Средняя оценка: {stat[1]:.2f}, Макс. оценка: {stat[2]}, Мин. оценка: {stat[3]}")
