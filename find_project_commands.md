# Команды для поиска проекта на VPS

## 1. Поиск проекта по имени
```bash
find / -name "modelix*" -type d 2>/dev/null
```

## 2. Поиск manage.py (Django проект)
```bash
find / -name "manage.py" 2>/dev/null
```

## 3. Проверка типичных мест размещения
```bash
# Проверка /var/www/
ls -la /var/www/

# Проверка домашней директории
ls -la ~/

# Проверка /opt/
ls -la /opt/

# Проверка /home/
ls -la /home/
```

## 4. Если проект в текущей директории
```bash
pwd
ls -la
```

## 5. Поиск по git репозиторию
```bash
find / -name ".git" -type d 2>/dev/null | grep -v ".git/"
```





