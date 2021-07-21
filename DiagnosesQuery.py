import json
from os import system
import logging
import pandas as pd

# create log file 
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#Let us Create an object 
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG) 

# open and read json file and load data using Python JSON module to make into list
with open('Diagnoses.json', 'r') as f:
    diagnosesData = json.loads (f.read())  

# open and read json file and load data using Python JSON module to make into list
with open('dxClassification.json', 'r') as f:
    dxClassData = json.loads (f.read()) 

# get diagnoses value from data key dictionary with .get() for Diagnoses.json
diagnosesJson = diagnosesData.get('data') 
diagnosesList = diagnosesJson.get('diagnoses') 

# get diagnoses value from data key dictionary with .get() for dxClassification.json
diagnosesClass = dxClassData.get('diagnosisClassifications')

# iterate over list to values from dictionaries like icd10 and std
classList = []
listOfClass = []
listOfLists = []
index = 0
dict_len = 0
list_len = 0

# Failed attempt 1 - no output took way too long and got Memory Error
for dic in diagnosesClass:
    classList.append(dic)
    dictItem = classList[index] # get each dict from JSON and parse to a list
    # while dict_len < len(dictItem): # get length of JSON and reiterate over it
    for v in dictItem.values(): # get values in dict
        if type(v) is list: # if list iterate 
            while dict_len < len(v): # iterate through list with len() of list
                for dict_item in v: # get items in list v
                    item = dict_item.values() # get values of dict items in list v 
                    if type(item) is dict: # if the values are dict get values again
                        print(item.values())
                        listOfClass.append(item.values())
                    else:
                        listOfClass.append(item)
                list_len += 1
        else: # if not list add value to listOfClass
            listOfClass.append(v)
        #dict_len += 1

    listOfLists.append(listOfClass)
    index += 1

#print(listOfLists[0])

# Failed attempt 2 - recursion was adding all items into single list instead of separate lists
for dic in diagnosesClass:
    classList.append(dic) # -> get single dictionary from JSON and parse them into a list
    dictItem = classList[index]
    while dict_len < len(dictItem):
        for val in dictItem.values():
            if type(val) is list: # -> gets values with lists of dict
                for dictItem in val: # -> gets dict
                    for value in dictItem.values():
                        if type(value) is dict:
                            for item in value.values(): # -> gets values in dict
                                listOfClass.append(item)
                        else:
                            listOfClass.append(value)
            else:
                listOfClass.append(val)
    logger.debug('f{listOfClass[index]}')    
    dict_len += 1
    listOfLists.append(listOfClass[index])
    index += 1

# converts list diagnosesData into json string
jsonData = json.dumps (diagnosesClass) # -> <class 'str'>

# read json into dataframe object
dfJson = pd.read_json (jsonData) # -> <class 'pandas.core.frame.DataFrame'> dataframe formed by pandas



# save dataframe object into csv
# dfJson.to_csv('Diagnosis Classification.csv', index=False)
# print('JSON file converted into csv file')
      
