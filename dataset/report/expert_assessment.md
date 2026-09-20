# Экспертная оценка безопасности проекта vulnerable-flask-demo

## Область анализа
Проанализирован исходный код Flask-приложения с помощью SAST-сканера Semgrep.
Код принадлежит авторам проекта, сканирование легально.

## Критические находки

### 1. SQL-инъекция (app.py:17, 20)
**Механизм:** Пользовательский ввод конкатенируется в SQL-запрос через f-string.
**Эксплуатация:** `username=' OR '1'='1' --` → обход аутентификации.
**Риск:** Полный доступ к БД, утечка данных.
**Рекомендация:** Параметризованные запросы: `cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))`.

### 2. Command Injection (app.py:34)
**Механизм:** `os.popen(f"ping -c 1 {host}")`, host из GET-параметра.
**Эксплуатация:** `?host=127.0.0.1; cat /etc/passwd`.
**Риск:** RCE, компрометация сервера.
**Рекомендация:** `subprocess.run(["ping", "-c", "1", host], shell=False)` + валидация.

### 3. Небезопасная десериализация (app.py:27)
**Механизм:** `pickle.loads(request.get_data())`.
**Эксплуатация:** Отправка вредоносного pickle-payload → RCE.
**Риск:** Полный контроль над сервером.
**Рекомендация:** Заменить на `json.loads`.

## Средние находки

### 4. Hardcoded secrets (app.py:9-10)
SECRET_KEY и DB_PASSWORD в открытом виде.
**Рекомендация:** Переменные окружения (.env + .gitignore) или secrets manager.

### 5. Debug=True (app.py:39)
Раскрытие stack trace, интерактивный Werkzeug debugger.
**Рекомендация:** `debug=False` в production.

## Низкие находки

### 6. Top-level app.run() (app.py:34)
**Рекомендация:** Обернуть в `if __name__ == "__main__":`.

## Общие рекомендации
1. Внедрить SAST в CI/CD (Semgrep через GitHub Actions).
2. Добавить Dependabot.
3. Code review с акцентом на OWASP Top 10.
4. Pre-commit hooks с Semgrep.

## Правовое соответствие
- Сканирование только собственного кода.
- GitHub Bug Bounty Rules не нарушены.
- УК РФ ст. 272 не нарушена.
