# Исправление получения файлов для Telegram бота

## Проблема
Бот отправлял только один файл из заявки, хотя пользователь прикреплял несколько.

## Решение

### 1. В админке Django
Теперь все файлы отображаются через inline `OrderFileInline`. В каждой заявке видно:
- Количество файлов в списке заявок
- Все файлы с превью в детальном просмотре заявки

### 2. Для Telegram бота

**ВАЖНО:** Бот должен получать файлы из модели `OrderFile`, а не из поля `file` модели `PrintOrder`!

#### Старый способ (НЕПРАВИЛЬНО):
```python
# ❌ Это получает только один файл (первый)
order = PrintOrder.objects.get(id=order_id)
if order.file:
    # Отправка одного файла
    bot.send_photo(chat_id, order.file)
```

#### Новый способ (ПРАВИЛЬНО):
```python
# ✅ Это получает ВСЕ файлы
order = PrintOrder.objects.get(id=order_id)

# Вариант 1: Использовать метод модели
all_files = order.get_all_files()  # Возвращает QuerySet OrderFile
for order_file in all_files:
    file_path = order_file.file.path
    # Отправка файла в Telegram
    with open(file_path, 'rb') as f:
        bot.send_photo(chat_id, f, caption=f"Файл: {order_file.file.name}")

# Вариант 2: Использовать related_name
all_files = order.files.all()  # related_name='files' из модели OrderFile
for order_file in all_files:
    file_path = order_file.file.path
    with open(file_path, 'rb') as f:
        bot.send_photo(chat_id, f)

# Вариант 3: Получить только пути к файлам
file_paths = order.get_all_file_paths()  # Список путей
for file_path in file_paths:
    with open(file_path, 'rb') as f:
        bot.send_photo(chat_id, f)
```

### 3. Структура данных

```python
PrintOrder
├── file (FileField) - старое поле, только первый файл (для обратной совместимости)
└── files (related_name) - все файлы через OrderFile
    ├── OrderFile 1
    │   └── file (FileField)
    ├── OrderFile 2
    │   └── file (FileField)
    └── OrderFile N
        └── file (FileField)
```

### 4. Пример полного кода для бота

```python
from main.models import PrintOrder

def send_order_to_telegram(order_id, chat_id, bot):
    """Отправляет заявку со всеми файлами в Telegram"""
    try:
        order = PrintOrder.objects.get(id=order_id)
        
        # Формируем текст сообщения
        message_text = f"""
📋 Новая заявка #{order.id}

👤 Имя: {order.name}
📞 Телефон: {order.phone}
📧 Email: {order.email}
🔧 Услуга: {order.get_service_type_display()}
💬 Сообщение: {order.message}
📅 Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}
"""
        
        # Отправляем текстовое сообщение
        bot.send_message(chat_id, message_text)
        
        # Отправляем ВСЕ файлы
        all_files = order.files.all()  # Получаем все файлы
        
        if all_files.exists():
            for order_file in all_files:
                file_path = order_file.file.path
                file_name = order_file.file.name.split('/')[-1]
                
                # Определяем тип файла
                if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    # Отправляем как фото
                    with open(file_path, 'rb') as photo:
                        bot.send_photo(chat_id, photo, caption=f"📎 {file_name}")
                else:
                    # Отправляем как документ
                    with open(file_path, 'rb') as doc:
                        bot.send_document(chat_id, doc, caption=f"📎 {file_name}")
        else:
            bot.send_message(chat_id, "⚠️ Файлы не прикреплены")
            
    except PrintOrder.DoesNotExist:
        bot.send_message(chat_id, f"❌ Заявка #{order_id} не найдена")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Ошибка: {str(e)}")
```

### 5. Проверка

После обновления кода бота проверьте:
1. В админке Django видно все файлы в заявке
2. Бот отправляет все файлы в Telegram канал
3. Логи показывают количество сохраненных файлов

### 6. Логирование

В `views.py` добавлено подробное логирование:
- Количество полученных файлов
- Имена всех сохраненных файлов
- ID созданной заявки

Проверьте логи Django для отладки:
```bash
tail -f /path/to/logs/django.log | grep "Order created"
```

