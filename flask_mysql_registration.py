from flask import Flask, request, render_template_string, session, redirect, url_for
import pymysql
from pymysql.err import IntegrityError, MySQLError
from werkzeug.security import generate_password_hash

# ================= НАСТРОЙКИ =================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""       # Укажи пароль MySQL, если он установлен
DB_NAME = "users_db"

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # Замени на свою секретную строку


# ================= ПОДКЛЮЧЕНИЕ К MYSQL =================
def get_connection(with_database=True):
    settings = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
    if with_database:
        settings["database"] = DB_NAME
    return pymysql.connect(**settings)


def init_database():
    # Создаём базу, если её ещё нет
    connection = get_connection(with_database=False)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()

    # Создаём таблицу пользователей
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(100) NOT NULL UNIQUE,
                    user_password VARCHAR(255) NOT NULL
                )
            """)
        connection.commit()
    finally:
        connection.close()


# ================= HTML-СТРАНИЦЫ =================
REGISTER_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Регистрация</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 420px;
               margin: 60px auto; padding: 20px; }
        input, button { box-sizing: border-box; width: 100%;
                        padding: 10px; margin: 8px 0; }
        button { cursor: pointer; }
        .error { color: #c62828; }
    </style>
</head>
<body>
    <h1>Регистрация пользователя</h1>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST" action="{{ url_for('register') }}">
        <label>Имя пользователя:</label>
        <input type="text" name="username" required maxlength="100">
        <label>Пароль:</label>
        <input type="password" name="password" required>
        <button type="submit">Зарегистрироваться</button>
    </form>
</body>
</html>
"""

PROFILE_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Профиль</title>
</head>
<body>
    <h1>Регистрация прошла успешно!</h1>
    <h2>Добро пожаловать, {{ username }}!</h2>
    <a href="{{ url_for('logout') }}">Выйти</a>
</body>
</html>
"""


# ================= МАРШРУТЫ FLASK =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template_string(REGISTER_PAGE, error=None)

    name = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not name or not password:
        return render_template_string(
            REGISTER_PAGE, error="Заполните все поля!"
        )

    # Сохраняем не исходный пароль, а его безопасный хеш
    password_hash = generate_password_hash(password)

    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                (name, password_hash)
            )
            connection.commit()

        session["username"] = name
        return redirect(url_for("profile"))

    except IntegrityError:
        return render_template_string(
            REGISTER_PAGE,
            error="Пользователь с таким именем уже существует!"
        ), 409

    except MySQLError as error:
        app.logger.exception("Ошибка MySQL: %s", error)
        return render_template_string(
            REGISTER_PAGE,
            error="Не удалось выполнить операцию с базой данных."
        ), 500

    finally:
        if connection:
            connection.close()


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("register"))
    return render_template_string(
        PROFILE_PAGE, username=session["username"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register"))


# ================= ЗАПУСК =================
if __name__ == "__main__":
    try:
        init_database()
        print("База данных и таблица users готовы.")
        print("Открой в браузере: http://127.0.0.1:5000/register")
        app.run(debug=True)
    except MySQLError as error:
        print("Не удалось подключиться к MySQL:", error)
        print("Проверь DB_HOST, DB_USER и DB_PASSWORD в начале файла.")
