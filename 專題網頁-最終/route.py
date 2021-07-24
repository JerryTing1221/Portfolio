import itertools 
import math

def route(info_list):
          
    info_list = info_list
          
    comb = itertools.permutations(info_list)
    comb_info = []
    for x in comb:
        comb_info.append(x)
      
          
    dis_dic = {}
    total_trname = []
    for i in range(len(comb_info)):
        trname = []
        dis_list = []
        for n in range(len(comb_info[0])):

            if 'Tname' in comb_info[i][n][0].keys():
                    trname.append(comb_info[i][n][0]['Tname']) 
                    lat1 = comb_info[i][n][0]['lat']
                    lon1 = comb_info[i][n][0]['lon']
            if 'Rname' in comb_info[i][n][0].keys():
                    trname.append(comb_info[i][n][0]['Rname'])
                    lat1 = comb_info[i][n][0]['Rlat']
                    lon1 = comb_info[i][n][0]['Rlon']
            try:
                if 'Tname' in comb_info[i][n+1][0].keys():    
                    lat2 = comb_info[i][n+1][0]['lat']
                    lon2 = comb_info[i][n+1][0]['lon']

                if 'Rname' in comb_info[i][n+1][0].keys():
                    lat2 = comb_info[i][n+1][0]['Rlat']
                    lon2 = comb_info[i][n+1][0]['Rlon']
            except:
                pass

            Dis=math.sqrt((lon1-lon2)**2+(lat1-lat2)**2)
            dis_list.append(Dis)

            sum_dis = sum(dis_list)

        total_trname.append(trname)
        dis_dic.update({i:sum_dis})

    final_dis = sorted(dis_dic.items(),key = lambda x:x[1])

    return total_trname[final_dis[0][0]]