class Value:
    def __init__(self, value=None):
        if value:
            self.amount = value

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        self.amount = value * (1 - obj.commission)


if __name__ == '__main__':
    class AccountTest:
        amount = Value()

        def __init__(self, commission):
            self.commission = commission


    new_account = AccountTest(0.33)
    new_account.amount = 100

    print(new_account.amount)