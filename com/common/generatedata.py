# -*- coding:utf-8 -*-
import random
import logging
import string
from datetime import date, timedelta

from com.common.getPath import Path


class Generate():
    def __init__(self):
        self.global_path = Path().get_current_path()
        self.district_code = self.get_district_code()
        self.min_age = 1919
        self.max_age = 2018
        self.sex = 2

    def get_district_code(self):
        """
        获取身份证头信息地址码
        :return:地址码字典
        """
        district_code_path = self.global_path + "\\config\\districtcode.txt"
        with open(district_code_path) as file:
            data = file.read()
        district_list = data.split('\n')
        code_list = []
        for node in district_list:
            if node[10:11] != ' ':
                state = node[10:].strip()
            if node[10:11] == ' ' and node[12:13] != ' ':
                city = node[12:].strip()
            if node[10:11] == ' ' and node[12:13] == ' ':
                district = node[14:].strip()
                code = node[0:6]
                code_list.append({"state": state, "city": city, "district": district, "code": code})
        return code_list

    def set_city(self, cityname):
        """
        设置身份地址范围，市级范围
        :param cityname: 市级名称如：成都市
        """
        result = []
        for item in self.district_code:
            if str(item['city']).__contains__(cityname):
                result.append(item)
        self.district_code = result

    def set_age(self, min_age, max_age):
        """
        设置身份证号的年龄范围
        :param min_age: 最小年龄
        :param max_age: 最大年龄
        :return:
        """
        try:
            now_yeaer = date.today().year
            if max_age >= min_age:
                self.max_age = now_yeaer - min_age
                self.min_age = now_yeaer - max_age
            else:
                self.max_age = now_yeaer - max_age
                self.min_age = now_yeaer - min_age
        except Exception as e:
            logging.error(str(e))

    def set_sex(self, sex):
        """
        设置性别
        :param boolean: 0 男，1 女 ，2 随机
        :return:
        """
        if sex in [0, 1, 2]:
            self.sex = sex

    def get_sequentiancode(self):
        try:
            scode = random.randint(100, 300)
            if self.sex == 2:
                return scode
            elif self.sex == 0:
                if scode % 2 == 1:
                    return scode
                else:
                    return self.get_sequentiancode()
            elif self.sex == 1:
                if scode % 2 == 0:
                    return scode
                else:
                    return self.get_sequentiancode()
        except Exception as e:
            logging.error(str(e))

    def generating_ID_card(self,type='id'):
        """
        生成身份证号
        :return: list{'city':'age':'','sex':'','id':''}
        """
        try:
            random_city = random.randint(0, len(self.district_code) - 1)
            city = self.district_code[random_city]['code']  # 地区项
            age = random.randint(self.min_age, self.max_age)
            id = city + str(age)  # 年份项
            da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
            id = id + da.strftime('%m%d')
            sex = self.get_sequentiancode()
            id = id + str(sex)

            count = 0
            weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
            checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '4',
                         '9': '3',
                         '10': '2'}  # 校验码映射
            for i in range(0, len(id)):
                count = count + int(id[i]) * weight[i]
            id = id + checkcode[str(count % 11)]  # 算出校验码
            result = {'city': self.district_code[random_city]['city'], 'age': date.today().year-age, 'sex': ["女","男"][sex%2], 'id': id}
            if type=="id":
                return id
            else:
                return result
        except Exception as e:
            return None

    def generating_ID_card_batch(self, number):
        id = set()
        while True:
            id.add(self.generating_ID_card())
            if len(id)==number:
                break
        return id

    def generating_phone_number(self):
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186", "187", "188", "189"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    def generating_phone_number_batch(self,number):
        phone = set()

        while True:
            phone.add(self.generating_phone_number())
            if len(phone) == number:
                break
        return phone

    def generating_nanme(self):
        firstName = u"赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯咎管卢莫经房裘缪干解应宗宣丁贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄魏加封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘姜詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲台从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庚终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查后江红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于仲孙太叔申屠公孙乐正轩辕令狐钟离闾丘长孙慕容鲜于宇文司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓拔夹谷宰父谷粱晋楚阎法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福百家姓续"
        girl = u"秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽 "
        boy = u"伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘"
        if self.sex == 0:
            return random.choice(firstName) + random.choice(boy)
        elif self.sex == 1:
            return random.choice(firstName) + random.choice(girl)
        else:
            return random.choice(firstName) + random.choice(boy)

    def generating_email(self):
        try:
            email_end=("@163.com","@live.com","@qq.com","@sina.com","@126.com")
            strs = "abcdefghijklmnopqrstuvwxyz0123456789"
            email_start = "".join(random.choice(strs) for i in range(random.randint(4, 15)))
            return email_start+random.choice(email_end)
        except:
            pass



if __name__ == '__main__':
    g = Generate()
    g.set_city("西安")
    g.set_age(25, 25)
    list = []
    # g.set_sex(1)
    print(g.generating_ID_card_batch(2))
    print(g.generating_ID_card())
    # for i in range(0, 10):
    #     list.append(g.generating_ID_card())
    print(g.generating_email())

    print("ok")
