# -*- coding: UTF-8 -*-
import random


class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return None

    def __getrandomvalue__(self, key):
        if key in self.__dict__:
            item = random.randint(0, len(self.__dict__[key]) - 1)
            return self.__dict__[key][item]
        else:
            return None


const = _const()
# 计息方式
const.intCalcType = ['eq_prin_int', 'eq_prin_amt','before_inte_after_prin']
# 性别
const.gender = ['F', 'M']
# 附件类型
const.attachmentsType = [
    "bank_idcard_front",
    "bank_idcard_front",
    "bank_idcard_front_crop",
    "bank_idcard_back_crop",
    "bank_idcard_head_photo",
    "bank_living_photo",
    "bank_living-video",
    "bank_personal_info_authorize",
    "bank_credit_authorize",
    "bank_register",
    "bank_loan_contract",
    "bank_withhold",
    "bank_account_service_protocol",
    "bank_electronic_loan_iou",
    "bank_investigation_report"
]
# 教育程度
const.education = [
    "unknown",
    "master_above",
    "undergraduate",
    "junior_college",
    "senior_below"
]
# 婚姻状态
const.marriage = [
    "unknown",
    "unmarried",
    "married"
]
# 额度循环类型
const.cycelType = [
    "nocycle",
    "clear",
    "term",
    "repay"
]
# 联系方式
# const.contact_info
# 联系方式类型
const.contactType = [
    "wechat",
    "alipay",
    "qq",
    "mobile",
    "telephone",
    "email"
]
# 还款类型
const.repayType = [
    "clear",
    "term"
]
# 卡类型
const.type = ['debit', 'credit']
# 还款方式
const.repayWay = [
    "cardi",
    "cardii",
    "wxpay",
    "compensate"
]
# 银联标识
const.unionMark = [0, 1]
# 关系类型
const.relateType = [
    "spouse",
    "parents",
    "children",
    "brothers_sisters",
    "relatives",
    "friends",
    "classmate",
    "colleagues",
    "other"
]
# 联系方式
# const.contact_info
# 联系类型
const.contactType = [
    "wechat",
    "alipay",
    "qq",
    "mobile",
    "telephone",
    "email"
]
# 月收入区间
const.monthIncome = [
    "unknown",
    "0_3000",
    "3001_6000",
    "6001_12000",
    "12001_20000",
    "20001_above"
]
# 工作年限
const.workYear = [
    "unknown",
    "one_year",
    "three_year",
    "five_year",
    "five_above"
]
# 单位性质
const.corpType = [
    "unknown",
    "state_owned_comp",
    "wholly_foreign_owned_enterprise",
    "joint_ventures",
    "public_limited_comp",
    "private_comp",
    "governmental_agencies"
]
# 工作状态
const.workStatus = [
    "unknown",
    "full_time",
    "part_time",
    "self_employed",
    "student"
]
# 行业
const.industry = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18
]
# 职位
const.duty = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
]
# 民族
const.nation = [
    "汉族",
    "蒙古族",
    "回族",
    "藏族",
    "维吾尔族",
    "苗族",
    "彝族",
    "壮族",
    "布依族",
    "朝鲜族",
    "满族",
    "侗族",
    "瑶族",
    "白族",
    "土家族",
    "哈尼族",
    "哈萨克族",
    "傣族",
    "黎族",
    "僳僳族",
    "佤族",
    "畲族",
    "高山族",
    "拉祜族",
    "水族",
    "东乡族",
    "纳西族",
    "景颇族",
    "柯尔克孜族",
    "土族",
    "达斡尔族",
    "仫佬族",
    "羌族",
    "布朗族",
    "撒拉族",
    "毛南族",
    "仡佬族",
    "锡伯族",
    "阿昌族",
    "普米族",
    "塔吉克族",
    "怒族",
    "乌孜别克族",
    "俄罗斯族",
    "鄂温克族",
    "德昂族",
    "保安族",
    "裕固族",
    "京族",
    "塔塔尔族",
    "独龙族",
    "鄂伦春族",
    "赫哲族",
    "门巴族",
    "珞巴族",
    "基诺族"
]
