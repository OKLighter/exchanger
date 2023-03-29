# exchanger
В связи с последними новостями
Рубль поменял на китайский юань CNY

1. Создать базу данных exchanger.db
2. Создать таблицу users_balance с колонками UserID, Balance_RUB (INTEGER), Balance_USD (INTEGER),
Balance_EUR (INTEGER)
3. Добавить пользователя с данными 100000, 1000, 1000
4. Добавить следующий функционал:
- обмен валюты по желанию пользователя
5. Позволить пользователю самостоятельно выбрать валютную пару, используя ввод в консоль
и произвести обмен валюты, через input()
6. Добавить все необходимые проверки и добавить сообщения об успешной операции, ошибках и т.д.

Алгоритм работы программы:

1. Приветствие: "Добро пожаловать в наш обменный пункт, курс валют следующий:
1 USD = 70 RUB
1 EUR = 80 RUB
1 USD = 0,87 EUR
1 EUR = 1,15 USD

Введите какую валюты желаете обменять:
1. RUB
2. USD
3. EUR

- Пользователь вводит цифру, обозначающую валюту (пример 2) - то есть выбрал USD

2. Какая сумма Вас интересует?

- Пользователь вводит сумму (пример 100) - то есть пользователь выбрал 100 USD

3. Какую валюту готовы предложить взамен?
1. RUB
2. USD
3. EUR

- Пользователь выбирает валюту, невозможно производить обмен двух одинаковых валют, то есть в данном примере
выбрать так же USD. К примеру пользователь ввел 1 - то есть RUB

4. Произвести расчет сколько RUB понадобится польователю для обмена на 100 USD.
Сдеать проверку на то что на счету достаточно RUB для обмена, в случае если недостаточно - оповестить

5. Произвести обмен валюты, при этом изменить значение в базе данных: + 100 USD и - 100 * 70 = 7000 RUB
