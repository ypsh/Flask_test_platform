from com.common.generatedata import Generate

class MakdeData():
    def __init__(self):
        self.g=Generate()

    def get_info(self,*args):
        info = []
        try:
            if args[0].city !="":
                self.g.set_city(args[0].city)
            if args[0].age != "":
                age = str(args[0].age).split("-")
                self.g.set_age(int(age[0]),int(age[1]))
            if args[0].sex != "":
                map = {"男":0,"女":1,"随机":3}
                self.g.set_sex(map[args[0].sex])
        except Exception as e:
            pass

        for i in range(0,1000):
            id = self.g.generating_ID_card("info")
            if id is not None:
                name = self.g.generating_nanme()
                mobile_phone = self.g.generating_phone_number()
                mail = self.g.generating_email()
                info.append([i + 1, name, id["id"], mobile_phone, mail, id["age"], id["sex"], id["city"]])
        return  info