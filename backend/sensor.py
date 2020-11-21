
class Sensor:

    def __init__(self, name, typ):
        self.__name = name
        self.__typ = typ

    def setvalue(self, value):
        self.__value=value
    def getvalue(self):
        return self.__value
    def getname(self):
        return self.__name
    def gettyp(self):
        return self.__typ