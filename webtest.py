import json
from flask import Flask, request
import difflib
import webh
import webh_2
import threading


with open('sample.json') as json_file:
    data = json.load(json_file)

title_list=[data[i]['title'] for i in range(len(data))]

target_game_name = ['asd']
a_index=0

app = Flask(__name__)
@app.route('/webhook', methods=['GET', 'POST'])

def webhook():
    global a_index
    global target_game_name
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')

    query_game_title=query_result.get('parameters').get('game_name')
   
    if query_result.get('action') == 'get_game':
        asdf=(difflib.get_close_matches(query_game_title, title_list, 1, 0.4))
        if len(asdf)==1:
            
            # e.x TEKKEN = Tekken = tekken = teken = ...
            target_game_name=asdf
            
            for i in range(len(data)):
                if (data[i]['title']== target_game_name[0]):
                    a_index = i
               
            fulfillmentText = "Found game in database: {}. Is this okay?".format(target_game_name[0])
        
        elif len(asdf)==0:
            fulfillmentText = "Nothing resembling title found in database. Input name again "

    if query_result.get('action') == 'confirmed_yes':

        fulfillmentText = "calculations ongoing (wait before input). what next?"
        
        thr = threading.Thread(target=webh.score_calc, args=(target_game_name[0],))
        thr.start()

        
    if query_result.get('action') == 'price_info':
        fulfillmentText = "Game price is:" + str(data[a_index]['price'])

    if query_result.get('action') == 'general_info':
        fulfillmentText = "Game price is: {} \n  Game dev's are: {} \n  Game genres are: {} Link for more info: {}".format(
            str(data[a_index]['price']),
            ','.join(data[a_index]['developer']),
            ','.join(data[a_index]['genre']),
            str(data[a_index]['href'])
            )

    if query_result.get('action') == 'mostsim_info':
        fulfillmentText = ', '.join(webh_2.get_10_sim(target_game_name[0]))


    return {
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
        }

if __name__ == '__main__':
    app.run()
