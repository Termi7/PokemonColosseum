class Moves:
    def __init__(self, name='', typeMove='', category='', contest='',  PP=0, power=0, accuracy=0):
        self.name=name
        self.typeMove= typeMove
        self.category=category
        self.contest=contest
        self.PP=PP
        self.power=power
        self.accuracy=accuracy

    def getName(self):
        return self.name

    def getTypeMove(self):
        return self.typeMove

    def getCategory(self):
        return self.category

    def getContest(self):
        return self.contest

    def getPP(self):
        return self.PP

    def getPower(self):
        return self.power

    def getAccuracy(self):
        return self.accuracy

