from django.db import connection, transaction
# For execute Raw Queries #####
def sql_select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    list = []
    i = 0
    for row in results:
        dict = {} 
        field = 0
        while True:
           try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field +1
           except IndexError as e:
                break
        i = i + 1
        list.append(dict) 
    return list



def custome_response(data,error = 0):
    dataArry = {}
    errorStr = ''
    if error:
       dataArry['status'] = False  
       if 'msg' in data:
           dataArry['msg'] =  data['msg']
           dataArry['data'] = data['data']
       else:           
        for val in data.items():
            errorStr = errorStr +'$'+ str(val[0])+':'+str(val[1][0])
        errorStr = errorStr[1:]
        dataArry['data'] = errorStr   
    else:
       dataArry['status'] = True 
       dataArry['data'] = data
       
    return dataArry