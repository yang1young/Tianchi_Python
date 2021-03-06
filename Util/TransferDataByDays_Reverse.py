#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16/4/23 下午2:50
# @Author  : ZHZ
# @Description  : 根据num_days去划分数据集,默认值是14

import pandas as pd
import numpy as np
import datetime
global sum_flag
num_days = 7
sum_flag_temp = 0

days_20141009 = datetime.datetime(2014, 10, 9)
item_id_dict = {}
all_item_sum = []
kid_item_sum = []
count1 = []
count2 = []

#filtered_outlier_if = pd.read_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/FilteredData/filtered_outlier_if.csv");
filtered_outlier_if = pd.read_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/OutputData/2_if2.csv");
filtered_outlier_if['days_20141009'] = filtered_outlier_if['date'].\
    map(lambda x:(datetime.datetime(x / 10000, x / 100 % 100, x % 100) - days_20141009).days)

#filtered_outlier_isf = pd.read_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/FilteredData/filtered_outlier_isf.csv");
#filtered_outlier_isf = pd.read_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/OutputData/2_isf2.csv");
#filtered_outlier_isf['days_20141009'] = filtered_outlier_isf['date'].\
#    map(lambda x:(datetime.datetime(x / 10000, x / 100 % 100, x % 100) - days_20141009).days)

def countByDays_if(dataframe, start_day, end_day):

    if start_day > end_day:
        return None,0
    dataframe = dataframe[dataframe['days_20141009']>=start_day]
    dataframe = dataframe[dataframe['days_20141009']<=end_day]
    if len(dataframe)<=0:
        return None,0
    per = float(num_days)/float(end_day-start_day+1)
    #print per
    #print start_day,end_day
    temp = {}
    #print start_day,end_day,dataframe.date.sort_values().head(1),dataframe.days_20141009.max()
    #temp['date'] = str(dataframe.date.min())+"_"+str(dataframe.date.max())
    # temp['date'] = str(dataframe.days_20141009.min()+num_days)+"_"+str(dataframe.days_20141009.max()+num_days)
    temp['date'] = (end_day-1)/num_days
    temp['item_id'] = item_id_dict[int(dataframe.item_id.mean())]
    temp['cate_id'] = dataframe.cate_id.max()
    temp['cate_level_id'] = dataframe.cate_level_id.max()
    temp['brand_id'] = dataframe.brand_id.max()
    temp['supplier_id'] = dataframe.supplier_id.max()
    temp['pv_ipv'] = dataframe.pv_ipv.sum()*per
    temp['pv_uv'] = dataframe.pv_uv.sum()*per
    temp['cart_ipv'] = dataframe.cart_ipv.sum()*per
    temp['cart_uv'] = dataframe.cart_uv.sum()*per
    temp['collect_uv'] = dataframe.collect_uv.sum()*per
    temp['num_gmv'] = dataframe.num_gmv.sum()*per
    temp['amt_gmv'] = dataframe.amt_gmv.sum()*per
    temp['qty_gmv'] = dataframe.qty_gmv.sum()*per
    temp['unum_gmv'] = dataframe.unum_gmv.sum()*per
    temp['amt_alipay'] = dataframe.amt_alipay.sum()*per
    temp['num_alipay'] = dataframe.num_alipay.sum()*per
    temp['qty_alipay'] = dataframe.qty_alipay.sum()*per
    temp['unum_alipay'] = dataframe.unum_alipay.sum()*per
    temp['ztc_pv_ipv'] = dataframe.ztc_pv_ipv.sum()*per
    temp['tbk_pv_ipv'] = dataframe.tbk_pv_ipv.sum()*per
    temp['ss_pv_ipv'] = dataframe.ss_pv_ipv.sum()*per
    temp['jhs_pv_ipv'] = dataframe.jhs_pv_ipv.sum()*per
    temp['ztc_pv_uv'] = dataframe.ztc_pv_uv.sum()*per
    temp['tbk_pv_uv'] = dataframe.tbk_pv_uv.sum()*per
    temp['ss_pv_uv'] = dataframe.ss_pv_uv.sum()*per
    temp['jhs_pv_uv'] = dataframe.jhs_pv_uv.sum()*per
    temp['num_alipay_njhs'] = dataframe.num_alipay_njhs.sum()*per
    temp['amt_alipay_njhs'] = dataframe.amt_alipay_njhs.sum()*per
    temp['qty_alipay_njhs'] = dataframe.qty_alipay_njhs.sum()*per
    temp['unum_alipay_njhs'] = dataframe.unum_alipay_njhs.sum()*per
    temp['is_final'] = False

    sum_flag_temp = dataframe.qty_alipay_njhs.sum()*per
    if end_day>=431:
        count1.append(0)
    if end_day==444:
        temp['date'] = 444/num_days
        count2.append(0)
        temp['is_final'] = True
    #print start_day,end_day
    print temp['item_id'],start_day,end_day,temp['date'],temp['qty_alipay_njhs']

    #print dataframe[['item_id','days_20141009','qty_alipay_njhs']]
    #print temp['item_id'],temp['date'],temp['qty_alipay_njhs']
    return temp,sum_flag_temp

