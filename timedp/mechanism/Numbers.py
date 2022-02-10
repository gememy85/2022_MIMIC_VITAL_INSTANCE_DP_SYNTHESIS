
class Numbers:
    def __init__(self, value:float):
        self.value = value

    def __repr__(self):
        return f"Numbers(type=={self.number_type})"

    def __str__(self):
        return self.value

class Positive(Numbers):
    def __init__(self, value):
        super().__init__(value)
        self.number_type = "positive"
    
class Negative(Numbers):
    def __init__(self, value):
        super().__init__(value)
        self.number_type = "negative"

class Zero(Numbers):
    def __init__(self, value):
        super().__init__(value)
        self.number_type = "zero"
