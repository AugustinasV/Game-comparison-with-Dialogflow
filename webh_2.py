import json

# return data[max_id]['title']
def get_most_sim(a_title):

    with open('results'+a_title+'.json') as json_file:
        data = json.load(json_file)
    
    max_id=0
    max_score=0
    for l in range(0, len(data)):
        if (data[l]['score'][0][0]>max_score and data[l]['title'] != a_title):
            max_score = data[l]['score'][0][0]
            max_id = l

    json_file.close()
    return data[max_id]['title']


# return tags_name, top_high_title
def get_genre_sim(a_title):

    with open('results'+a_title+'.json') as json_file:
        data = json.load(json_file)
        
    tags_name = ['Action', 'Indie','Adventure','Rpg', 'Shooter', 'Arcade', 'Strategy','Platformer','Combat','Fantasy'] 
    
    top_high=[]
    top_high_title=[]
    
    for kk in range(0,len(tags_name)):
        max = 0
        top_h_t=''
        for ll in range(0,len(data)):
            if data[ll]['score'][0][0]>max and data[ll]['title'] != a_title and (tags_name[kk] in data[ll]['genre']):
                max = data[ll]['score'][0][0]
                top_h_t=data[ll]['title']
            
        top_high.append(max)
        top_high_title.append(top_h_t)
    
    json_file.close()
    return tags_name, top_high_title
    
# return top_high_title
def get_10_sim(a_title):
    
    with open('results'+a_title+'.json') as json_file:
        data = json.load(json_file)
     
    top_high=[]
    top_high_title=[]

    for k in range(0,5):
        k=k
        max = 0
        top_h_t=''
        for l in range(0,len(data)):
            if data[l]['score'][0][0]>max and data[l]['title'] != a_title and (data[l]['title'] not in top_high_title):
                max = data[l]['score'][0][0]
                top_h_t=data[l]['title']
        top_high.append(max)
        top_high_title.append(top_h_t)        

    json_file.close()
    return top_high_title


        
