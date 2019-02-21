class someClass():
    def __init__(self):
        self.var = var = 200
        var = 300
        self.other = var
        var = 400
        print(self.var)
    def printIt(self):
        print(self.var)
    def updateIt(self, num):
        self.var = num
    def printOther(self):
        print(self.other)

#test = someClass()
#test.printIt()
#test.updateIt(600)
#test.printOther()

empty = tuple()

mt = empty
mt = ('',)

print(empty, type(empty))
print(mt, type(mt))

if not all(mt):
    print('sooooo')

if mt == ():
    print('Set to none then')