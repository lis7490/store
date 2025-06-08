class Product:
    def __init__(self, catalog=None):
        self.products = catalog.products if catalog else []
        self.next_id = max([p['id'] for p in self.products], default=0) + 1
        self.cart = []  # Корзина для покупок
        self.discount_rules = []  # Правила скидок
        self.tax_rate = 0.20  # Стандартная ставка налога 20%
        self.catalog = catalog  # Сохраняем переданный каталог

    # Методы для работы с каталогом
    def _find_product_by_id(self, product_id):

        for product in self.products:
            if product['id'] == product_id:
                return product
        return None

    def add_product(self, name, category, price, weight, description):
        product = {
            'id': self.next_id,
            'name': name,
            'category': category,
            'price': float(price),
            'weight': float(weight),
            'description': description
        }
        self.products.append(product)
        self.next_id += 1
        print(f"Товар '{name}' (ID: {product['id']}) добавлен в каталог.")
        return product['id']

    def edit_product(self, product_id, **kwargs):
        product = self._find_product_by_id(product_id)
        if not product:
            print(f"Товар с ID {product_id} не найден.")
            return False

        valid_fields = ['name', 'category', 'price', 'weight', 'description']
        for field, value in kwargs.items():
            if field in valid_fields:
                if field in ['price', 'weight']:
                    try:
                        value = float(value)
                    except ValueError:
                        print(f"Ошибка: неверный формат для поля {field}")
                        continue
                product[field] = value
        print(f"Товар с ID {product_id} обновлен.")
        return True

    def delete_product(self, product_id):
        """Удаление товара из каталога"""
        product = self._find_product_by_id(product_id)
        if not product:
            print(f"Товар с ID {product_id} не найден.")
            return False

        self.products.remove(product)
        print(f"Товар '{product['name']}' (ID: {product_id}) удален из каталога.")
        return True

    def get_total_products(self):
        """Получение общего количества товаров"""
        return len(self.products)

    def get_product_info(self, product_id):
        """Получение полной информации о товаре"""
        product = self._find_product_by_id(product_id)
        if not product:
            print(f"Товар с ID {product_id} не найден.")
            return None

        return product

    def display_catalog(self):
        """Отображение каталога товаров"""
        print("\n=== КАТАЛОГ ТОВАРОВ ===")
        # Используем self.products вместо self.catalog.products
        for product in self.products:
            print(f"\nID: {product['id']}")
            print(f"Название: {product['name']}")
            print(f"Категория: {product['category']}")
            print(f"Цена: {product['price']:.2f} руб.")
            print(f"Вес: {product['weight']:.2f} кг")
            print(f"Описание: {product['description']}")
        print("\n=======================")


    # Методы для работы с корзиной
    def add_to_cart(self, product_id, quantity=1):
        """Добавление товара в корзину"""
        product = self._find_product_by_id(product_id)
        if not product:
            print(f"Товар с ID {product_id} не найден.")
            return False

        # Проверяем, есть ли уже такой товар в корзине
        for item in self.cart:
            if item['product']['id'] == product_id:
                item['quantity'] += quantity
                print(f"Количество товара '{product['name']}' в корзине увеличено до {item['quantity']}.")
                return True

        # Если товара еще нет в корзине
        self.cart.append({
            'product': product,
            'quantity': quantity
        })
        print(f"Товар '{product['name']}' добавлен в корзину.")
        return True

    def remove_from_cart(self, product_id, quantity=None):
        """Удаление товара из корзины"""
        for item in self.cart[:]:
            if item['product']['id'] == product_id:
                if quantity is None or quantity >= item['quantity']:
                    self.cart.remove(item)
                    print(f"Товар '{item['product']['name']}' полностью удален из корзины.")
                else:
                    item['quantity'] -= quantity
                    print(f"Количество товара '{item['product']['name']}' уменьшено до {item['quantity']}.")
                return True

        print(f"Товар с ID {product_id} не найден в корзине.")
        return False

    def display_cart(self):
        """Отображение содержимого корзины"""
        print("\n=== ВАША КОРЗИНА ===")
        if not self.cart:
            print("Корзина пуста.")
        else:
            total_price = 0
            total_weight = 0

            for item in self.cart:
                product = item['product']
                subtotal = product['price'] * item['quantity']
                total_price += subtotal
                total_weight += product['weight'] * item['quantity']

                print(f"\nID: {product['id']}")
                print(f"Название: {product['name']}")
                print(f"Категория: {product['category']}")
                print(f"Цена за шт.: {product['price']:.2f} руб.")
                print(f"Вес за шт.: {product['weight']:.2f} кг")
                print(f"Количество: {item['quantity']}")
                print(f"Итого: {subtotal:.2f} руб.")

            print("\n=== ИТОГО ===")
            print(f"Общая стоимость: {total_price:.2f} руб.")
            print(f"Общий вес: {total_weight:.2f} кг")
        print("\n===================")

    def clear_cart(self):
        """Очистка корзины"""
        self.cart = []
        print("Корзина очищена.")

    def get_cart_total(self):
        """Получение общей стоимости корзины"""
        return sum(item['product']['price'] * item['quantity'] for item in self.cart)

    def sort_cart(self, algorithm='quick', key='price', reverse=False):
        """
        Сортировка корзины с выбором алгоритма и параметров

        Параметры:
        algorithm - алгоритм сортировки ('bubble', 'insertion', 'quick', 'merge')
        key - поле для сортировки ('price', 'weight', 'category', 'name')
        reverse - порядок сортировки (False - возрастание, True - убывание)
        """
        if not self.cart:
            print("Корзина пуста, сортировка не требуется.")
            return

        # Выбираем ключ для сортировки
        key_func = {
            'price': lambda x: x['product']['price'],
            'weight': lambda x: x['product']['weight'],
            'category': lambda x: x['product']['category'],
            'name': lambda x: x['product']['name']
        }.get(key.lower(), lambda x: x['product']['price'])

        # Выбираем алгоритм сортировки
        algorithms = {
            'bubble': self._bubble_sort,
            'insertion': self._insertion_sort,
            'quick': self._quick_sort,
            'merge': self._merge_sort
        }

        if algorithm.lower() not in algorithms:
            print(f"Алгоритм '{algorithm}' не поддерживается. Используется быстрая сортировка.")
            algorithm = 'quick'

        print(f"\nСортировка корзины с помощью {algorithms[algorithm].__name__} по {key} "
              f"({'убывание' if reverse else 'возрастание'})")

        # Создаем копию списка для сортировки
        items_to_sort = self.cart.copy()

        # Выполняем сортировку
        sorted_items = algorithms[algorithm](items_to_sort, key_func, reverse)

        # Обновляем корзину
        self.cart = sorted_items
        print("Корзина успешно отсортирована.")

        # Реализации алгоритмов сортировки

    def _bubble_sort(self, items, key, reverse=False):
        n = len(items)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                a = key(items[j])
                b = key(items[j + 1])

                if (a > b and not reverse) or (a < b and reverse):
                    items[j], items[j + 1] = items[j + 1], items[j]
        return items

    def _insertion_sort(self, items, key, reverse=False):
        for i in range(1, len(items)):
            current = items[i]
            j = i - 1
            while j >= 0 and (
                    (key(items[j]) > key(current) and not reverse) or
                    (key(items[j]) < key(current) and reverse)
            ):
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = current
        return items

    def _quick_sort(self, items, key, reverse=False):
        if len(items) <= 1:
            return items

        pivot = items[len(items) // 2]
        pivot_key = key(pivot)
        left = [x for x in items if (key(x) < pivot_key) ^ reverse]
        middle = [x for x in items if key(x) == pivot_key]
        right = [x for x in items if (key(x) > pivot_key) ^ reverse]

        return self._quick_sort(left, key, reverse) + middle + self._quick_sort(right, key, reverse)

    def _merge_sort(self, items, key, reverse=False):
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = self._merge_sort(items[:mid], key, reverse)
        right = self._merge_sort(items[mid:], key, reverse)

        return self._merge(left, right, key, reverse)

    def _merge(self, left, right, key, reverse):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            left_val = key(left[i])
            right_val = key(right[j])

            if (left_val <= right_val and not reverse) or (left_val >= right_val and reverse):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def calculate_total(self, include_tax=True, apply_discounts=True):
        """
        Расчет общей стоимости товаров в корзине с учетом налогов и скидок

        Параметры:
        include_tax - учитывать ли налог (по умолчанию True)
        apply_discounts - применять ли скидки (по умолчанию True)

        Возвращает словарь с различными суммами:
        {
            'subtotal': общая стоимость без налогов и скидок,
            'discounts': сумма скидок,
            'tax': сумма налога,
            'total': итоговая сумма к оплате
        }
        """
        if not self.cart:
            return {
                'subtotal': 0,
                'discounts': 0,
                'tax': 0,
                'total': 0
            }

        # Рассчитываем базовую стоимость
        subtotal = sum(item['product']['price'] * item['quantity'] for item in self.cart)

        # Применяем скидки
        discounts = 0
        if apply_discounts:
            discounts = self._apply_discounts(subtotal)

        # Рассчитываем сумму после скидок
        amount_after_discounts = subtotal - discounts

        # Рассчитываем налог
        tax = 0
        if include_tax:
            tax = amount_after_discounts * self.tax_rate

        # Итоговая сумма
        total = amount_after_discounts + tax

        return {
            'subtotal': subtotal,
            'discounts': discounts,
            'tax': tax,
            'total': total
        }

    def _apply_discounts(self, subtotal):
        """Внутренний метод для применения всех активных скидок"""
        total_discount = 0

        for rule in self.discount_rules:
            if rule['type'] == 'percentage':
                # Скидка в процентах от суммы
                discount = subtotal * rule['value'] / 100
                total_discount += discount
            elif rule['type'] == 'fixed':
                # Фиксированная скидка
                total_discount += rule['value']
            elif rule['type'] == 'threshold':
                # Скидка при превышении порога
                if subtotal >= rule['threshold']:
                    if rule['discount_type'] == 'percentage':
                        discount = subtotal * rule['discount_value'] / 100
                    else:
                        discount = rule['discount_value']
                    total_discount += discount

        # Не позволяем скидке превысить сумму заказа
        return min(total_discount, subtotal)

    def add_discount_rule(self, rule_type, value=None, threshold=None, discount_type=None, discount_value=None):
        """
        Добавление правила скидки

        Поддерживаемые типы скидок:
        1. Процентная скидка: {'type': 'percentage', 'value': 10} - 10% скидка
        2. Фиксированная скидка: {'type': 'fixed', 'value': 500} - скидка 500 руб.
        3. Пороговая скидка: {'type': 'threshold', 'threshold': 10000,
                              'discount_type': 'percentage/fixed',
                              'discount_value': 10/500}
                              - при заказе от 10000 руб. скидка 10% или 500 руб.
        """
        rule = {'type': rule_type}

        if rule_type == 'percentage':
            rule['value'] = float(value)
        elif rule_type == 'fixed':
            rule['value'] = float(value)
        elif rule_type == 'threshold':
            rule['threshold'] = float(threshold)
            rule['discount_type'] = discount_type
            rule['discount_value'] = float(discount_value)
        else:
            raise ValueError("Неизвестный тип скидки")

        self.discount_rules.append(rule)
        print(f"Добавлено правило скидки: {rule}")

    def set_tax_rate(self, rate):
        """Установка ставки налога (в десятичном формате, например 0.20 для 20%)"""
        self.tax_rate = float(rate)
        print(f"Ставка налога установлена: {rate * 100}%")

    def display_totals(self):
        """Отображение итоговой суммы с детализацией"""
        totals = self.calculate_total()

        print("\n=== ИТОГОВАЯ СУММА ===")
        print(f"Общая стоимость товаров: {totals['subtotal']:.2f} руб.")
        print(f"Скидки: -{totals['discounts']:.2f} руб.")
        print(f"Сумма после скидок: {totals['subtotal'] - totals['discounts']:.2f} руб.")
        print(f"Налог ({self.tax_rate * 100}%): {totals['tax']:.2f} руб.")
        print(f"ИТОГО К ОПЛАТЕ: {totals['total']:.2f} руб.")
        print("======================")

    def main_menu(self):
        while True:
            print("\n=== ГЛАВНОЕ МЕНЮ ===")
            print("1. Просмотр каталога товаров")
            print("2. Добавить товар в корзину")
            print("3. Удалить товар из корзины")
            print("4. Просмотр корзины")
            print("5. Сортировка корзины")
            print("6. Расчет итоговой суммы")
            print("7. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.display_catalog()
            elif choice == '2':
                self.add_to_cart_interface()
            elif choice == '3':
                self.remove_from_cart_interface()
            elif choice == '4':
                self.display_cart()
            elif choice == '5':
                self.sort_cart_interface()
            elif choice == '6':
                self.display_totals()
            elif choice == '7':
                print("До свидания!")
                break
            else:
                print("Неверный ввод, попробуйте еще раз.")


class TextInterface:
    """Класс для текстового интерфейса"""

    def __init__(self, catalog):
        self.catalog = catalog

    def main_menu(self):
        while True:
            print("\n=== ГЛАВНОЕ МЕНЮ ===")
            print("1. Просмотр каталога товаров")
            print("2. Добавить товар в корзину")
            print("3. Удалить товар из корзины")
            print("4. Просмотр корзины")
            print("5. Сортировка корзины")
            print("6. Расчет итоговой суммы")
            print("7. Выход")

            choice = input("Выберите действие: ")

            if choice == '1':
                self.catalog.display_catalog()
            elif choice == '2':
                self.add_to_cart_interface()
            elif choice == '3':
                self.remove_from_cart_interface()
            elif choice == '4':
                self.catalog.display_cart()
            elif choice == '5':
                self.sort_cart_interface()
            elif choice == '6':
                self.catalog.display_totals()
            elif choice == '7':
                print("До свидания!")
                break
            else:
                print("Неверный ввод, попробуйте еще раз.")

    def add_to_cart_interface(self):
        product_id = int(input("Введите ID товара: "))
        quantity = int(input("Введите количество (по умолчанию 1): ") or 1)
        self.catalog.add_to_cart(product_id, quantity)

    def remove_from_cart_interface(self):
        product_id = int(input("Введите ID товара: "))
        quantity = input("Введите количество для удаления (оставьте пустым для удаления всех): ")
        quantity = int(quantity) if quantity else None
        self.catalog.remove_from_cart(product_id, quantity)

    def sort_cart_interface(self):
        print("\nДоступные алгоритмы сортировки: bubble, insertion, quick, merge")
        algorithm = input("Выберите алгоритм (по умолчанию quick): ") or 'quick'

        print("\nДоступные поля для сортировки: price, weight, category, name")
        key = input("Выберите поле для сортировки (по умолчанию price): ") or 'price'

        reverse = input("Сортировать по убыванию? (y/n, по умолчанию n): ").lower() == 'y'

        self.catalog.sort_cart(algorithm=algorithm, key=key, reverse=reverse)


# Пример использования
if __name__ == "__main__":
    catalog = Product()
    # Добавляем товары
    phone_id = catalog.add_product(
        name="Смартфон Samsung Galaxy S21",
        category="Смартфоны",
        price=69990,
        weight=0.17,
        description="Флагманский смартфон с AMOLED-экраном и тройной камерой"
    )

    laptop_id = catalog.add_product(
        name="Ноутбук ASUS VivoBook 15",
        category="Ноутбуки",
        price=54990,
        weight=1.8,
        description="Ультрабук с процессором Intel Core i5 и SSD на 512 ГБ"
    )

    # Выводим каталог
    catalog.display_catalog()

    # Редактируем товар
    catalog.edit_product(
        phone_id,
        name="Смартфон Samsung Galaxy S21 Ultra",
        price=79990,
        description="Флагманский смартфон с S-Pen, AMOLED-экраном и 108MP камерой"
    )

    # Проверяем изменения
    phone = catalog.get_product_info(phone_id)
    print("\nОбновленная информация о товаре:")
    print(f"Название: {phone['name']}")
    print(f"Новая цена: {phone['price']} руб.")
    print(f"Новое описание: {phone['description']}")

    # Удаляем товар
    catalog.delete_product(laptop_id)

    # Проверяем каталог после удаления
    print("\nКаталог после удаления:")
    catalog.display_catalog()

    # Итоговое количество товаров
    print(f"\nВсего товаров в каталоге: {catalog.get_total_products()}")

    # Добавляем товары в каталог
    phone_id = catalog.add_product(
        name="Смартфон Samsung Galaxy S21",
        category="Смартфоны",
        price=69990,
        weight=0.17,
        description="Флагманский смартфон"
    )

    laptop_id = catalog.add_product(
        name="Ноутбук ASUS VivoBook 15",
        category="Ноутбуки",
        price=54990,
        weight=1.8,
        description="Ультрабук с SSD"
    )

    headphones_id = catalog.add_product(
        name="Наушники Sony WH-1000XM4",
        category="Аксессуары",
        price=29990,
        weight=0.25,
        description="С шумоподавлением"
    )

    # Работа с корзиной
    catalog.add_to_cart(phone_id, 2)
    catalog.add_to_cart(laptop_id)
    catalog.add_to_cart(headphones_id, 3)

    # Просмотр корзины
    catalog.display_cart()

    # Удаление товаров из корзины
    catalog.remove_from_cart(headphones_id, 2)  # Уменьшаем количество
    catalog.remove_from_cart(phone_id)  # Полностью удаляем

    # Просмотр изменений
    catalog.display_cart()

    # Очистка корзины
    catalog.clear_cart()
    catalog.display_cart()

# Пример использования с сортировкой


    # Добавляем товары в каталог
    catalog.add_product("Смартфон Samsung", "Смартфоны", 69990, 0.17, "Флагман")
    catalog.add_product("Ноутбук ASUS", "Ноутбуки", 54990, 1.8, "Ультрабук")
    catalog.add_product("Наушники Sony", "Аксессуары", 29990, 0.25, "Беспроводные")
    catalog.add_product("Телевизор LG", "Телевизоры", 129990, 18.2, "OLED")
    catalog.add_product("Мышь Logitech", "Аксессуары", 4990, 0.1, "Беспроводная")

    # Добавляем товары в корзину
    catalog.add_to_cart(1, 2)
    catalog.add_to_cart(2)
    catalog.add_to_cart(3, 3)
    catalog.add_to_cart(4)
    catalog.add_to_cart(5)

    print("\nИсходная корзина:")
    catalog.display_cart()

    # Примеры сортировки
    print("\nСортировка пузырьком по цене (возрастание):")
    catalog.sort_cart(algorithm='bubble', key='price', reverse=False)
    catalog.display_cart()

    print("\nСортировка вставками по весу (убывание):")
    catalog.sort_cart(algorithm='insertion', key='weight', reverse=True)
    catalog.display_cart()

    print("\nБыстрая сортировка по категории (возрастание):")
    catalog.sort_cart(algorithm='quick', key='category', reverse=False)
    catalog.display_cart()

    print("\nСортировка слиянием по названию (убывание):")
    catalog.sort_cart(algorithm='merge', key='name', reverse=True)
    catalog.display_cart()

# Пример использования с налогами и скидками


    # Добавляем товары
    catalog.add_product("Смартфон", "Электроника", 50000, 0.2, "Флагман")
    catalog.add_product("Ноутбук", "Электроника", 80000, 2.5, "Игровой")
    catalog.add_product("Наушники", "Аксессуары", 15000, 0.3, "Беспроводные")

    # Добавляем в корзину
    catalog.add_to_cart(1, 2)  # 2 смартфона
    catalog.add_to_cart(2)  # 1 ноутбук
    catalog.add_to_cart(3, 3)  # 3 наушников

    # Настраиваем налоги и скидки
    catalog.set_tax_rate(0.20)  # 20% налог

    # Добавляем правила скидок:
    # 1. Общая 5% скидка на весь заказ
    catalog.add_discount_rule('percentage', value=5)

    # 2. Дополнительная фиксированная скидка 1000 руб.
    catalog.add_discount_rule('fixed', value=1000)

    # 3. Скидка 10% при заказе от 100000 руб.
    catalog.add_discount_rule('threshold', threshold=100000,
                              discount_type='percentage', discount_value=10)

    # Показываем корзину
    catalog.display_cart()

    # Показываем итоговую сумму с детализацией
    catalog.display_totals()

    # Пример получения отдельных значений
    totals = catalog.calculate_total()
    print(f"\nСумма без учета налогов: {totals['subtotal'] - totals['discounts']:.2f} руб.")
    print(f"Общая сумма к оплате: {totals['total']:.2f} руб.")



    # Запускаем интерфейс
    if __name__ == "__main__":
        # Создаем основной каталог
        main_catalog = Product()

        # Добавляем тестовые товары
        phone_id = main_catalog.add_product(
            name="Смартфон Samsung Galaxy S21",
            category="Смартфоны",
            price=69990,
            weight=0.17,
            description="Флагманский смартфон с AMOLED-экраном и тройной камерой"
        )

        laptop_id = main_catalog.add_product(
            name="Ноутбук ASUS VivoBook 15",
            category="Ноутбуки",
            price=54990,
            weight=1.8,
            description="Ультрабук с процессором Intel Core i5 и SSD на 512 ГБ"
        )

    interface = TextInterface(main_catalog)
    interface.main_menu()