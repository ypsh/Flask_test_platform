# -*- coding: UTF-8 -*-
class Compare:
    """比较dict是否相等"""

    def cmp_dict(self, src_data, dst_data):
        if type(src_data) != type(dst_data):
            print("type: '{}' != '{}'".format(type(src_data), type(dst_data)))
            return False
        if isinstance(src_data, dict):
            if len(src_data) != len(dst_data):
                print("dict len: '{}' != '{}'".format(len(src_data), len(dst_data)))
                return False
            for key in src_data:
                if not (key in dst_data):
                    print(key + '在dst不存在')
                    return False
                self.cmp_dict(src_data[key], dst_data[key])
        elif isinstance(src_data, list):
            if len(src_data) != len(dst_data):
                print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
                return False
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                self.cmp_dict(src_list, dst_list)
        else:
            if src_data != dst_data:
                print("value '{}' != '{}'".format(src_data, dst_data))
                return False
            else:
                return True

    """比较dict是否包含"""

    def contain_dict(self, src_data, dst_data):
        if type(src_data) != type(dst_data):
            print("type: '{}' != '{}'".format(type(src_data), type(dst_data)))
            return False
        if isinstance(src_data, dict):
            for key in src_data:
                if not (key in dst_data):
                    return False
                elif (key in dst_data) and (key in src_data):
                    if src_data[key] != dst_data[key]:
                        print('值不相等:%s %s' % (src_data[key], dst_data[key]))
                        return False
                self.cmp_dict(src_data[key], dst_data[key])
        elif isinstance(src_data, list):
            for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
                self.cmp_dict(src_list, dst_list)
        else:
            if src_data == dst_data:
                print("value '{}' != '{}'".format(src_data, dst_data))
                return False

    """比较相等"""

    def cmp_equal(self, src_data, dst_data):
        if type(src_data) == type(dst_data):
            if type('type') == type(src_data):
                if src_data == dst_data:
                    return True
                else:
                    return False
            else:
                result = self.cmp_dict(src_data, dst_data)
                if result is None:
                    return True
                else:
                    return result

    """比较包含"""

    def cmp_contain(self, src_data, dst_data):
        if type(src_data) == type(dst_data):
            if type('type') == type(src_data):
                if src_data.find(dst_data) != -1:
                    return True
                else:
                    return False
            else:
                result = self.contain_dict(src_data, dst_data)
                if result is None:
                    return True
                else:
                    return result

    def equal(self, exp, actual):
        return exp == actual

    def not_equal(self, exp, actual):
        return exp != actual

    def str_contains(self,dic,string):
        return str(dic).__contains__(string)


if __name__ == '__main__':
    s1 = {"code": "200", "message": "OK", "result": "OK"}
    s2 = {"result": "OK"}
