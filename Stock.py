# -*- coding: UTF-8 -*-

import baostock as bs


class Stock:
    def __init__(self, code="sh.600036", start_date='2020-10-27', end_date='2020-11-27'):
        self.code = code
        self.data_list = []
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        # 登陆系统
        lg = bs.login()
        if lg.error_code is True:
            return lg.error_code, lg.error_msg
        # 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
        # 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
        # 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
        # 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
        # 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
        # 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
        # 成长指数，例如：sz.399376 小盘成长 等；
        # 价值指数，例如：sh.000029 180价值 等；
        # 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；

        # 详细指标参数，参见“历史行情指标参数”章节；“周月线”参数与“日线”参数不同。
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        # adjustflag 表示复权类型，1为后复权，2为前复权，3为不复权
        # frequency表示周期，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、
        # 60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
        rs = bs.query_history_k_data_plus(self.code,
                                          "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                                          start_date=self.start_date, end_date=self.end_date, frequency="d",
                                          adjustflag='2')
        if rs.error_code is True:
            return rs.error_code, rs.error_msg
        self.data_list = []
        while rs.next():
            self.data_list.append(rs.get_row_data())
        if len(self.data_list) > 0:
            return 0, "OK"
        else:
            return 1, "没有相关数据!"

    def rsv(self, c_list):  # 计算给定序列的RSV
        c_min = min(c_list)
        c_max = max(c_list)
        if c_min == c_max:  # 没有涨跌幅
            return 50
        return (c_list[-1]-c_min)/(c_max-c_min)*100

    def kdj_cell(self, c_list, k_last=50, d_last=50):
        rsv = self.rsv(c_list)
        k = (2/3)*k_last + (1/3)*rsv
        d = (2/3)*d_last + (1/3)*k
        j = 3*k - 2*d
        return k, d, j

    def kdj_sig(self, n=-1):  # n表示从过去的第几个kdj开始算，默认从上一个交易日开始
        k = d = 50
        for i in range(n, 1):
            k, d, j = self.kdj_cell(self.get_c_list(i), k, d)
        return k, d, j

    def get_c_list(self, end=0, n=9):  # end<=0,为计算锚点，默认当天开始，向过去取9天
        if len(self.data_list) < n-end:  # 数据不够
            print("采集的数据不够")
            return []
        c_list = []
        for i in range(end-n, end):
            c_list.append(float(self.data_list[i][5]))  # 取出收盘价尾缀到c_list
        return c_list


if __name__ == '__main__':
    stock = Stock("sh.600036")
    e, m = stock.get_data()
    print(e)
    if e is False:
        print("login failure!")
    else:
        print("login success!")
    k, d, j = stock.kdj_sig()
    if j > 100:
        print("j=%d, 可卖出！" %j)
    elif j < 0:
        print("j=%d, 可买入！" %j)
    else:
        print("j=%d, 不动！" %j)



