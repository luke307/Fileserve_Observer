class Test:
    var1 = 1
    var2 = 'zwei'

    def __init__(self):
        pass

print(vars(Test))


for key in (key for key in vars(Test) if not key.startswith('_')):
    print(key,': ',vars(Test)[key])
