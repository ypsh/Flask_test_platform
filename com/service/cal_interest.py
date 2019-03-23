class Cal_interest:
    def equivalent_prinicpal_interest(self):
        # 贷款额为a，月利率为i，年利率为I，还款月数为n
        a = 5000.00
        I = 0.18
        i = I / 12
        n = 60

        print("-----等额本息计算,以5个月为例-----")
        # 月均还款(本金+利息)
        b = a * i * pow((1 + i), n) / (pow((1 + i), n) - 1)
        # 还款利息总和
        Y = n * a * i * pow((1 + i), n) / (pow((1 + i), n) - 1) - a
        # 第一个月还款利息
        c1 = a * i
        # 剩余利息
        e1 = Y - c1
        # 剩余本金
        a1 = a - (b - c1)
        print("第1个月应还利息为%s,应还本金为%s,还款总额（本金+利息）为%s" % (c1, b - c1, b))
        # 第2 - n个月还款利息
        for t in range(2, 6):
            ci = (a * i - b) * pow((1 + i), (t - 1)) + b
            bi = b - ci
            print("第%d个月应还利息为%s,应还本金为%s,还款总额（本金+利息）为%s" % (t, ci, bi, b))

    def equivalent_prinicpl(self):
        print("-----等额本金计算,以5个月为例-----")
        a = 5000.00
        I = 0.18
        i = I / 12
        n = 60
        # 每月应还本金
        d = a / n
        for m in range(1, 6):
            f = (a - d * (m - 1)) * i  # 每月应还利息
            g = d + f
            print("第%d个月应还利息为%s,应还本金为%s,还款总额（本金+利息）为%s" % (m, f, d, g))

if __name__ == '__main__':
    Cal_interest().equivalent_prinicpal_interest()
    Cal_interest().equivalent_prinicpl()