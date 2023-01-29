import json
from json import JSONEncoder
from transformers import AutoTokenizer

import torch
import numpy

from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel

model_name = "distilbert-base-uncased"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
n = 512

with open('sample.json') as json_file:
    data = json.load(json_file)


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

# ==================================================================
#           convert long str to 512

def strToTensor(b):
    b_tensor = tokenizer.encode(b,return_tensors="pt").to()
    b_output=model(b_tensor)
    b_combine = torch.mean(b_output.last_hidden_state, axis = 1)
    return b_combine

def tensorMean(a): # a = tensor_list
    a_temp=[]
    if len(a)%2!=0 and len(a)>1:
        a_temp.append(torch.add(a[-1]*0.5 , a[-2]*0.5))
        for i in range(0, len(a)-1, 2):
            a_temp.append(torch.add(a[i]*0.5 , a[i+1]*0.5))
        a=a_temp
        tensorMean(a)

    elif len(a)%2!=0 and len(a)>1: 
        for i in range(0, len(a), 2):
            a_temp.append(torch.add(a[i]*0.5 , a[i+1]*0.5))
        a=a_temp
        tensorMean(a)
    return a

def strToMean(c): # long string c
    str_list = []
    tensor_list = []
    for i in range(0, len(c), n):
        str_list.append(c[i:i+n])
    for j in str_list[0:-2]:
        tensor_list.append(strToTensor(j))
    # len(last_substring)!= 512 ====> mean with dif weight
    tensor_list.append(torch.add(strToTensor(str_list[-1])* (len(str_list[-1])/512), strToTensor(str_list[-2])* (1-(len(str_list[-1])/512))))
    return tensorMean(tensor_list)[0]        

# ==================================================================


def score_calc(a_title):

    for i in range(len(data)):
        if (data[i]['title']== a_title):
            
            a_tensor = tokenizer.encode(data[i]['desc'], return_tensors="pt").to()

            if (list(a_tensor.shape)[1] > 512):
                a_combine=strToMean(data[i]['desc'])
            else:
                a_combine=strToTensor(data[i]['desc'])

    for j in range(len(data)):
        b_tensor = tokenizer.encode(data[j]['desc'], return_tensors="pt").to()

        if (list(b_tensor.shape)[1] > 512):
            b_combine=strToMean(data[j]['desc'])
            data[j]['score'] = cosine_similarity(a_combine.cpu().detach().numpy(), b_combine.cpu().detach().numpy())

        else:
            b_combine=strToTensor(data[j]['desc'])
            data[j]['score'] = cosine_similarity(a_combine.cpu().detach().numpy(), b_combine.cpu().detach().numpy())

    # ==================================================================

    with open('results'+a_title+'.json','w') as outfile:
        json.dump(data, outfile, cls=NumpyArrayEncoder)





