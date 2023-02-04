import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from joblib import dump, load
from keras.models import load_model


path="NNModel/"

encoder = load(path+'encoder.joblib')
model_a = load_model(path+"predict_model_A.h5")
model_b = load_model(path+"predict_model_B.h5")

def suggestedtower(my_progress,serie='A'):

  
  try:
    progression=np.array(my_progress).reshape(-1,1)
    new_p=encoder.transform(progression).toarray()
    
    lookback_size=5

    if serie=='B':
      lookback_size=3
    input_progression=np.array(new_p).reshape(1,lookback_size,len(encoder.categories_[0]))
    
    if serie=='B':
      predictions=model_b.predict(input_progression)
    else:
      
      predictions=model_a.predict(input_progression)
    
    indice = np.argmax(predictions)
    
    top=10
    
    indice_list=[]
    
    for k in range(top):
    
        index = np.argsort(np.max(predictions, axis=0))[-(k+1)]
        indice_list.append(index)
        
    top_list=[]
    
    for index in indice_list:
    
        output=[0]*len(encoder.categories_[0])
        output[index]=1
        top_list.append(output)
        
    top_list=np.array(top_list)
  
    suggested_list=encoder.inverse_transform(top_list).reshape(1,-1)[0]

  except:
    return []
  
  return suggested_list
