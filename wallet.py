import csv
from datetime import datetime
from typing import List, Dict


class FinanceManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data: List[Dict[str, str]] = self.load_data()

    def load_data(self) -> List[Dict[str, str]]:
        data = []
        try:
            with open(self.file_name, 'r') as file:
                reader = csv.DictReader(file, delimiter=':')
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print("Файл не найден. Создание нового файла.")
        return data

    def save_data(self) -> None:
        with open(self.file_name, 'w', newline='') as file:
            fieldnames = ['Номер', 'Дата', 'Категория', 'Сумма', 'Описание']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=':')
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def display_balance(self) -> None:
        total_income = sum(float(row['Сумма']) for row in self.data if row['Категория'] == 'Доход')
        total_expenses = sum(float(row['Сумма']) for row in self.data if row['Категория'] == 'Расход')
        balance = total_income - total_expenses
        print(f"Баланс: {balance} | Доходы: {total_income} | Расходы: {total_expenses}")

    def add_transaction(self) -> None:
        new_row = {}
        new_row['Номер'] = len(self.data) + 1  # Автоматическое присвоение номера записи

        new_row['Дата'] = self.validate_input("Введите дату (гггг-мм-дд): ", lambda x: datetime.strptime(x, '%Y-%m-%d'))

        new_row['Категория'] = self.validate_input("Введите категорию (Доход/Расход): ", lambda x: x in ['Доход', 'Расход'])

        new_row['Сумма'] = self.validate_input("Введите сумму: ", lambda x: float(x))

        new_row['Описание'] = input("Введите описание: ")

        self.data.append(new_row)
        print("Транзакция добавлена.")

    def edit_transaction(self) -> None:
        index = int(input("Введите номер записи для редактирования: "))
        if 0 < index <= len(self.data):
            row = self.data[index - 1]
            print("Текущая запись:")
            print(row)
            field_to_edit = input("Введите название поля для редактирования (Дата/Категория/Сумма/Описание): ")
            new_value = input("Введите новое значение: ")
            if field_to_edit == 'Сумма':
                new_value = float(new_value)  # Преобразование в float для суммы
            elif field_to_edit == 'Дата':
                new_value = self.validate_input("Введите дату (гггг-мм-дд): ", lambda x: datetime.strptime(x, '%Y-%m-%d'))
            row[field_to_edit] = new_value
            print("Запись успешно изменена.")
        else:
            print("Некорректный номер записи.")

    def validate_input(self, prompt: str, validation_func) -> str:
        while True:
            user_input = input(prompt)
            try:
                if validation_func(user_input):
                    return user_input
                else:
                    print("Некорректный ввод. Попробуйте снова.")
            except ValueError:
                print("Некорректный ввод. Попробуйте снова.")


# Главная программа
file_name = "finance_data.csv"
finance_manager = FinanceManager(file_name)

while True:
    print("\n1. Показать баланс")
    print("2. Добавить транзакцию")
    print("3. Показать все")
    print("4. Поиск")
    print("5. Изменить транзакцию")
    print("6. Сохранить и выйти")

    choice = input("Выберите действие: ")

    if choice == '1':
        finance_manager.display_balance()
    elif choice == '2':
        finance_manager.add_transaction()
    elif choice == '3':
        for row in finance_manager.data:
            print(row)
    elif choice == '4':
        while True:
            print('1. По категории')
            print('2. По дате')
            print('3. По сумме')
            print('4. Назад')

            search = input("Выберите действие: ")

            if search == '1':
                category = input("Введите категорию: ")
                for row in finance_manager.data:
                    if row['Категория'] == category:
                        print(row)
            elif search == '2':
                date = input("Введите дату (гггг-мм-дд): ")
                for row in finance_manager.data:
                    if row['Дата'] == date:
                        print(row)
            elif search == '3':
                sum_input = input("Введите сумму: ")
                for row in finance_manager.data:
                    if row['Сумма'] == sum_input:
                        print(row)
            elif search == '4':
                break

    elif choice == '5':
        finance_manager.edit_transaction()

    elif choice == '6':
        finance_manager.save_data()
        print("Данные сохранены. До свидания!")
        break
    else:
        print("Некорректный выбор. Попробуйте снова.")
