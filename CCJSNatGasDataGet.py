import requests
import json
import datetime
import time
import os
from shutil import copyfile


def login():
    """获取token"""
    data = {'username': 'cchg', 'password': 'cchg123!@#'}
    url = "http://ganghua.dsmcase.com:88/lrd/login"
    r = requests.post(url=url, json=data, headers=headers)
    # 将获取到的token返回
    return (r.json()["data"]["token"])

def getTodayDate():
    """获取时间"""
    today_date = datetime.date.today()#- datetime.timedelta(days=1) #更改数据时间
    today_str = today_date.strftime("%Y-%m-%d")
    yestoday_date = today_date - datetime.timedelta(days=1)
    yestoday_str = yestoday_date.strftime("%Y-%m-%d")
#     print(today_str,yestoday_str)
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    today_stamp = str(round(today_stamp*1000))
    yestoday_stamp = time.mktime(time.strptime(yestoday_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    yestoday_stamp = str(round(yestoday_stamp*1000))
    return today_stamp, yestoday_stamp

def Parmasdata(deviceCodes,keys):
    """JSON字符包含流量信息"""
    endtime,starttime = getTodayDate()
    data = {'page':'1','limit':'289','startTime':starttime,
               'endTime':endtime,'deviceCodes':deviceCodes,'keys':keys}
    getTbHistoryValue = requests.get(
        url="http://ganghua.dsmcase.com:88/lrd/dashboard/tbhistory/getTbHistoryValue",
        params=data,
        headers=headers
    )
#     print(getTbHistoryValue.json())
    return getTbHistoryValue.json()['data']

def confirm_login():
    """调用获取登录信息接口，将登录成功后，返回的token放在该请求的header中"""
    #将login（）方法中返回的token放入header中

    headers["Token"] = login()
#    获取设备名称(2个C_11000427_2,C_11000427_3)
    getDevices = requests.get(
        url="http://ganghua.dsmcase.com:88//lrd/dashboard/tbhistory/getDevices",
        headers=headers
    )
    deviceCodes = list(getDevices.json()['data'])
    
    # 获取设备属性（C3 c4 c5 c6）
    getKeys = requests.get(
        url="http://ganghua.dsmcase.com:88/lrd/dashboard/tbhistory/getKeys",
        headers=headers
    )
    keys = getKeys.json()['data']

    listname = []
    MC0573dataFC6SUM = Parmasdata('C_V0000057_3','C6')   #0573累计流量
    MC0572dataFC6SUM = Parmasdata('C_V0000057_2','C6')   #0572累计流量
    MC0571dataFC6SUM = Parmasdata('C_V0000057_1','C6')   #0571累计流量
    MC4273dataFC6SUM = Parmasdata('C_11000427_3','C6')   #4273累计流量
    MC4272dataFC6SUM = Parmasdata('C_11000427_2','C6')   #4272累计流量
    MC4271dataFC6SUM = Parmasdata('C_11000427_1','C6')   #4271累计流量
#    
    listname.append(MC0573dataFC6SUM)
    listname.append(MC0572dataFC6SUM)
    listname.append(MC0571dataFC6SUM)
    listname.append(MC4273dataFC6SUM)
    listname.append(MC4272dataFC6SUM)
    listname.append(MC4271dataFC6SUM)
    return MC0573dataFC6SUM,MC0572dataFC6SUM,MC0571dataFC6SUM,MC4273dataFC6SUM,MC4272dataFC6SUM,MC4271dataFC6SUM

def Datatotxtsample(x,name,srcname):
    """生成txt"""
    for i in range(len(x["list"])):
        valuex = x["list"][i]['value']
        time = x["list"][i]['collectionTime']
        value = valuex
        linex = f'TAGNAME=Root.CN.EL.NatGas.{name}'+ '\n'
        liney = 'ITEM=VALUE,VALUE={},TIMESTAMP={},QUALITY=192'.format(value,time)+ '\n'
        new_context = linex+liney 
        with open(srcname,"a+") as f:
            f.write(new_context)
        # print(linex,liney)

if __name__ == "__main__":
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    today_date = datetime.date.today()#- datetime.timedelta(days=1) #更改数据时间
    today_str = today_date.strftime("%Y-%m-%d")
    srcname=f'CCJSNatGas{today_str}.Txt'
    txtname = r'\\192.168.220.238\ccjspims\CCJSNatGas\DATE\CCJSNatGas.Txt' #\\192.168.220.238\ccjspims\CCJSNatGas\DATE
    MC0573dataFC6SUM,MC0572dataFC6SUM,MC0571dataFC6SUM,MC4273dataFC6SUM,MC4272dataFC6SUM,MC4271dataFC6SUM = confirm_login()
    if(os.path.exists(srcname)):
        os.remove(srcname)
    Datatotxtsample(MC4273dataFC6SUM,'FI-CS001',srcname) # kunlun4273
    Datatotxtsample(MC4272dataFC6SUM,'FI-CS002',srcname) # kunlun4272
    Datatotxtsample(MC0572dataFC6SUM,'FI-KL001',srcname) # changshu0572
    Datatotxtsample(MC0571dataFC6SUM,'FI-KL002',srcname) # changshu0571
    copyfile(srcname, txtname) #复制到pims文件夹