def TransferDataByDays_if():
    new_father_kid_item_x = []
    new_father_kid_item_all = []
    for i,father_kid_item in filtered_outlier_if.groupby([filtered_outlier_if['cate_level_id'],
                                            filtered_outlier_if['cate_id'],
                                            filtered_outlier_if['item_id']]):

        first_day = father_kid_item.days_20141009.min()
        last_day = father_kid_item.days_20141009.max()
        flag_day = last_day
        print first_day,last_day
        father_kid_item  = father_kid_item.sort_values('days_20141009')

        is_first = True
        sum_flag = 0

        while(flag_day>=first_day):
            flag_day = flag_day - num_days
            if (flag_day<=first_day):
                temp,sum_flag_temp = countByDays_if(father_kid_item, first_day, flag_day+num_days)
            else:
                temp,sum_flag_temp = countByDays_if(father_kid_item, flag_day+1, flag_day+num_days)
            if temp == None:
                print "这里有个None"
                continue

            temp['qty_alipay_njhs']  = sum_flag
            sum_flag = sum_flag_temp
            new_father_kid_item_x.append(temp)
            new_father_kid_item_all.append(temp)

        new_father_kid_item_train = pd.DataFrame(new_father_kid_item_x,columns=[
            "date","item_id","cate_id","cate_level_id","brand_id","supplier_id","pv_ipv","pv_uv","cart_ipv","cart_uv",
            "collect_uv","num_gmv","amt_gmv","qty_gmv","unum_gmv","amt_alipay","num_alipay","qty_alipay","unum_alipay",
            "ztc_pv_ipv","tbk_pv_ipv","ss_pv_ipv","jhs_pv_ipv","ztc_pv_uv","tbk_pv_uv","ss_pv_uv","jhs_pv_uv","num_alipay_njhs",
            "amt_alipay_njhs","unum_alipay_njhs","is_final","qty_alipay_njhs"])

        new_father_kid_item_train[new_father_kid_item_train['is_final']==False].drop(["is_final"],axis = 1).\
            to_csv('/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/2016_04_24/train'+str(item_id_dict[i[2]])+'.csv',index = None,columns=None)
        new_father_kid_item_x = []
        #break
    print len(count1),len(count2)

    new_father_kid_item_all = pd.DataFrame(new_father_kid_item_all,columns=[
            "date","item_id","cate_id","cate_level_id","brand_id","supplier_id","pv_ipv","pv_uv","cart_ipv","cart_uv",
            "collect_uv","num_gmv","amt_gmv","qty_gmv","unum_gmv","amt_alipay","num_alipay","qty_alipay","unum_alipay",
            "ztc_pv_ipv","tbk_pv_ipv","ss_pv_ipv","jhs_pv_ipv","ztc_pv_uv","tbk_pv_uv","ss_pv_uv","jhs_pv_uv","num_alipay_njhs",
            "amt_alipay_njhs","unum_alipay_njhs","is_final","qty_alipay_njhs"])

    new_father_kid_item_all.to_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/"
                                        "Data/if_all.csv",index = None,columns=None)
    if_all_predict = new_father_kid_item_all[new_father_kid_item_all['is_final']].drop(["is_final"],axis = 1)

    if_all_predict.to_csv('/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/if_all_predict.csv',index = None,columns=None)
    # new_father_kid_item[new_father_kid_item['is_final']==False].drop(["is_final"],axis = 1).\
    # to_csv('/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/Data/if_all_train.csv',index = None,columns=None)
def TransferDataByDays_isf():
    new_father_kid_item_data = []
    for i,father_kid_item in filtered_outlier_isf.groupby([filtered_outlier_isf['cate_level_id'],
                                            filtered_outlier_isf['cate_id'],
                                            filtered_outlier_isf['item_id'],
                                            filtered_outlier_isf['store_code']]):

        first_day = father_kid_item.days_20141009.min()
        last_day = father_kid_item.days_20141009.max()
        flag_day = last_day
        print first_day,last_day

        father_kid_item  = father_kid_item.sort_values('days_20141009')

        father_kid_item_data = {}
        #print father_kid_item[father_kid_item['days_20141009']==last_day]
        is_first = True

        while(flag_day>=first_day):
            flag_day = flag_day - num_days
            if (flag_day<first_day):
                temp = countByDays_if(father_kid_item, first_day, flag_day+num_days)
            else:
                temp = countByDays_if(father_kid_item, flag_day+1, flag_day+num_days)

            if is_first:
                is_first = False
                kid_item_sum.append({'item_id':str(i[2])+"_"+str(i[3]),'sum':temp['qty_alipay_njhs']})

            if temp == None:
                print "这里有个None"
            else:
                new_father_kid_item_data.append(temp)
        #break
    new_father_kid_item = pd.DataFrame(new_father_kid_item_data,columns=[
        "date","item_id","cate_id","cate_level_id","brand_id","supplier_id","pv_ipv","pv_uv","cart_ipv","cart_uv",
        "collect_uv","num_gmv","amt_gmv","qty_gmv","unum_gmv","amt_alipay","num_alipay","qty_alipay","unum_alipay",
        "ztc_pv_ipv","tbk_pv_ipv","ss_pv_ipv","jhs_pv_ipv","ztc_pv_uv","tbk_pv_uv","ss_pv_uv","jhs_pv_uv","num_alipay_njhs",
        "amt_alipay_njhs","qty_alipay_njhs","unum_alipay_njhs"]
                                       ).to_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/"
                                                "Data/isf_all.csv",index = None,columns=None)

def transItemID():
    item_ids = filtered_outlier_if.item_id.value_counts().sort_values().index
    df_data = []
    for i in range(0,len(item_ids)):
        temp = {}
        temp['item_id'] = item_ids[i]
        temp['new_id'] = i
        item_id_dict[item_ids[i]] = i
        #print i,item_ids[i]
        df_data.append(temp)
    pd.DataFrame(df_data,columns=['item_id','new_id']).to_csv("/Users/zhuohaizhen/PycharmProjects/Tianchi_Python/"
                                        "Data/item_id.csv",index = None,columns=None)


transItemID()
TransferDataByDays_if()
