class Test:
    var1 = 1
    var2 = 'zwei'

    def __init__(self):
        pass

    def __iter__(self):
        for attr in self.__dict__:
            print(attr, value)
            yield attr, value

for key in (key for key in vars(Test) if not key.startswith('_')):
    print(key,': ',vars(Test)[key])
