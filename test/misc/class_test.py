

class TEST:
    def __init__(self, name):
        self.value = 0
        self.name = name
        self.modifier = []
    
    def register_modifier(self, modi):
        self.modifier.append(modi)
    
    def do(self):
        for modi in self.modifier:
            modi.do(self)


class Modifier:
    def __init__(self, raise_num):
        self.raise_num = raise_num
    def do(self, cls):
        print("Original: ", cls.value,"Raise: ", self.raise_num)
        cls.value += self.raise_num
        print(cls.value)
        print(cls.name)
        return 0

if __name__ =="__main__":

    test = TEST("Main")

    for i in range(0, 5):
        modi = Modifier(i+1)
        test.register_modifier(modi)
    
    test.do()
