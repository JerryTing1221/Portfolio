#!/usr/bin/env python
# coding: utf-8

# In[11]:


def resrecommand(*locs):
    from math import sqrt
    from math import cos
    from math import sin
    import math
    import csv
    import pandas as pd
    import numpy as np
    from collections import defaultdict
    from random import sample

    #======================================================================================================================

    def rad(d):
        return d * math.pi / 180.0

    def getDistance(lat1, lon1, lat2, lon2):
        EARTH_REDIUS = 6378.137
        radLat1 = rad(lat1)
        radLat2 = rad(lat2)
        a = radLat1 - radLat2
        b = rad(lon1) - rad(lon2)
        s = 2 * math.asin(math.sqrt(math.pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b/2), 2)))
        s = s * EARTH_REDIUS
        return s

    def location(x):
        if x in loc:
            lat1 = loc[x][0]
            lon1 = loc[x][1]
            return lat1, lon1
    def restaurant(x):
        if x in loc:
            return loc[x]
            lat2 = loc[x][0]
            lon2 = loc[x][1]
            return lat2, lon2

    #======================================================================================================================

    locfile = '景點經緯度.csv'  #csv檔案路徑 
    with open(locfile, newline='', encoding='utf-8-sig') as csvlocfile:
        data = list(csv.reader(csvlocfile))
    loc = dict()
    for row in data:
        loc[row[0]] = list(row[1:])
    del loc['景點名稱']

    resfile = '餐廳經緯度.csv'  #csv檔案路徑 
    with open(resfile, newline='', encoding='utf-8-sig') as csvresfile:
        data = list(csv.reader(csvresfile))
    res = dict()    
    for row in data:
        res[row[0]] = list(row[1:])
    del res['餐廳']

    #======================================================================================================================
    
    userlocList= []
    loclatlonList = []
    for l in locs:
        userlocList.append(l)
        loclatlon = loc[l]
        loclatlonList.append(loclatlon)

    locslist = dict()
    for i in range(len(userlocList)):
        lat1 = float(loclatlonList[i][0])
        lon1 = float(loclatlonList[i][1])
        locslist[userlocList[i]] = (lat1,lon1) # 將三組經緯度加入字典

    #======================================================================================================================

    nearresList = []
    for l in locslist:
        loaction = l
        lat1 = float(loc[l][0])
        lon1 = float(loc[l][1])
        for i in res:
            resvalue = res[i]
            lat2 = float(resvalue[0])
            lon2 = float(resvalue[1])
            s = getDistance(lat1, lon1, lat2, lon2)
        #     print(location)
        #     print(lat1)
        #     print(lon1)
        #     print(i)
        #     print(lat2)
        #     print(lon2)
        #     print('距離' + str(round(s,2)) + '公里')
            if round(s, 2) < 0.5:
                nearres = i
                nearresList.append(nearres)
            else:
                continue
                
    #======================================================================================================================
    if len(nearresList) > 3:
        nearresList = sample(nearresList, 3)
    elif len(nearresList) > 0 and len(nearresList) < 3:
        nearresList = nearresList
    else:
        nearresList = '附近暫無推薦餐廳'
    #======================================================================================================================

    return nearresList


# In[31]:


resrecommand('安平古堡')

