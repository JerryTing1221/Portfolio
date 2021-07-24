from flask import Flask, request, render_template
from pandas.core.reshape.pivot import pivot_table
from werkzeug.datastructures import TypeConversionDict
import os
import pandas as pd
import numpy as np
from random import choice, shuffle
import random
import pro_word2vec
import pymysql.cursors
import pickle   #將python 序列化和反序列化的模塊  pickling=>dump儲存
from pymongo import MongoClient
from gensim.models import word2vec
from restaurant import resrecommand
import route




# MySQL連線配置資訊
config = {
    'host': '3.16.42.183',
    'port': 3306,
    'user': 'jerry',
    'password': '1221',
    'db': 'project',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}
# 建立連線
connection = pymysql.connect(**config)

# 建立遊標方法1
cursor = connection.cursor()


# MongoDB連線
model_name = 'wvmodel'
client = MongoClient("mongodb://" + "ec2-3-16-42-183.us-east-2.compute.amazonaws.com"+":27017") # No private key  
auth = client.admin.authenticate("chi","101") # Authenticate to admin
db = client['travel_project']
collection = db['models']

json_data = {}
data = collection.find({'name': model_name}) 
for i in data: 
    json_data = i #fetching model from db 
pickled_model = json_data[model_name] 
model = pickle.loads(pickled_model)




app = Flask(__name__)


#首頁
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')


# 第一頁
@app.route('/start',methods=['GET','POST'])
def chose_category():

    # 將9種Type裡含有景點分別放入一個list

    Type1list = os.listdir("C:/Users/Tibame/Desktop/專題網頁/static/分類/Type1list")
    shuffle(Type1list)
    Type2list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type2list')
    shuffle(Type2list)
    Type3list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type3list')
    shuffle(Type3list)
    Type4list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type4list')
    shuffle(Type4list)
    Type5list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type5list')
    shuffle(Type5list)
    Type6list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type6list')
    shuffle(Type6list)
    Type7list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type7list')
    shuffle(Type7list)
    Type8list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type8list')
    shuffle(Type8list)
    Type9list = os.listdir('C:/Users/Tibame/Desktop/專題網頁/static/分類/Type9list')
    shuffle(Type9list)

    return render_template('Page_1.html', Type1list=Type1list, Type2list=Type2list, 
    Type3list=Type3list, Type4list=Type4list, Type5list=Type5list, Type6list=Type6list, 
    Type7list=Type7list, Type8list=Type8list, Type9list=Type9list)




# 第二頁
@app.route('/show',methods=['GET','POST'])
def show():
    if request.method == 'POST':

        # 透過語意分析將各組景點排名
        rank = pd.read_excel('point_ranking.xlsx')

        Type1list = rank.loc[0][1:]
        Type2list = rank.loc[1][1:]
        Type3list = rank.loc[2][1:]
        Type4list = rank.loc[3][1:]
        Type5list = rank.loc[4][1:]
        Type6list = rank.loc[5][1:]
        Type7list = rank.loc[6][1:]
        Type8list = rank.loc[7][1:]
        Type9list = rank.loc[8][1:]


        # 獲取 Page1 使用者點的照片種類
        values = request.form.getlist('checkbox')
        
        # 找到使用者點的是哪一個種類，重新呼叫景點list
        photoClass1 = locals()[values[0]]
        photoClass2 = locals()[values[1]]
        photoClass3 = locals()[values[2]]

        return render_template('Page_2.html', values=values, photoClass1=photoClass1,
        photoClass2=photoClass2, photoClass3=photoClass3, Type1list=Type1list, Type2list=Type2list, 
        Type3list=Type3list, Type4list=Type4list, Type5list=Type5list, Type6list=Type6list, 
        Type7list=Type7list, Type8list=Type8list, Type9list=Type9list)




