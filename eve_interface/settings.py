#
import os
import json

path = os.getcwd()
print path
cfg = json.loads(open(path+'/knowledgeBase.json.template').read())
print cfg

dbHost = cfg.get('dbHost')
dbPort = cfg.get('dbPort')
dbName = cfg.get('dbName')
dbUser = cfg.get('dbUser')
dbPass = cfg.get('dbPass')

#
MONGO_HOST = dbHost
MONGO_PORT = dbPort
MONGO_DBNAME = dbName
#

RESOURCE_METHODS = ['GET']
ITEM_METHODS = ['GET']

XML = False
ensure_ascii = False 
PUBLIC_METHODS = ['GET']
PUBLIC_ITEM_METHODS = ['GET']


knowledgeBase_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.

    'rankone':{
            'type':'string',
              },
    'ranktwo':{
            'type':'string',
              },
    'rankthree':{
            'type':'string',
              },
    'source':{
            'type':'string',
              },
    'index':{
            'type':'string',
              },
    'sortrankone':{
            'type':'string',
              },
    'sortranktwo':{
            'type':'string',
              },
    'sortrankthree':{
            'type':'string',
              },
    'content':{
            'type':'list',
            'schema':{
                },
            },
    'keyword':{
            'type':'dict',
            'schema':{
                },
              },
}

knowledgeBase = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'knowledgeBase',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'index',
    },
    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'pagination':False,
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema':knowledgeBase_schema
}

DOMAIN = {
    'knowledgeBase':knowledgeBase,
}   

