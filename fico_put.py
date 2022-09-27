
import requests
from functools import reduce
import operator

def Get_From_Server(login, password, url):
    return requests.get(url, auth=(login, password))

def Put_on_Server(login, password, json, url):
    return requests.put(url, auth=(login, password), data=json)

#Ф-ция для получения пути (список ключей) к значению указанного ключа
#На вход подается словарь или список, нужный ключ и пустой массив, в котором будет путь
#На выходе будет или None (ничего не надено), или первый ключ пути, весь путь в обратном порядке будет в поданном списке
def get_path_on_key_json(json, key, path=[]):
    try:
        if type(json)==dict:
            keys=list(json.keys())
            for i in range(len(keys)):
                if ((type(json[keys[i]])==dict)|(type(json[keys[i]])==list)):
                    result=get_path_on_key_json(json[keys[i]], key, path)
                    if (result!=None):
                        path.append(keys[i])
                        return keys[i]
                elif (keys[i]==key):
                    path.append(keys[i])
                    #print('keys[i]', keys[i])
                    return keys[i]
        elif type(json)==list:
            for j in range(len(json)):
                result=get_path_on_key_json(json[j], key, path)
                if (result!=None):
                    #print('result!=None ', result, 'j', j)
                    path.append(j)
                    return j
                else:
                    return None
    except Exception as Error:
        print('Возникла ошибка \n', Error)
        return None

#получение значения по пути
#При использовании с ф-цией get_path_on_key_json список необходимо обратить, например *path[::-1]
def get_by_path(obj, *path):
    return reduce(operator.getitem, path, obj)

#Замена значения по пути на новое new_value
#При использовании с ф-цией get_path_on_key_json список необходимо обратить, например *path[::-1]
def put_by_path(obj, new_value, *path):
    *keys, newkey = path
    reduce(operator.getitem, keys, obj)[newkey] = new_value
    return obj

def Put_on_Server(login, password, var_to_change, val_to_change, terms_dict={}, url):
    try:
        #res=url #Для теста
        res=Get_From_Server(login, password, url)
        for i in range(len(res)):
            flag=1
            terms_keys=list(terms_dict.keys())
            #print('terms_dict:', terms_dict)
            #print('terms_dict:', terms_dict)
            for j in range(len(terms_keys)):
                #print('Условие i=', i, 'на ключ ', terms_keys[j])
                path_for_term=[]
                get_path_on_key_json(res[i], terms_keys[j], path_for_term)
                if get_by_path(res[i], *path_for_term[::-1])!=terms_dict[terms_keys[j]]:
                    #print('Не cоответствие условиям i=', i)
                    flag=0
            if flag==1:
                #print('flag==1, i=', i)
                path_for_var=[]
                get_path_on_key_json(res[i], var_to_change, path_for_var)
                put_by_path(res[i], val_to_change, *path_for_var[::-1])
        Put_on_Server(login, password, res, url)
        return 0
    except Exception as Error:
        print('Возникла ошибка \n', Error)
        return 1

#Переменные, необходимые для запуска
#Параметр, который надо изменить
var_to_change='param'
#Значение, на которое надо изменить
val_to_change='Yes'
#Условия, словарь ключи-парамеры для условия, значения-необходимое значение
terms_dict={"term_param_1": "abcde", "term_param_2":None}
#Логин пользователя, для подключения к FICO
login=''
#Пароль пользователя, для подключения к FICO
password=''

Put_on_Server(login, password, var_to_change, val_to_change, terms_dict)
