import urllib, json, requests

file = open("dests.txt", encoding='UTF-8')
file = file.read()
file = file.splitlines()
api_s='api here '

#Distance and duration from Tel Aviv
url_distance = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
from_TLV_to_x = dict()
distance_TLV = list()
i=0
for x in file:
    from_TLV_to_x['origins']='תל אביב'
    from_TLV_to_x['destinations'] = x
    from_TLV_to_x['key'] = api_s
    try:
        url = url_distance + urllib.parse.urlencode(from_TLV_to_x)
        distance_TLV.append(dict())
        results=requests.get(url)
        if results.status_code==200: 
            try:
                distance_TLV[i][x]=results.json()
                i=i+1
            except:
                print('json false')
        else:
            print("HTTP error")
    except:
        print('request false')
        
        
distance=dict()
duration=dict()
j=0
for x in file:
    distance[x]=distance_TLV[j][x]['rows'][0]['elements'][0]['distance']['text']
    duration[x]=distance_TLV[j][x]['rows'][0]['elements'][0]['duration']['text']
    j=j+1


#Latitude and longitude
loc=dict()
location=dict()
for address in file:
    try:
        url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address, api_s)
        response=requests.get(url)
        if not response.status_code==200:
            print("HTTP error")
        else:
            try:
               loc[address]=response.json()
               location[address]=loc[address]['results'][0]['geometry']['location']
            except:
                print('json false')
    except:
        print('requests false')


#Create a dictionary of all the information
all_info=list()
k=0
for x in file:
    all_info.append(dict())
    all_info[k][x]=dict()
    all_info[k][x]['lon_lat']=location[x]
    all_info[k][x]['distance_from_TLV']=distance[x]
    all_info[k][x]['duration_from_TLV']=duration[x]
    k=k+1
    
#Printing the information
n=0
for x in file:
    print('The distance from '+x+' to Tel-Aviv is: ' +all_info[n][x]['distance_from_TLV'])
    print("The duration from "+x+' to Tel-Aviv is: '+all_info[n][x]['duration_from_TLV'])
    print('Latitude of '+x+' is: '+str(all_info[n][x]['lon_lat']['lat']) )
    print('longitude of '+x+ ' is: '+str(all_info[n][x]['lon_lat']['lng']))
    print(' ')
    n=n+1

#Finding the 3 places furthest from Tel Aviv
three_place=dict()
three_place[1]=str(0)
one=str(0)
two=str(0)
three=str(0)
i=0
for x in file:
    if all_info[i][x]['distance_from_TLV']>one:
        three=two
        two=one
        one=all_info[i][x]['distance_from_TLV']
        y=three_place[1]
        three_place[1]=x
        three_place[2]=y    
    if all_info[i][x]['distance_from_TLV']>two and all_info[i][x]['distance_from_TLV']<one:
        three=two
        two=all_info[i][x]['distance_from_TLV']
        y=three_place[2]
        three_place[2]=x
        three_place[3]=y
    if all_info[i][x]['distance_from_TLV']>three and all_info[i][x]['distance_from_TLV']<two:
        three=all_info[i][x]['distance_from_TLV']
        three_place[3]=x
    i+=1
    
