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
                                "type": "array",
                                "items":[]              
                                },
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "array","items":[],"minItems": 0,"maxItems": 10,"additionalItems": True},
                                                       "email":{"type": "array","items":[],"minItems": 0,"maxItems": 10,"additionalItems": True}
                                                           
                                               }              
                                },
                             "basic_info":   
                               { 
                                "type": "array",
                                "items": {
                                          "type" : "object",
                                          "properties" : {
                                           "indexPos": { "type": "integer" },
		                           "placeHolder": { "type" : "string" },
                                           "isUpper":{ "type": "integer" },
                                           "keyName":{ "type" : "string","enum": ["FirstName","LastName","CompName","CardName","DEPTName","NickName"] },
                                           "value":{ "type" : "string"}    
                                          }
                                         },
                                "minItems": 1,
                                "maxItems": 10
                                },                                 
                    }
            },
            "side_second":{
                    
                    "type": "object",
                    "properties":{ 
                            "contact_info":
                               { 
                                "type": "object",
                                "properties": {
                                                       "phone":{"type": "array","items":[],"minItems": 0,"maxItems": 10,"additionalItems": True},
                                                       "email":{"type": "array","items":[],"minItems": 0,"maxItems": 10,"additionalItems": True}
                                          
                                                           
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

