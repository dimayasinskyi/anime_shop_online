from django.test import TestCase
from django.db.models.signals import pre_save
from django.core.files.uploadedfile import SimpleUploadedFile

import re, glob, os

from .models import Goods, Categories


class GoodAndCategoryModelTest(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(title='Test category')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif',
        )
        self.good = Goods.objects.create(title='Test good', description='This is test good', com_qty=500, sel_qty=500, price=500.00, image=image, category=self.category, cropping='1x1').full_clean()

    def test_create_category(self):
        category = Categories.objects.get(title='Test category')
        self.assertEqual(str(category), category.title)

    def test_create_good_and_connection_category(self):
        good = Goods.objects.get(title='Test good')

        expected = {
            'title': 'Test good',
            'description': 'This is test good',
            'com_qty': 500,
            'sel_qty': 500,
            'price': 500.00,
            'category': self.category,
        }
        for field, value in expected.items():
            self.assertEqual(getattr(good, field), value)
        
        self.assertIn('test_image', good.image.name)
        self.assertEqual(str(good), good.title)
        
        goods_in_category = self.category.goods_set.all()
        self.assertIn(good, goods_in_category)
        self.assertEqual(goods_in_category.count(), 1)

        self.assertTrue(os.path.isfile(good.image.path), msg="Зображення не завантажене")

        url = os.path.splitext(re.sub(r'_[A-Za-z0-9]+(?=\.)', '', good.image.path))[0]
        good.delete()
        for img in glob.glob(url+'*'):
            self.assertFalse(os.path.isfile(img), msg="Файл зображення не видалено автоматично")



# ✅ 1. Тести моделей
# 🔹 Ти вже зробив:

#  Тест створення категорії
#  Тест створення товару
#  Перевірка __str__ методів (str(good) == good.title)
#  Валідація кількостей (наприклад, sel_qty <= com_qty)
#  Зв’язок між товарами та категоріями
#  Перевірка збереження зображення

# ✅ 2. Тести форм (forms)
#  Тест на валідну форму створення товару

#  Тест на невалідну форму (наприклад, price <= 0, відсутнє зображення)

#  Перевірка обов'язкових полів

# ✅ 3. Тести представлень (views)
#  Сторінка списку товарів (чи віддає статус 200 і містить товар)

#  Сторінка конкретного товару (чи відкривається)

#  Пошук товарів (?find=назва)

#  Фільтр по категоріям (?cate=1)

#  Помилки 404 для неіснуючих товарів/категорій

#  Створення товару (POST-запит)

#  Оновлення товару (перевірка редагування)

#  Видалення товару

# ✅ 4. Тести URL'ів
#  Чи правильні шляхи ведуть до правильних view

#  Чи можна відкрити сторінку по reverse('shop:product_detail', args=[product.pk])

# ✅ 5. Тести шаблонів (templates)
#  Тест чи використовується правильний шаблон

#  Тест чи виводиться потрібна інформація в шаблоні

#  Чи є кнопки, зображення, посилання

# ✅ 6. Тести авторизації та доступу
#  Тест чи можна створити товар тільки авторизованому користувачу

#  Тест чи неавторизований користувач не має доступу до створення/редагування

#  Тест реєстрації/входу

# ✅ 7. Тести замовлення (якщо вже є)
#  Створення замовлення

#  Перевірка статусів: новий, в роботі, виконано, скасовано

#  Додавання товарів у кошик

#  Зменшення кількості com_qty після покупки

# ✅ 8. Тести API (якщо використовуєш DRF або інше)
#  GET список товарів

#  POST створення нового товару (тільки авторизовані)

#  PUT/PATCH редагування

#  DELETE товару

# ✅ 9. Тести безпеки
#  Перевірка доступу до дій (редагування товару не твоїм користувачем)

#  XSS в назвах товару (при виведенні)

# 🎁 Бонус: Тести пошти / оплати (опційно)
#  Відправка листа після замовлення

#  Перевірка обробки оплати (якщо є)





# Що перевірити або покращити:
# 1. 🧱 Назви моделей, наприклад Goods
# Якщо в тебе є модель Goods — краще назвати її Good (в однині).

# Django сам створює таблицю goods, це стандарт.

# 4. 📝 README.md — відсутній
# Обов'язково додай файл README.md:


# 5. 🔐 Секрети в settings.py
# Якщо в settings.py є SECRET_KEY, краще перенести в .env файл.

# Підключити бібліотеку python-decouple або dotenv.

# python
# Копіювати
# Редагувати
# # settings.py
# from decouple import config
# SECRET_KEY = config("SECRET_KEY")