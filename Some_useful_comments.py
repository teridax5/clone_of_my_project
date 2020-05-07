import datetime as dt

today_date = dt.datetime.now()


class Record:
    def __init__(self, amount, comment, date=None):  # date=None to auto-input current date if it wasn't entered
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = today_date.date()  # here and next we transform datetime-variable into date-variable
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()  # transforming input data in format 'dd.mm.YY'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, obj):
        self.records.append(obj)  # we fill a one-dimensional massive with an object of a called class

    def get_today_stats(self):
        summary = 0
        for i in self.records:
            if i.date == today_date.date():  # a nice example of using an attribute of the packed object
                summary += i.amount
        return summary  # returning the integer to be called by subclass

    def get_week_stats(self):
        summary = 0
        for i in self.records:
            delta = today_date.date() - i.date
            if 0 <= delta.days <= 7:  # the easiest way to count days
                summary += i.amount
        return summary


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remain = self.limit - super().get_today_stats()
        if super().get_today_stats() < self.limit:  # we use a method of the superclass to count all today's ops.
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remain} кКал'
        else:
            return 'Хватит есть!'

    def get_today_stats(self):
        summary = super().get_today_stats()
        return f'За сегодня было съедено {summary} кКал.'  # a nice example of polymorphism

    def get_week_stats(self):
        summary = super().get_week_stats()
        return f'За последние 7 дней было съедено {summary} кКал.'


class CashCalculator(Calculator):
    EURO_RATE = 80.28
    USD_RATE = 74.28

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        #  Okay, this part is very important. If we create a dictionary as self.dict, we cannot change it when
        #  self.EURO_RATE and self.USD_RATE will be changed outside. So please, create your dictionary inside a method
        #  of a class to be called on every call of this method!!!
        value_dict = {'rub': ['руб', 1], 'usd': ['USD', self.USD_RATE], 'eur': ['Euro', self.EURO_RATE]}
        #  Manipulating with superclass'es method as it was changed in subclass and using our temporary dictionary!
        transact = round((self.limit - super().get_today_stats()) / value_dict[currency][1], 2)
        if super().get_today_stats() < self.limit:
            return f'На сегодня осталось {transact} {value_dict[currency][0]}'
        elif super().get_today_stats() > self.limit:
            return f'Денег нет, держись: твой долг - {-transact} {value_dict[currency][0]}'
        else:
            return 'Денег нет, держись'

    def get_today_stats(self):
        summary = super().get_today_stats()
        return f'За сегодня Вы потратили {summary} рублей.'

    def get_week_stats(self):
        summary = super().get_week_stats()
        return f'За последние 7 дней Вы потратили {summary} рублей.'