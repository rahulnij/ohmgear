#------------------------------------- Default json structure which will insert into database ---------------------#
#------------------------------------------------------------------------------------------------------------------#
# validation for json schema:jsonschema
## validation for json data: validictory
#BUSINESS_CARD_SCHEMA_VALIDATION = {
#    "name": "BUSINESS CARD",
#    "properties":{
#            "side_first":{
#                    
#                    "type": "object",
#                    "properties":{
#                            "card_name": {
#                                        "type": "string"
#                                   },
#                            "language":{"type": "string"},       
#                            "personal_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "name":{"type": "string"},
#                                                       "nick_name":{"type": "string"}
#                                               }               
#                                },
#                            "organization_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "company":{"type": "string"},
#                                                       "title":{"type": "string"}
#                                               },
#                                "required":["company","title"]               
#                                },
#                            "contact_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "phone":{"type": "string"},
#                                                       "email":{"type": "string","format": "email"},
#                                                       "skype_id":{"type": "string"},
#                                                       "address":{"type": "string"}
#                                               },
#                                 "required":["phone","skype_id","address"]               
#                                }
#                    }, 
#                    "required":["personal_info","organization_info","contact_info"]
#            },    
#            "side_second":{                    
#                    
#                    "type": "object",
#                    "properties":{
#                            "card_name": {
#                                        "type": "string"
#                                   },
#                            "language":{"type": "string"},         
#                            "personal_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "name":{"type": "string"},
#                                                       "nick_name":{"type": "string"}
#                                               },              
#                                },
#                            "organization_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "company":{"type": "string"},
#                                                       "title":{"type": "string"}
#                                               },
#                                "required":["company","title"]               
#                                },
#                            "contact_info":
#                               { 
#                                "type": "object",
#                                "properties": {
#                                                       "phone":{"type": "string"},
#                                                       "email":{"type": "string","format": "email"},
#                                                       "skype_id":{"type": "string"},
#                                                       "address":{"type": "string"}
#                                               },
#                                 "required":["phone","email","skype_id","address"]               
#                                }
#                    }, 
#                    "required":["personal_info","organization_info","contact_info"]
#            }, 
#    
#  },
#"required": ["side_first","side_second"]
#}

BUSINESS_CARD_DATA_VALIDATION = {
    "name": "BUSINESS CARD",
    "properties":{
            "side_first":{
                    
                    "type": "object",
                    "properties":{
                            "card_name": {
                                        "type": "string","blank": True,"minLength": 0, "maxLength": 50
                                   },
                            "language":{"type": "string","blank": True,"minLength": 2, "maxLength": 2},         
                            "personal_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string","blank": True},
                                                       "nick_name":{"type": "string","blank": True}
                                               }              
                                },
                            "organization_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "company":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "title":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }
                                               
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "string","pattern": "^$|^[0-9-]+$","blank": True},
                                                       "email":{"type": "string","pattern": "^$|^[A-Za-z0-9][A-Za-z0-9\.]*@([A-Za-z0-9]+\.)+[A-Za-z0-9]+$","blank": True},
                                                       "skype_id":{"type": "string","blank": True},
                                                       "address":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }              
                                }
                    }
            },    
            "side_second":{                    
                    
                    "type": "object",
                    "properties":{
                            "card_name": {
                                        "type": "string","blank": True,"minLength": 0, "maxLength": 50
                                   },
                            "language":{"type": "string","blank": True,"minLength": 2, "maxLength": 2},         
                            "personal_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string","blank": True},
                                                       "nick_name":{"type": "string","blank": True}
                                               }              
                                },
                            "organization_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "company":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "title":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }
                                               
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "string","pattern": "^$|^[0-9-]+$","blank": True},
                                                       "email":{"type": "string","pattern": "^$|^[A-Za-z0-9][A-Za-z0-9\.]*@([A-Za-z0-9]+\.)+[A-Za-z0-9]+$","blank": True},
                                                       "skype_id":{"type": "string","blank": True},
                                                       "address":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }              
                                }
                    }
            }
    
  }
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

