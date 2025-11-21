# Команды для загрузки обновлений на VPS

## 1. Подключение к VPS по SSH

```bash
ssh username@your-vps-ip
# или
ssh username@your-domain.com
```

## 2. Переход в директорию проекта

```bash
cd /path/to/your/project
# Например:
cd /var/www/modelix-site
# или
cd ~/modelix-site
```

## 3. Получение обновлений с GitHub

```bash
# Проверка текущего статуса
git status

# Получение последних изменений
git pull origin main

# Если нужно принудительно обновить (осторожно!)
# git fetch origin
# git reset --hard origin/main
```

## 4. Если нужно перезапустить сервер (для Django)

```bash
# Если используете systemd
sudo systemctl restart gunicorn
# или
sudo systemctl restart your-service-name

# Если используете supervisor
sudo supervisorctl restart modelix

# Если используете PM2 (Node.js)
pm2 restart all
```

## 5. Сбор статических файлов (для Django)

```bash
python manage.py collectstatic --noinput
```

## 6. Применение миграций (если есть изменения в БД)

```bash
python manage.py migrate
```

## Полный скрипт одной командой (если проект в /var/www/modelix-site):

```bash
cd /var/www/modelix-site && git pull origin main && python manage.py collectstatic --noinput && python manage.py migrate && sudo systemctl restart gunicorn
```

## Альтернатива: Создание deploy скрипта на сервере

Создайте файл `deploy.sh` на сервере:

```bash
#!/bin/bash
cd /var/www/modelix-site
git pull origin main
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart gunicorn
echo "Deployment completed!"
```

Сделайте его исполняемым:
```bash
chmod +x deploy.sh
```

Затем запускайте просто:
```bash
./deploy.sh
```





