# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import requests
import json
import datetime
import time


# %%
def login():
    """获取token"""
    data = {'username':'cchg','password':'cchg123!@#'}
 
 
    url = "http://ganghua.dsmcase.com:88/lrd/login"
 
    r = requests.post(url=url, json=data, headers=headers)
    #将获取到的token返回

    return (r.json()["data"]["token"])


# %%
def getTodayDate():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    yestoday_date = today_date - datetime.timedelta(days=1)
    yestoday_str = yestoday_date.strftime("%Y-%m-%d")
#     print(today_str,yestoday_str)
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    today_stamp = str(round(today_stamp*1000))
    yestoday_stamp = time.mktime(time.strptime(yestoday_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    yestoday_stamp = str(round(yestoday_stamp*1000))
    return today_stamp, yestoday_stamp


# %%
def Parmasdata(deviceCodes,keys):
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


# %%
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
    # 获取历史资料keys[0]['name']
    # MC4272dataPC3 = Parmasdata(deviceCodes[0],'C3')   #4272压力
    # MC4272dataTC4 = Parmasdata(deviceCodes[0],'C4')   #4272温度
    # MC4272dataFC5 = Parmasdata(deviceCodes[0],'C5')   #4272流量
    MC4272dataFC6SUM = Parmasdata(deviceCodes[0],'C6')   #4272累计流量
    MC4273dataFC6SUM = Parmasdata(deviceCodes[1],'C6')   #4273累计流量
#     C3Pdata = {'page':'10','limit':'30','startTime':'1618296802000','endTime':'1618383202000','deviceCodes':deviceCodes[0],'keys':'C3'}
    
#     getTbHistoryValue = requests.get(
#         url="http://ganghua.dsmcase.com:88/lrd/dashboard/tbhistory/getTbHistoryValue",
#         params=C3Pdata,
#         headers=headers
#     )
#     print(r.headersgetDevices.json(),getKeys.json(),)
#     print(getTbHistoryValue.json())
    return MC4272dataFC6SUM,MC4273dataFC6SUM


# %%
def Datatotxt(x,y):
    if(os.path.exists("qtfs.txt")):
        os.remove("qtfs.txt")
    for i in range(0,len(x["list"]),3):
        valuex = x["list"][i]['value']
        valuey = y["list"][i]['value']
        time = y["list"][i]['collectionTime']
        value = valuex + valuey
        linex = 'TAGNAME=Root.CN.CCJS_BPA.BPA1.EXCEL.bondedtm'+ '\n'
        liney = 'ITEM=VALUE,VALUE={},TIMESTAMP={},QUALITY=192'.format(value,time)+ '\n'
        new_context = linex+liney 
        with open("qtfs.txt","a+") as f:
            f.write(new_context)
        # print(linex,liney)


# %%
if __name__ == "__main__":
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    x,y = confirm_login()
    Datatotxt(x,y)


