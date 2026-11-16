from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Учебные данные для авторизации
users = {
    "admin": "12345",
    "student": "qwerty"
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask: авторизация</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111827;
            color: #f3f4f6;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .form {
            background: #1f2937;
            padding: 30px;
            width: 340px;
            border: 1px solid #374151;
            border-radius: 12px;
            box-sizing: border-box;
        }
        h2 { margin-top: 0; text-align: center; }
        label { display: block; margin: 14px 0 6px; }
        input {
            width: 100%;
            box-sizing: border-box;
            padding: 11px;
            border: 1px solid #4b5563;
            border-radius: 6px;
            background: #111827;
            color: white;
        }
        button {
            width: 100%;
            margin-top: 18px;
            padding: 11px;
            border: 0;
            border-radius: 6px;
            background: #4f46e5;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #4338ca; }
        .error {
            padding: 10px;
            color: #fecaca;
            background: #7f1d1d;
            border-radius: 6px;
        }
        .success {
            padding: 10px;
            color: #bbf7d0;
            background: #14532d;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <div class="form">
        <h2>Авторизация</h2>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if success %}
            <p class="success">{{ success }}</p>
        {% endif %}

        <form method="POST" action="{{ url_for('login') }}">
            <label for="username">Имя пользователя</label>
            <input id="username" type="text" name="username"
                   placeholder="Введите логин" required>

            <label for="password">Пароль</label>
            <input id="password" type="password" name="password"
                   placeholder="Введите пароль" required>

            <button type="submit">Войти</button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    success = None

    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not username or not password:
                error = "Заполните все поля!"
            elif username in users and users[username] == password:
                success = "Авторизация прошла успешно!"
            else:
                error = "Неверное имя пользователя или пароль!"

        except Exception:
            error = "Произошла ошибка при авторизации."

    return render_template_string(HTML_PAGE, error=error, success=success)


if __name__ == "__main__":
    app.run(debug=True)
