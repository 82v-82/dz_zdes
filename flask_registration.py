from flask import Flask, request, render_template_string, redirect, url_for, session
import pymysql
from pymysql.err import IntegrityError

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Настройки MySQL — при необходимости измени их под свой компьютер.
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "users"


def connect_db(with_database=True):
    """Подключение к MySQL."""
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


def init_db():
    """Создаёт базу данных и таблицу, если их ещё нет."""
    connection = connect_db(with_database=False)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(100) UNIQUE NOT NULL,
                    user_password VARCHAR(255) NOT NULL
                )
            """)
        connection.commit()
    finally:
        connection.close()


def create_user(name, password):
    """Добавляет нового пользователя и возвращает его ID."""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (user_name, user_password) VALUES (%s, %s)",
                (name, password)
            )
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()


def check_user(name, password):
    """Проверяет логин и пароль в базе данных."""
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, user_name FROM users "
                "WHERE user_name = %s AND user_password = %s",
                (name, password)
            )
            return cursor.fetchone()
    finally:
        connection.close()


REGISTER_HTML = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Регистрация</title>
</head>
<body>
    <h2>Регистрация пользователя</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Имя пользователя"
               value="{{ username }}" required>
        <br><br>
        <input type="password" name="password" placeholder="Пароль" required>
        <br><br>
        <button type="submit">Зарегистрироваться</button>
    </form>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    <a href="{{ url_for('login') }}">Уже есть аккаунт? Войти</a>
</body>
</html>
"""

LOGIN_HTML = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Вход</title>
</head>
<body>
    <h2>Вход</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Имя пользователя" required>
        <br><br>
        <input type="password" name="password" placeholder="Пароль" required>
        <br><br>
        <button type="submit">Войти</button>
    </form>
    {% if error %}<p style="color:red">{{ error }}</p>{% endif %}
    <a href="{{ url_for('register') }}">Регистрация</a>
</body>
</html>
"""

PROFILE_HTML = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Профиль</title>
</head>
<body>
    <h1>Добро пожаловать, {{ username }}!</h1>
    <a href="{{ url_for('logout') }}">Выйти</a>
</body>
</html>
"""


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("profile"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not name or not password:
            return render_template_string(
                REGISTER_HTML, error="Заполните все поля", username=name
            )

        try:
            create_user(name, password)
            session["username"] = name
            return redirect(url_for("profile"))
        except IntegrityError:
            return render_template_string(
                REGISTER_HTML,
                error="Пользователь с таким именем уже существует",
                username=name
            )
        except pymysql.MySQLError as error:
            return render_template_string(
                REGISTER_HTML,
                error=f"Ошибка MySQL: {error}",
                username=name
            )

    return render_template_string(REGISTER_HTML, error=None, username="")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            user = check_user(name, password)
        except pymysql.MySQLError as error:
            return render_template_string(
                LOGIN_HTML, error=f"Ошибка MySQL: {error}"
            )

        if user:
            session["username"] = user["user_name"]
            return redirect(url_for("profile"))

        return render_template_string(
            LOGIN_HTML, error="Неверное имя пользователя или пароль"
        )

    return render_template_string(LOGIN_HTML, error=None)


@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template_string(
        PROFILE_HTML, username=session["username"]
    )


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    try:
        init_db()
        print("База данных и таблица users готовы.")
        print("Открой в браузере: http://127.0.0.1:5000/register")
        app.run(debug=True)
    except pymysql.MySQLError as error:
        print("Не удалось подключиться к MySQL:", error)
        print("Проверь, что MySQL запущен и настройки DB_HOST, DB_USER, DB_PASSWORD верны.")
