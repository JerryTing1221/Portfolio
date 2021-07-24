#--------------------------------------------------------------------------------------------------------------------------
# Word2vec 推薦
#--------------------------------------------------------------------------------------------------------------------------
from gensim.models import word2vec
import json

def pro_word2vec(inputname,myID,myName,myLen,model):
    
    MyID = myID
    MyName = myName
    Inputname = inputname
    MyLen = myLen
    model = model

    
    #載入訓練好的模型
    #model = word2vec.Word2Vec.load("./word2vec.model")  
    
    with open('./NewContList.json','r',encoding='utf-8') as f:
        NewContList = json.load(f) 

    JiebaList = []
    for z in  MyID:
        JiebaList.append(NewContList[int(z)])

    #取出目標景點
    TargetList = []
    for y in range(MyLen):
        if MyName[y] == Inputname:
            TargetList = JiebaList[y]
            break

    # 計算分數        
    ScoreList = []  
    for x in range(MyLen):
        if MyName[x] == Inputname:continue
        Score = Count = 0
        scoList =[]
        for c in TargetList:    
            for d in JiebaList[x]:
                try:
                    Score += model.wv.similarity(c,d)
                    Count += 1
                except:
                    pass
        scoList.append(MyID[x])
        scoList.append(Score/Count)
        ScoreList.append(scoList)
        ScoreList = sorted(ScoreList,reverse=True,key = lambda s: s[1])
    
    ResultList = []
    for e,f in ScoreList:
        ResultList.append(e)    

    return ResultList[0:5]