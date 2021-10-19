class Test:
    var1 = 1
    var2 = 'zwei'

    def __init__(self):
        self.haus = 'drei'

    def test(self,auto):
        """
        text
        """

print(vars(Test))

t = Test()
t.test('hallo')

for key in (key for key in vars(Test) if not key.startswith('_')):
    print(key,': ',vars(Test)[key])

for key in (key for key in vars(t) if not key.startswith('_')):
    print(key,': ',vars(t)[key])