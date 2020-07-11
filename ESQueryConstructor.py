import json
import requests


class BooleanQueryConstructor:
    def __init__(self):
        self.json_dict = {'query':{'bool':{'filter':[],'must':[],'must_not':[],'should':[]}},'size':10}
        
    # 距离单位为m
    
    def size(self,n):
        self.json_dict['size']=n
        return self
    
    def geo_distance(self,column_name,lon,lat,distance):
        geo_distance_dict = {
            'geo_distance' : {
                'distance' : '%s'%distance,
                column_name : {
                    'lat' : lat,
                    'lon' : lon
                }
            }
        }
        self.json_dict['query']['bool']['filter'].append(geo_distance_dict)
        return self
    
    def must_match(self,column_name,text_to_search):
        must_match_dict = {
            'match' : {
                column_name : text_to_search,
            }
        }
        self.json_dict['query']['bool']['must'].append(must_match_dict)
        return self
    
    def must_term(self,column_name,text_to_search):
        must_term_dict = {
            'term' : {
                column_name : text_to_search,
            }
        }
        self.json_dict['query']['bool']['must'].append(must_term_dict)
        return self
    
    def should_match(self,column_name,text_to_search):
        must_match_dict = {
            'match' : {
                column_name : text_to_search,
            }
        }
        self.json_dict['query']['bool']['should'].append(must_match_dict)
        return self
    
    def must_not_term(self,column_name,text_to_search):
        must_not_term_dict = {
            'term' : {
                column_name : text_to_search,
            }
        }
        self.json_dict['query']['bool']['must_not'].append(must_not_term_dict)
        return self
    
    
    def to_json(self):
        for condition in ['filter','must','must_not','should']:
            if len(self.json_dict['query']['bool'][condition])==0:
                self.json_dict['query']['bool'].pop(condition)
        return json.dumps(self.json_dict,ensure_ascii=False).encode('utf-8')
    
base_url = 'http://a.com:8888'
username = 'user'
password = 'pwd'
headers = {
        'Content-Type': 'application/json',
}


index_name = 'index'
type_name = 'type'

constructor = BooleanQueryConstructor()
body = constructor.geo_distance('geo_point',110.0,30.0,1000).must_match('name','').must_not_term('level','high').size(10).to_json()

r = requests.get('/'.join([base_url,index_name,type_name,'_search?pretty']), auth=(username, password), data=body, headers=headers,timeout=2)
hits = [i['_source'] for i in r.json()['hits']['hits']]
