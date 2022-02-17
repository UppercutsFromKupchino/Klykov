from flask import Flask


# Создаю app - экземпляр класса Flask
app = Flask(__name__)
app.secret_key = 'farinov'

# Импорт модуля декорации маршрутов
from app import routes
