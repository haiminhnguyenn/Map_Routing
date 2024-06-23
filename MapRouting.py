
import numpy as np 
import pandas as pd 
import math 
import difflib 
import requests 
import folium 
from pprint import pprint 
from queue import PriorityQueue 

dict ={'V Hostel': 1, 'Phố Hàng Giấy': 2, 'Cà Phê Cham': 3, 'Phố Hàng Giấy giao Phố Hàng Buồm': 4, 'Cà Phê AnAn': 5, 'Nguyễn Siêu': 6, 'Đền Cố Lương': 7, 'Holiday Suites Hotel&Spa': 8, 'Taco Bar': 9, 'Cơm gà Tuyết Nhung-Phú Yên': 10, 'Bia Ba Bat': 11, 'Phố Chợ Gạo': 12, 'Pateta': 13, 'ViettinBank': 14, 'Tiệm Cắt Tóc Hà': 15, 'Valhalla grill': 16, 'Cà phê Văn': 17, 'Le Maquis': 18,
       'Phố Tạ Hiện': 19, 'Nhà Hàng Local': 20, 'Tạp hóa': 21, 'Cà phê Vui': 22, 'Tasty Time': 23, 'Sunshine Palace': 24, 'Nhà Hàng Matto': 25, 'ANZ': 26, 'K-Mart-1': 27, 'K-Mart-2': 28, 'Spa': 29, 'Old Quarter View Hanoi Hostel': 30, 'Phố Tạ Hiện Nhà Thuốc': 31, 'S cafe': 32, 'Phố Mã Mây': 33, 'Hải Xệ': 34, 'Nhà hàng bia khánh râu': 35, 'The cosy inn hanoi': 36, 'Nhà Hàng Mai Ly 63': 37, 'Quán Cô Nhàn': 38, 'Khách Sạn An': 39, 'Trường Mẫu giáo Tuổi thơ': 40, 'vintage store': 41, 'Cau man': 42, 'Cà Phê Glamour': 43, 'Tim coffee': 44, 'v hostel': 1, 'phố hàng giấy': 2, 'cà phê cham': 3, 'phố hàng giấy giao phố hàng buồm': 4, 'cà phê anan': 5, 'nguyễn siêu': 6, 'đền cố lương': 7, 'holiday suites hotel&spa': 8, 'taco bar': 9, 'cơm gà tuyết nhung-phú yên':10,
         'bia ba bat': 11, 'phố chợ gạo': 12, 'pateta': 13, 'viettinbank': 14, 'tiệm cắt tóc hà': 15, 'valhalla grill': 16, 'cà phê văn': 17, 'le maquis': 18, 'phố tạ hiện': 19, 'nhà hàng local': 20, 'tạp hóa': 21, 'cà phê vui': 22, 'tasty time': 23, 'sunshine palace': 24, 'nhà hàng matto': 25, 'anz': 26, 'k-mart-1': 27, 'k-mart-2': 28, 'spa': 29, 'old quarter view hanoi hostel': 
30, 'phố tạ hiện nhà thuốc': 31, 's cafe': 32, 'phố mã mây': 33, 'hải xệ': 34, 'nhà hàng bia khánh râu': 35, 'the cosy inn hanoi': 36, 'nhà hàng mai ly 63': 37, 'quán cô nhàn': 38, 'khách sạn an': 39, 'trường mẫu giáo tuổi thơ': 40, 'cau man': 42, 'cà phê glamour': 43, 'tim coffee': 44
} 
numNode=46
MAXC=10**10 
adj=[[] for i in range(numNode)] 
loc=[(0,0) for i in range(numNode)] 
df=None 

def initGraph(): 
    
    df=pd.read_csv('./coordinates.txt',sep=' ') 
    df.pop('Unnamed: 3') 
    for i in range(1,numNode):
        loc[i]=(df['loc0'][i-1],df['loc1'][i-1]) 
    edges=open('./edges.txt','r') 
    for line in edges.readlines(): 
        u,v=line.split() 
        adj[int(u)].append(int(v)) 



def visualizeFullGraph():
    initGraph() 
    BASE_URL = 'https://openstreetmap.org/search?format=json'
    map = folium.Map(location=[21.03498,105.85207],zoom_start=18)
    for u in range(1,numNode): 
        folium.Marker(location=loc[u],popup=str(u)).add_to(map) 
        for v in adj[u]:
            folium.PolyLine(locations=[loc[u],loc[v]],color='red',weight=3,opacity=10).add_to(map) 
    folium.ClickForLatLng().add_to(map) 
    map.show_in_browser()
            

    
        

def queryPath(source : str,sink : str): 
    initGraph() 
    source=source.lower() 
    sink=sink.lower() 
    sourceCandidates=difflib.get_close_matches(source,dict.keys()) 
    sinkCandidates=difflib.get_close_matches(sink,dict.keys()) 
    if len(sourceCandidates)==0: 
        print('Can not find the start location') 
        return 
    if len(sinkCandidates)==0: 
        print('Can not find the destination') 
        return 
    source=sourceCandidates[0]
    sink=sinkCandidates[0] 
    nodes=findBestWay(dict[source],dict[sink]) 
    if nodes[0]==-1: 
        print('No way') 
    Route(nodes) 


def Route(nodes: [int])->None: 
    BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'
    map = folium.Map(location=[21.03559,105.85234],zoom_start=18)
    for i in range(len(nodes)-1):
        folium.PolyLine(locations=[loc[nodes[i]],loc[nodes[i+1]]],color='red',weight=3,opacity=1).add_to(map)
    folium.Marker(location=loc[nodes[0]]).add_to(map) 
    folium.Marker(location=loc[nodes[len(nodes)-1]]).add_to(map) 
    map.show_in_browser() 


def findBestWay(source: int, sink: int): 
    result=[]
    d=[MAXC for i in range(numNode)]
    trace=[0 for i in range(numNode)] 
    d[source]=0 
    q=PriorityQueue() 
    q.put((math.dist(loc[source],loc[sink]),0,source)) 
    while q.empty()==False: 
        fu,du,u=q.get() 
        if du!=d[u]: 
            continue 
        for v in adj[u]: 
            #print(str(v)+' '+str(len(d)))
            if d[v]>d[u]+math.dist(loc[u],loc[v]): 
                d[v]=d[u]+math.dist(loc[u],loc[v]) 
                q.put((-d[v]-math.dist(loc[v],loc[sink]),d[v],v)) 
                trace[v]=u 
    if trace[sink]==0: 
        return [-1] 
    while trace[sink]!=0: 
        result.append(sink) 
        sink=trace[sink] 
    result.append(sink) 
    result.reverse() 
    return result 
    

#queryPath('ca phe an an','Nha hang Matto') 
#visualizeFullGraph()

        

