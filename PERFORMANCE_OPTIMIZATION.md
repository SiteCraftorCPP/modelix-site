# Оптимизация производительности сайта

## ✅ Что уже сделано

### 1. CSS Оптимизация
- **Удалены все `backdrop-filter: blur()`** - главная причина лагов на retina дисплеях
- **Упрощены hover-эффекты** - убраны тяжёлые `transform: scale()` и сложные `box-shadow`
- **Отключены анимации градиентов** - убраны постоянные анимации фона
- **Добавлен CSS containment** - изолированы независимые блоки для оптимизации рендеринга
- **Оптимизирован text-rendering** - ускорен рендеринг текста

### 2. HTML Оптимизация
- **Добавлен `loading="lazy"`** для всех изображений (кроме hero)
- **Добавлен `decoding="async"`** для асинхронной декодировки изображений
- **Первое изображение с `loading="eager"`** для быстрого отображения

### 3. JavaScript
- **Удалена плашка-уведомление** и связанные с ней функции

## 🚀 Рекомендации для VPS

### 1. Оптимизация изображений (КРИТИЧНО!)
```bash
# Установить imagemagick или webp tools
sudo apt-get install webp

# Конвертировать все JPG/PNG в WebP с качеством 80%
cd media/services
for file in *.jpg; do cwebp -q 80 "$file" -o "${file%.jpg}.webp"; done
for file in *.png; do cwebp -q 80 "$file" -o "${file%.png}.webp"; done

# Для PNG с большим размером использовать оптимизацию
cd media/hero
optipng -o7 *.png
```

### 2. Nginx конфигурация

Добавьте в `nginx.conf`:

```nginx
# Сжатие статики
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/css text/javascript application/javascript image/svg+xml;

# Кэширование статики
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /media/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# HTTP/2
listen 443 ssl http2;

# Brotli сжатие (если доступно)
brotli on;
brotli_types text/css application/javascript image/svg+xml;
```

### 3. Django settings оптимизация

Добавьте в `settings.py`:

```python
# Включить GZip middleware
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # В начало!
    # ... остальные middleware
]

# Оптимизация запросов к БД
CONN_MAX_AGE = 600  # Переиспользование соединений с БД

# Кэширование (если установлен Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 4. Установить Redis для кэширования

```bash
sudo apt-get install redis-server
pip install django-redis
```

### 5. Оптимизация Gunicorn

В `gunicorn.conf.py` или командной строке:

```bash
gunicorn modelix_site.wsgi:application \
    --workers 4 \
    --worker-class gevent \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 5
```

## 📊 Ожидаемые результаты

- **FPS**: с 3 до 60 FPS
- **Загрузка страницы**: -40-60%
- **Размер CSS**: -30% (убрали тяжёлые эффекты)
- **Размер изображений**: -60-80% (после WebP конвертации)

## 🔧 Дополнительные оптимизации

### 1. CDN для статики (опционально)
Использовать Cloudflare или другой CDN для раздачи статики.

### 2. Preload критичных ресурсов

Добавьте в `<head>`:

```html
<link rel="preload" href="/static/css/performance-fix.css" as="style">
<link rel="preconnect" href="https://fonts.googleapis.com">
```

### 3. Минификация CSS/JS

```bash
pip install django-compressor

# В settings.py
INSTALLED_APPS += ['compressor']
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
```

### 4. Мониторинг производительности

Используйте инструменты:
- **Chrome DevTools** → Performance
- **Lighthouse** (встроен в Chrome)
- **WebPageTest.org**

## 🎯 Следующие шаги

1. ✅ Протестировать сайт локально
2. Конвертировать изображения в WebP
3. Настроить Nginx кэширование
4. Настроить Redis
5. Протестировать на VPS с MacBook

## 📝 Команды для деплоя на VPS

```bash
# 1. Обновить код
git pull

# 2. Собрать статику
python manage.py collectstatic --noinput

# 3. Перезапустить Gunicorn
sudo systemctl restart gunicorn

# 4. Перезапустить Nginx
sudo systemctl restart nginx

# 5. Проверить логи
sudo journalctl -u gunicorn -f
```

## ⚠️ Важно

Основная причина лагов была **`backdrop-filter: blur()`** - эффект размытия фона, который на retina дисплеях MacBook вызывает огромную нагрузку на GPU. Теперь он полностью отключен.

Все hover-эффекты максимально упрощены - только изменение `opacity`, без `scale`, `transform` и сложных теней.

