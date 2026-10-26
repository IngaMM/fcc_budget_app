import math

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False
        end

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total+=item['amount']
        return total

    def get_amount_spent(self):
        total = 0
        for item in self.ledger:
            if item['amount'] < 0:
                total-=item['amount']
        return total

    def transfer(self, amount, other_instance):
        if self.withdraw(amount, f'Transfer to {other_instance.name}'):
            other_instance.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        star_str = int((30 - len(self.name))/2) * '*'
        output = star_str + self.name + star_str
        if len(output) < 30:
            output += '*\n'
        else:
            output += '\n'
        for entry in self.ledger:
            description = entry['description'][0:23]
            amount = f"{entry['amount']:.2f}"[0:7]
            filler_length = 30 - len(description) - len(amount)
            output += description + filler_length * ' ' + amount + '\n'
        output += f"Total: {self.get_balance():.2f}"
        return output

def get_percentages(categories):
    percentages = []
    total_spent = 0
    for category in categories:
        amount_spent = category.get_amount_spent()

        percentages.append(amount_spent)
        total_spent += amount_spent

    percentages = [math.floor(percentage/total_spent * 100) for percentage in percentages]

    print(percentages)
    return percentages

def create_spend_chart(categories):
    output = 'Percentage spent by category\n'
    percentages = get_percentages(categories)
    value = 100
    while value >= 0:
        bar = ''
        for index, category in enumerate(categories):
            if value <= percentages[index]:
                bar += ' o '
            else:
                bar += 3 * ' '

        output += f"{str(value):>3}" + '|' + bar + ' ' + '\n'
        value -= 10

    line = 4 * ' ' + '-' + 3 * len(categories) * '-' + '\n'

    output += line

    max_name_length = max([len(category.name) for category in categories])
    i = 0
    while i <= max_name_length - 1:
        label = ''
        for category in categories:
            if i < len(category.name):
                label += category.name[i] + 2 * ' '
            else:
                label += 3 * ' '
        label_line = 5 * ' ' + label
        if i < max_name_length - 1:
            label_line += '\n'
        i+=1
        output += label_line
    return output

food = Category('Food')
clothing = Category('Clothing')
software = Category('Software')
hardware = Category('Hardware')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
food.transfer(50, clothing)
clothing.deposit(100, 'initial deposit')
clothing.withdraw(16.00, 'pants')
clothing.withdraw(56.00, 'shirts')
hardware.deposit(1000, 'initial depsoit')
hardware.withdraw(350.56, 'new CPU')
hardware.withdraw(124.33, 'new motherboard')
software.deposit(250.00, 'initial deposit')
software.withdraw(200, 'Windows 11')
print(food)
print(clothing)
print(software)
print(hardware)

print(create_spend_chart([food, clothing, software, hardware]))
