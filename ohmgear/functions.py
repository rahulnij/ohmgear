from django.db import connection, transaction
from django.utils.six.moves.http_client import responses
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


# ---------- Work for all api response -----------------#
from django.template.response import SimpleTemplateResponse
from rest_framework.response import Response
class CustomeResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """
    
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,validate_errors=None,already_exist=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)
         
        tempData = {}       

        if status:   
           tempData['status_code'] =  status
        
        
        #-------- Condition for validate_errors ---------# 
        errorStr = ''
        if validate_errors or already_exist:
            if 'msg' in data:
              tempData['msg'] = data['msg']
            else:
                for val in data.items():
                   errorStr = errorStr +'$'+ str(val[0])+':'+str(val[1][0])
                errorStr = errorStr[1:]
                tempData['msg'] = errorStr
            if already_exist:   
               tempData['status'] = True
            else:
               tempData['status'] = False 
        else:
           tempData['data'] = data
           tempData['status'] = True
        #-------  End ----------------------------------------#        
        
        self.data = tempData
        
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type        
        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value
#------------------ End ----------------------------------#

#---------------------------- File Uploads ---------------#
def handle_uploaded_file(f,file,image_path=None):
    name, extension = file.name.rsplit('.',1)
    import uuid,os
    filename = "%s.%s" % (uuid.uuid4(), extension)
    path = image_path+filename
    try:
        destination = open(filepath, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except:
        return False
#---------------------------- End File uploads ------------#