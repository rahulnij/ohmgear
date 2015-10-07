#------------------------------------- Default json structure which will insert into database ---------------------#
#------------------------------------------------------------------------------------------------------------------#

BUSINESS_CARD_DATA_TYPE = {
    "name": "BUSINESS CARD",
    "properties":{
            "side_first":{
                    
                    "type": "object",
                    "properties":{
                            "card_name": {
                                        "type": "string"
                                   },
                            "personal_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string"},
                                                       "nick_name":{"type": "string"}
                                               },
                                "required":["name","nick_name"]               
                                },
                            "organization_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "company":{"type": "string"},
                                                       "title":{"type": "string"}
                                               },
                                "required":["company","title"]               
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "string"},
                                                       "email":{"type": "string"},
                                                       "skype_id":{"type": "string"},
                                                       "address":{"type": "string"}
                                               },
                                 "required":["phone","email","skype_id","address"]               
                                }
                    }, 
                    "required":["personal_info","organization_info","contact_info"]
            },    
            "side_second":{                    
                    
                    "type": "object",
                    "properties":{
                            "card_name": {
                                        "type": "string"
                                   },
                            "personal_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string"},
                                                       "nick_name":{"type": "string"}
                                               },
                                "required":["name","nick_name"]               
                                },
                            "organization_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "company":{"type": "string"},
                                                       "title":{"type": "string"}
                                               },
                                "required":["company","title"]               
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "string"},
                                                       "email":{"type": "string"},
                                                       "skype_id":{"type": "string"},
                                                       "address":{"type": "string"}
                                               },
                                 "required":["phone","email","skype_id","address"]               
                                }
                    }, 
                    "required":["personal_info","organization_info","contact_info"]
            }, 
    
  },
"required": ["side_first","side_second"]
}

BUSINESS_CARD = {

    "side_first":{
            "language":"",
            "card_name":"",
            "personal_info":{
                               "name":"",
                               "nick_name":""
                            },
            "organization_info":{
                                 "company":"",
                                 "title":""
                                },
            "contact_info":{
                             "phone":"",
                             "email":"",
                             "skype_id":"",
                             "address":"",                            
                           },
            "fields":{
                          "static_fields":{
                                        "tag_line":"",
                                        "birthday":"",
                                        "social_profile":"",
                                        "instant_messaging":""
                                   },
                          "dynamic_fields":[{"text":"value"},{"text":"value"}]
                                     
                     }                            
    },    
    "side_second":{
            "language":"",
            "card_name":"",
            "personal_info":{
                               "name":"",
                               "nick_name":""
                            },
            "organization_info":{
                                 "company":"",
                                 "title":""
                                },
            "contact_info":{
                             "phone":"",
                             "email":"",
                             "skype_id":"",
                             "address":"",                                                          
                           },
            "fields":{
                          "static_fields":{
                                        "tag_line":"",
                                        "birthday":"",
                                        "social_profile":"",
                                        "instant_messaging":""
                                   },
                          "dynamic_fields":[{"text":"value"},{"text":"value"}]
                                     
                     }                           
    }     

}

