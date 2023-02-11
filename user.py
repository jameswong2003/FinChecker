class Profile:
    def __init__(self, name, starting_balance):
        self.name = name
        self.current_balance = starting_balance

    
    def addBalance(self, add):
        self.current_balance += add