import sqlite3
from currency_converter import CurrencyConverter

currency1 = CurrencyConverter()

keys = {1: "Balance_CNY", 2: "Balance_USD", 3: "Balance_EUR"}

usd_eur_pair = currency1.convert(1, "USD", "EUR")
eur_usd_pair = currency1.convert(1, "EUR", "USD")
usd = currency1.convert(1, "USD", "CNY")
eur = currency1.convert(1, "EUR", "CNY")
action = 0
summa = 0
select = []
balance = 0
new_balance = 0


class DataBase:
    """Класс для работы с базой данных"""

    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()

    def create_table(self, sql):
        """Создание таблицы"""
        with self.con:
            self.cur.execute(sql)
            self.con.commit()
            return True

    def insert_user(self, rub_q, usd_q, eur_q):
        """Создание пользователя"""
        with self.con:
            result = self.cur.execute("""SELECT UserID FROM users_balance""").fetchall()
            if len(result) == 0:
                with self.con:
                    self.cur.execute("""
                    INSERT INTO users_balance(
                    Balance_CNY, Balance_USD, Balance_EUR)
                    VALUES(?, ?, ?);""", (rub_q, usd_q, eur_q,))
                    self.con.commit()
                    return True

    def get_balance(self, currency, user_id):
        """Получение баланса из базы данных"""
        global balance
        with self.con:
            res = self.cur.execute(f"SELECT {currency} FROM users_balance WHERE UserID = ?;", (user_id,)).fetchone()
            balance = res[0]
            return True

    def set_balance(self, bal, cur, user_id):
        """Установка нового значения баланса в базе данных"""
        with self.con:
            self.cur.execute(f"UPDATE users_balance SET {cur} = ? WHERE UserID = ?""", (bal, user_id))
            self.con.commit()
            self.get_balance(cur, user_id)
            print(f"Остаток на счете {cur}: {balance} {cur[-3:]}")
            print()
            return True


def insert_sum():
    """Валидация суммы"""
    global summa
    try:
        summa = float(input("Какая сумма Вас интересует?: \n"
                            "Для возврата в главное меню введите 0 \n"))
        if summa < 0:
            print("Сумма должна быть больше нуля, попробуйте снова")
            insert_sum()
        elif summa == 0:
            print("Возвращаюсь в главное меню")
            select.clear()
            main()
        else:
            return True
    except ValueError:
        print("Вы ввели не корректное значение")
        insert_sum()


def select_action():
    """Выбор действия в меню"""
    global select
    try:
        global action
        if len(select) == 0:
            text = "Введите какую валюту желаете обменять: "
        else:
            text = "Какую валюту готовы предложить взамен: "
        action = int(input(f"{text} \n"
                           "1. CNY \n"
                           "2. USD \n"
                           "3. EUR \n"
                           "4. Покинуть обменник \n").strip())
        if action not in (1, 2, 3, 4):
            print("Вы ввели не корректное значение")
            select_action()
        elif action == 4:
            print("Спасибо, до скорой встречи!")
            exit()
        else:
            if action not in select:
                select.append(action)
            else:
                print("Вы ввели не допустимую команду")
                select_action()
    except ValueError:
        print("Вы ввели не корректное значение")
        select_action()


def check_summa():
    insert_sum()
    if balance >= summa:
        global new_balance
        new_balance = balance - summa
        print(f"С вашего счета '{keys[select[1]]}' списано: {summa} {keys[select[1]][-3:]}")
        data.set_balance(round(new_balance, 2), keys[select[1]], 1)
        data.get_balance(keys[select[1]], 1)
        data.get_balance(keys[select[0]], 1)
        delta = round(currency1.convert(summa, keys[select[1]][-3:], keys[select[0]][-3:]), 2)
        print(f"Пополнение счета '{keys[select[0]]}' на сумму: {delta} {keys[select[0]][-3:]}")
        new_balance = balance + delta
        data.set_balance(round(new_balance, 2), keys[select[0]], 1)
        select.clear()
        print("Возвращаюсь в главное меню")
    else:
        print("На вашем счете недостаточно средств")
        check_summa()


data = DataBase("exchanger.db")


def main():
    """Основная программа"""
    global keys
    data.create_table(
        """CREATE TABLE IF NOT EXISTS users_balance(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Balance_CNY INTEGER NOT NULL,
        Balance_USD INTEGER NOT NULL,
        Balance_EUR INTEGER NOT NULL);""")
    data.insert_user(100000, 1000, 1000)

    while True:
        print()
        print(
            f"Добро пожаловать в наш обменный пункт, курс валют следующий: "
            f"\n USD = {round(usd, 2)} CNY"
            f"\n EUR = {round(eur, 2)} CNY"
            f"\n USD = {round(usd_eur_pair, 2)} EUR"
            f"\n EUR = {round(eur_usd_pair, 2)} USD")
        select_action()
        print(f"Ваш выбор {select[0]}. {keys[select[0]][-3:]}")
        select_action()
        print(f"Ваш выбор {select[1]}. {keys[select[1]][-3:]}")
        data.get_balance(keys[select[1]], 1)
        print(f"На вашем балансе {balance} {keys[select[1]][-3:]}")
        check_summa()


if __name__ == '__main__':
    main()