# 第三頁
@app.route('/recommend',methods=['GET','POST'])
def recommend():
    if request.method == 'POST':

        global location
        # 使用者選擇的地點
        answer = request.form.getlist('checkbox')
        location = []
        for i in answer:
            i.replace(' ','')
            location.append(i)
        

        # 找出使用者選擇地點的圖片檔案路徑
        path = []
        path_dic = {} 

        a = os.walk('C:/Users/Tibame/Desktop/專題網頁/static/分類')
        for root, dirs, files in a:
            path.append(root)

        for i in path:
            name = i.split('\\')[-1]
            route = i.replace("\\",'/')
            path_dic[name] = route

        place1_photo = path_dic[location[0]]
        place1_photo = place1_photo.replace('C:/Users/Tibame/Desktop/專題網頁','..') + "/" + location[0] + "1.jpg"
        place2_photo = path_dic[location[1]]
        place2_photo = place2_photo.replace('C:/Users/Tibame/Desktop/專題網頁','..') + "/" + location[1] + "1.jpg"
        place3_photo = path_dic[location[2]]
        place3_photo = place3_photo.replace('C:/Users/Tibame/Desktop/專題網頁','..') + "/" + location[2] + "1.jpg"

        
        
        # 協同過濾
        file = 'C:/Users/Tibame/Desktop/專題網頁/all_comments.xls'
        df = pd.read_excel(file) # local 讀檔案
        pivot_table = df.pivot_table(index=['使用者'],columns=['地點'],values="評價(1~5)")
        # 景點1
        point1 = pivot_table[location[0]]
        similarity_with_other_1 = pivot_table.corrwith(point1)  
        similarity_with_other_1 = similarity_with_other_1.sort_values(ascending=False)
        recomList1 = str(similarity_with_other_1.head(10)).replace('地點','').replace(' ','').replace('.','').replace('10','').split('\n')[1:-1]
        if location[0] in recomList1:
            recomList1.remove(location[0])
        # 景點2
        point2 = pivot_table[location[1]]
        similarity_with_other_2 = pivot_table.corrwith(point2)
        similarity_with_other_2 = similarity_with_other_2.sort_values(ascending=False)
        recomList2 = str(similarity_with_other_2.head(10)).replace('地點','').replace(' ','').replace('.','').replace('10','').split('\n')[1:-1]
        if location[1] in recomList2:
            recomList2.remove(location[1]) 
        # 景點3
        point3 = pivot_table[location[2]]
        similarity_with_other_3 = pivot_table.corrwith(point3)  
        similarity_with_other_3 = similarity_with_other_3.sort_values(ascending=False)
        recomList3 = str(similarity_with_other_3.head(10)).replace('地點','').replace(' ','').replace('.','').replace('10','').split('\n')[1:-1]
        if location[2] in recomList3:
            recomList3.remove(location[2])

        
        # word2vec
        # 景點1
        inputname = location[0]

        sql = """select ID,Tname
                from Attraction
                where cluster = (select cluster from Attraction where Tname = '%s')
                ;"""%(inputname)
        cursor.execute(sql)
        output = cursor.fetchall()

        # 轉成表格
        NewDF = pd.DataFrame(output)
        myID = NewDF['ID']
        myName = NewDF['Tname']
        myLen = len(NewDF)

        # 取得分析結果
        word2vec_recommend_1 = []
        word = pro_word2vec.pro_word2vec(inputname,myID,myName,myLen,model)
        for a in word:
            sql = """select Tname,Address 
                    from Attraction
                    where ID = '%s'
                    ;"""%(a)
            cursor.execute(sql)
            output = cursor.fetchall()
            for b in output:
                word2vec_recommend_1.append(b['Tname'])

        # 景點二
        inputname = location[1]

        sql = """select ID,Tname
                from Attraction
                where cluster = (select cluster from Attraction where Tname = '%s')
                ;"""%(inputname)
        cursor.execute(sql)
        output = cursor.fetchall()

        # 轉成表格
        NewDF = pd.DataFrame(output)
        myID = NewDF['ID']
        myName = NewDF['Tname']
        myLen = len(NewDF)

        # 取得分析結果
        word2vec_recommend_2 = []
        word = pro_word2vec.pro_word2vec(inputname,myID,myName,myLen,model)
        for a in word:
            sql = """select Tname,Address 
                    from Attraction
                    where ID = '%s'
                    ;"""%(a)
            cursor.execute(sql)
            output = cursor.fetchall()
            for b in output:
                word2vec_recommend_2.append(b['Tname'])

        
        # 景點三
        inputname = location[2]

        sql = """select ID,Tname
                from Attraction
                where cluster = (select cluster from Attraction where Tname = '%s')
                ;"""%(inputname)
        cursor.execute(sql)
        output = cursor.fetchall()

        # 轉成表格
        NewDF = pd.DataFrame(output)
        myID = NewDF['ID']
        myName = NewDF['Tname']
        myLen = len(NewDF)

        # 取得分析結果
        word2vec_recommend_3 = []
        word = pro_word2vec.pro_word2vec(inputname,myID,myName,myLen,model)
        for a in word:
            sql = """select Tname,Address 
                    from Attraction
                    where ID = '%s'
                    ;"""%(a)
            cursor.execute(sql)
            output = cursor.fetchall()
            for b in output:
                word2vec_recommend_3.append(b['Tname'])

        #--------------------------------------------------------------------------------------------------------------------------
        # 關閉 Mysql連線
        #--------------------------------------------------------------------------------------------------------------------------
        #connection.commit()
        #cursor.close()
        #connection.close()


        #餐廳推薦
        #景點一
        point1_restaurant = resrecommand(location[0])
        #景點二
        point2_restaurant = resrecommand(location[1])
        #景點三
        point3_restaurant = resrecommand(location[2])

        if point1_restaurant =='附近暫無推薦餐廳':
            judge1 = False
        else:
            judge1 = True
        
        if point2_restaurant =='附近暫無推薦餐廳':
            judge2 = False
        else:
            judge2 = True

        if point3_restaurant =='附近暫無推薦餐廳':
            judge3 = False
        else:
            judge3 = True
            





        return render_template('Page_3.html', location=location, place1_photo=place1_photo,
        place2_photo=place2_photo, place3_photo=place3_photo,recomList1=recomList1, recomList2=recomList2,
        recomList3=recomList3,word2vec_recommend_1=word2vec_recommend_1,word2vec_recommend_2=word2vec_recommend_2,
        word2vec_recommend_3=word2vec_recommend_3, point1_restaurant=point1_restaurant, point2_restaurant=point2_restaurant,
        point3_restaurant=point3_restaurant, judge1=judge1, judge2=judge2, judge3=judge3)




