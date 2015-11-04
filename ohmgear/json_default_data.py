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
                            "basic_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string","blank": True},
                                                       "nick_name":{"type": "string","blank": True},
                                                       "card_name": {"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "language":{"type": "string","blank": True,"minLength": 2, "maxLength": 2},                                                       
                                                       "title":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "company_name":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }              
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "array","items":[{}],"blank": True},
                                                       "email":{"type": "array","items":[{}],"blank": True},
                                                       "message":{"type": "array","items":[{}],"blank": True},
                                                       "website":{"type": "array","items":[{}],"blank": True},
                                                       "social_network":{"type": "array","items":[{}],"blank": True},
                                                       "address":{
                                                               "type": "object",
                                                               "properties": {
                                                                "work":{
                                                                  "type": "object",
                                                                  "properties": {
                                                                     "city":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "country":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "state":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "street":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "zipCode":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                                                  }
                                                                }   ,
                                                               "phone":{
                                                                  "type": "object",
                                                                  "properties": {
                                                                     "city":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "country":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "state":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "street":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "zipCode":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}                                                                 
                                                                  
                                                                  }                                                                  
                                                                
                                                                
                                                                }
                                                               
                                                               }
                                                       
                                                       }
                                                           
                                               }              
                                }
                    }
            },
            "side_second":{
                    
                    "type": "object",
                    "properties":{        
                            "basic_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "name":{"type": "string","blank": True},
                                                       "nick_name":{"type": "string","blank": True},
                                                       "card_name": {"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "language":{"type": "string","blank": True,"minLength": 2, "maxLength": 2},                                                       
                                                       "title":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                       "company_name":{"type": "string","blank": True,"minLength": 0, "maxLength": 50}
                                               }              
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "array","items":[{}],"blank": True},
                                                       "email":{"type": "array","items":[{}],"blank": True},
                                                       "message":{"type": "array","items":[{}],"blank": True},
                                                       "website":{"type": "array","items":[{}],"blank": True},
                                                       "social_network":{"type": "array","items":[{}],"blank": True},
                                                       "address":{
                                                               "type": "object",
                                                               "properties": {
                                                                "work":{
                                                                  "type": "object",
                                                                  "properties": {
                                                                     "city":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "country":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "state":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "street":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "zipCode":{"type": "string","blank": True,"minLength": 0, "maxLength": 10}
                                                                  }
                                                                }   ,
                                                               "phone":{
                                                                  "type": "object",
                                                                  "properties": {
                                                                     "city":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "country":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "state":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "street":{"type": "string","blank": True,"minLength": 0, "maxLength": 50},
                                                                     "zipCode":{"type": "string","blank": True,"minLength": 0, "maxLength": 10}                                                                 
                                                                  
                                                                  }                                                                  
                                                                
                                                                
                                                                }
                                                               
                                                               }
                                                       
                                                       }
                                                           
                                               }              
                                }
                    }
            }            
            
    
  }
}

BUSINESS_CARD = {

    "side_first":{
            "basic_info":{
                               "name":"",
                               "nick_name":"",                               
                               "language":"en",
                               "card_name":"",
                               "title":"",
                               "company_name":""
                            },
            "contact_info":{
                                 "phone":[{}],
                                 "email":[{}],
                                 "message":[{}],
                                 "website":[{}], 
                                 "social_network":[{}],
                                   "address":{
                                        "work":{
                                           "city":"",
                                           "country":"",
                                           "state":"",
                                           "street":"",
                                           "zipCode":""
                                        },
                                        "phone":{
                                           "city":"",
                                           "country":"",
                                           "state":"",
                                           "street":"",
                                           "zipCode":""
                                        }                                   
                                   }
                                   
                            }         
    },    
    "side_second":{
            "basic_info":{
                               "name":"",
                               "nick_name":"",                               
                               "language":"en",
                               "card_name":"",
                               "title":"",
                               "company_name":""
                            },
            "contact_info":{
                                 "phone":[{}],
                                 "email":[{}],
                                 "message":[{}],
                                 "website":[{}], 
                                 "social_network":[{}],
                                 "address":{
                                        "work":{
                                           "city":"",
                                           "country":"",
                                           "state":"",
                                           "street":"",
                                           "zipCode":""
                                        },
                                        "phone":{
                                           "city":"",
                                           "country":"",
                                           "state":"",
                                           "street":"",
                                           "zipCode":""
                                        }                                   
                                   }
                                   
                            }         
    }
}

