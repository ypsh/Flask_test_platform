# -*- coding: UTF-8 -*-
class ListOperate:
    # 获取嵌套列表内子列表包含特定元素的特定列值
    def get_item(self, source_list, key, return_number):
        if type([]) == type(source_list):
            for item in source_list:
                if item.__contains__(key):
                    return item[return_number]
        return None