#第四頁
@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':

        #將所有checkbox選中選項放到一個list
        point_add = request.form.getlist('checkbox')
        
        #所有被選中餐廳
        restaurant = request.form.getlist('restaurant')

        all_point = []
        for i in location:
            all_point.append(i)
        for i in point_add:
            if i not in all_point:
                all_point.append(i)
        
        

        info_list = []
        for i in all_point:
            sql = """select Tname,lat,lon
                    from Attraction
                    where Tname = '%s'
                    ;"""%(i)
            cursor.execute(sql)
            output = cursor.fetchall()
            info_list.append(output)
        try:
            for i in restaurant:
                sql = """select Rname,Rlat,Rlon
                        from Restaurant
                        where Rname = '%s'
                        ;"""%(i)
                cursor.execute(sql)
                output = cursor.fetchall()
                info_list.append(output)
        except:
            pass

        result = route.route(info_list)
                


        start = result[0]
        points = result[1]
        for i in result[2:-1]:
            points = points + '|' + i 
        end = result[-1]
        src="https://www.google.com/maps/embed/v1/directions?key=AIzaSyBTLhO_brJgayLcXkAJZiFrO4ZZmfnT4JY&origin={start}&waypoints={points}&destination={end}".format(start=start,points=points,end=end)

        


        return render_template('Page_4.html', location=location, point_add=point_add
        , restaurant=restaurant,all_point=all_point,result=result, src=src)


        




if __name__ == '__main__':
    app.run(debug=True)