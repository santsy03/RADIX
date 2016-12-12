
def getRootMenu():
    ''' retrieves the root menu'''
    #return (((menu['levels'][0])['menus'])[0])['id']
    return '1-0-0-1'

def createMenusOld():
    from prepaid import menu
    menus = {}
    for level in menu['levels']:
        for k,v in level.iteritems():
            try:
                for item in v:
                    try:
                        menus[item['id']] = Menu(item)
                        print 'passed ...',item['id']
                    except Exception,e:
                        print 'failed ...',item['id']
            except Exception,e:
                pass
    return menus

def getFlow():
    from sample_data import sample_flow
    return sample_flow

def createMenus():
    menus = {}
    flows = getFlow()
    for flowId,flowDefinitions in flows.iteritems():
        #pprint(flowDefinitions)
        for flowId,flowDefinition in flowDefinitions.iteritems():
            #pprint(flowDefinition)
            for levelId,levelValue in flowDefinition['levels'].iteritems():
                #pprint(levelValue)
                for menuId,menuDefinition in levelValue['menus'].iteritems():
                    #pprint(menuDefinition)
                    menus[str(menuDefinition['id']).strip()] = Menu(menuDefinition)
    return menus


class Menu(object):

    def __init__(self,definition):
        #print definition
        self.id = definition['id']
        self.leaf = definition['leaf']
        self.title = definition['title']
        self.footer = definition['footer']
        try:
          self.entries = definition['entries']
        except Exception,e:
          self.entries = []
        self.parameter = definition['parameter']
        self.service = definition['services']
        self.package = definition['package']
        try:
            self.response = definition['response']
        except Exception:
            self.response = 'any'
        self.checkpoint = definition['checkpoint']
        self.type = definition['type']
        self.definition = definition

    def __str__(self):
        return str(self.definition)

    def fetchContent(self,source,resources):
        from urllib2 import urlopen,Request
        #from ussd.services.common.secure.secure import decrypt
        import re
        #from ussd.configs.core import crbt
	from string import Template
        url  = (Template(source)).safe_substitute(resources['parameters'])
        if re.match(r'^(.*)encuser(.*)encpass(.*)',url):
            user = decrypt(crbt['user'])
            password = decrypt(crbt['password'])
            url = url.replace('encuser',user).replace('encpass',password)
	    print 'SENDING CRBT REQUEST'
        try:
            url = url.replace(' ','')
            response = (urlopen(Request(url),timeout = 10))
            try:
                resources['action'] = response.headers['action']
            except Exception,e:
                pass
            try:
                (resources['parameters'])['service'] = response.headers['service']
            except Exception,e:
                pass
            try:
                (resources['parameters'])['package'] = response.headers['package']
            except Exception,e:
                pass
            resources['ussdResponseString'] = response.read()
            resources['action'] = 'request'
            return resources
        except Exception,e:
            print 'error',str(e)
            resources['ussdResponseString'] = 'system is currently unavailable. please try again later.'
            resources['action'] = 'end'
            return resources
    
    def provisionService(self,resources):
        from urllib2 import urlopen,Request
        from urllib import urlencode
        args = urlencode(resources['parameters'])
        try:
            url = 'http://127.0.0.1:9097/provision?%s' %args
            response = urlopen(Request(url),timeout=10)
        except Exception,e:
            error = 'operation:submitProvision,status:error,desc:%s,params:%s' %(str(e),str(resources['parameters']),)
            print error
        else:
            success = 'operation:submitProvision,status:success,desc:%s,params:%s' %(str(resources['parameters']),)
            print success


    def start(self,resources):
        #print resources['parameters']
        from string import Template
        language = resources['language']
        if language == 'txt-1':
            language='txt1'
        elif language == 'txt-2':
            language='txt2'
        else:
            language='txt3'
       
        resources['action'] = 'request'
        if self.leaf and (resources['parameters'])['service'] and (resources['parameters'])['package']:
            self.provisionService(resources)
            resources['ussdResponseString'] = 'Your request is being processed. You will receive a confirmation message shortly.'
            resources['action'] = 'end'
        else:
            if self.service:
                if self.service != ((resources['parameters'])['service']):
                    (resources['parameters'])['package'] = None
                (resources['parameters'])['service'] = self.service
            if self.package:
                (resources['parameters'])['package'] = self.package
            if self.type == 'flares':
                (resources['parameters'])['sessionIdInternal'] = self.generateSessionId()
            txt = ''
            if self.title:
                txt += '%s\n' %(self.title,)
            entriesIterator = self.entries.iteritems()
            #length = entriesIterator.__length_hint__()
            indexes = []
            #print self.entries
            for k,v in self.entries.iteritems():
                indexes.append(int(k))
            indexes.sort()    
            for i in indexes:
                try:
                    if self.entries[str(i)]['type']=='static':
                        try:
                            txt+='%s\n' %(Template((self.entries[str(i)])[language]).safe_substitute(resources['parameters']))
                            if self.leaf == 0:
                                resources['action'] = 'request'
                            else:
                                resources['action'] = 'end'
                            resources['ussdResponseString'] = txt
                        except Exception,e:
                            error = 'operation: compiling menu txt,error:%s' %(str(e),)
                            print error
                    elif self.entries[str(i)]['type'] == 'dynamic' or self.entries[str(i)]['type'] == 'loop':
                        resources = self.fetchContent((self.entries[str(i)])['source'],resources)
			if self.leaf == 0:
                            resources['action'] = 'request'
                        else:
                            resources['action'] = 'end'
                except KeyError,e:
                    pass

            if self.footer:
                resources['ussdResponseString'] += '%s' %(str(self.footer),)
        resources = self.setNavigation(resources)
        return resources

    def setNavigation(self,resources):
        navigation = resources['navigation']
        if len(navigation) == 0:
            navigation.append(self.id)
            resources['navigation'] = navigation
        elif str(navigation[(len(navigation)-1)]) != str(self.id):
            navigation.append(str(self.id).strip())
            resources['navigation'] = navigation
        return resources

    def getPreviousMenu(self,resources):
        navigation = resources['navigation']
        if len(navigation)>0:
            if len(navigation)-2 >= 0:
                resources['currentMenuId'] = str(navigation[len(navigation)-2]).strip()
            else:
                resources['currentMenuId'] = resources['root']
            resources['navigation'].pop()
            return resources
        else:
            resources['currentMenuId'] = resources['root']
            return resources

    
    def processAction(self,resources):
        request = resources['ussdRequestString']
        currentMenuId = resources['currentMenuId']
        (resources['parameters'])['request'] = request
        if str(request).strip() == '#':
                resources = self.getPreviousMenu(resources)
        else:
            if self.parameter:
                (resources['parameters'])[self.parameter] = request
            if self.response == 'key':
                for key,entry in self.entries.iteritems():
                    if (entry['type'].strip()).lower() == 'loop':
                        currentMenuId = self.id
                        break
                    if str(request).strip() == str(entry['key']).strip():
                        currentMenuId = entry['nextmenuid']
                        break
            elif self.response == 'any':
                currentMenuId = (self.entries['1'])['nextmenuid']
            resources['currentMenuId'] = currentMenuId
        return resources

    def generateSessionId(self):
        from time import time
        from random import randint
        sessionId = '%d%d' %(int(time()),int(randint(0,2000)))
        return sessionId


if __name__ == '__main__':
    print getRootMenu()
    menus =  createMenus()
    print menus
    #for k,v in menus.iteritems():
    #    print v,'\n'
    #definition = {'checkpoint': False, 'entries': [{'nextmenuid': '1-0-4-1', 'service': False, 'key': '1', 'package': False, 'txt-2': 'Dear customer your request for this offer is being processed. You will receive a confirmation message shortly.', 'txt-1': 'Dear customer your request for this offer is being processed. You will receive a confirmation message shortly.', 'type': 'static', 'response': 'key', 'name': False}], 'leaf': True, 'id': '1-0-4-1', 'title': False,'service':False,'package':False,'response':'key','footer':False,'parameter':False}
    #menu = Menu(definition)
    
