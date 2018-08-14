class Media:
    def __init__(self, name):
        self.name = name
        self.facebook = 0
        self.twitter = 0
        self.url = ""
        self.rate = 0


obj = Media("xui")
obj.twitter = 10
print(obj.name, obj.twitter)
