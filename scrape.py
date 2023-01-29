import requests 
import re
import json
from bs4 import BeautifulSoup

url = "https://store.steampowered.com/search/?tags="
tags_id = [19,492,21,122,1774,1773,9,1625,3993,1684]
tags_name = ['Action', 'Indie','Adventure','Rpg', 'Shooter', 'Arcade', 'Strategy','Platformer','Combat','Fantasy'] 

# "infinite scrool" => multiple pages loaded in one 
# 1 page = 50 items; change 'start' to n * 50

params = {
    "query": "",
    "start": 0,
    "count": 25,
    "cc": "US",
    "l": "english",
    "v": "4",
    "tag": "",
    "tagid": "",
}

# href=[]
title=[]
comp=[]


for i in range(0,len(tags_id)):

    url = "https://store.steampowered.com/search/?tags="+str(tags_id[i])
    params['tagid']=str(tags_id[i])
    params['tag']=str(tags_name[i])

    for page in range(0,1):
        params["start"] = 50 * page

        response = requests.get(url,params=params)
        website_bs = BeautifulSoup(response.content, 'html.parser')

        for it in website_bs.find_all('a', class_='search_result_row ds_collapse_flag'):

            x={'href':it.get('href'),
               'title': ((it.find('div', class_='responsive_search_name_combined')).find('div', class_='col search_name ellipsis')).find('span', class_='title').text, #ok
               'price': int(((it.find('div', class_='responsive_search_name_combined')).find('div', class_='col search_price_discount_combined responsive_secondrow')).get('data-price-final')), # ok
               'developer':[], # ok
               'genre':[], # ok
               'score':0, #ok
               'desc':""} # ok 
            comp.append(x)
    print(len(comp))
    print(tags_name[i])

    stop=[' a ',' an '," another "," any "," certain "," each "," every ",' her ',' his ',' its ',' its ',' my ',' no ',' our ',' some ',' that ',' the ',' their ',' this ']
    stop2=['\t', '\n', '\r', 'About This Game']

    for a in range(25*i, len(comp)):

        response = requests.get(comp[a]['href'],params=params)
        print(comp[a]['title'])

        website_bs = BeautifulSoup(response.content, 'html.parser')

        if website_bs.find('div',id= 'developers_list', class_='summary column') == None:
            comp[a]['developer'] = ''    
        else:
            comp[a]['developer'] = ((website_bs.find('div',id= 'developers_list', class_='summary column')).text.strip().replace('\n', '')).split(',')
        
        if website_bs.find('div',id= 'genresAndManufacturer', class_='details_block') == None:
            comp[a]['genre']= ''
        else:
            comp[a]['genre'] = ((website_bs.find('div',id= 'genresAndManufacturer', class_='details_block').find('span')).text.strip().replace('\n', '')).split(',')
            comp[a]['genre'].append(tags_name[i])

        
        if ((website_bs.find('div',id='game_area_description' ,class_='game_area_description')) == None):
            comp[a]['desc']=''
        else:
            temp = (website_bs.find('div',id='game_area_description' ,class_='game_area_description').text)
            for word in stop:
                temp=temp.replace(word, " ")
            for word2 in stop2:
                temp=re.sub(word2,"",temp)
            comp[a]['desc']=temp


with open("sample.json", "w",encoding='utf-8') as outfile:
    json.dump(comp, outfile)
