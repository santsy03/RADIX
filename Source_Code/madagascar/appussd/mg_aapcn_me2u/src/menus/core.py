from prepaid import menu

def get_root_menu():
    ''' retrieves the root menu'''
    return (((menu['levels'][0])['menus'])[0])['id']

def create_menus():
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

class Menu(object):

    def __init__(self,definition):
        self.id = definition['id']
        self.leaf = definition['leaf']
        self.title = definition['title']
        self.footer = definition['footer']
        self.entries = definition['entries']
        self.parameter = definition['parameter']
        self.service = definition['service']
        self.package = definition['package']
        self.response = definition['response']
        self.checkpoint = definition['checkpoint']
        self.type = definition['type']
        self.definition = definition

    def __str__(self):
        return str(self.definition)

    def fetch_content(self,source,resources):
        from urllib2 import urlopen,Request
        from string import Template
        url  = (Template(source)).safe_substitute(resources['parameters'])
        print url
        try:
            response = (urlopen(Request(url), timeout=3))
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
            resources['action'] = 'end'
            return resources
        except Exception,e:
            print 'error',str(e)
            resources['ussdResponseString'] = 'system is currently unavailable. please try again later.'
            resources['action'] = 'end'
            return resources
    
    def provision_service(self,resources):
        from urllib2 import urlopen,Request
        from urllib import urlencode
        args = urlencode(resources['parameters'])
        try:
            url = 'http://127.0.0.1:9095/provision?%s' %args
            response = urlopen(Request(url),timeout=7)
        except Exception,e:
            error = 'operation:submitProvision,status:error,desc:%s,params:%s' %(str(e),str(resources['parameters']),)
            print error
        else:
            success = 'operation:submitProvision,status:success,desc:%s,params:%s' %(str(resources['parameters']),)
            print success


    def start(self,resources):
        from string import Template
        language = resources['language']
        resources['action'] = 'request'
        if self.leaf and (resources['parameters'])['service'] and (resources['parameters'])['package']:
            self.provision_service(resources)
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
                (resources['parameters'])['sessionIdInternal'] = self.generate_session_id()
            txt = ''
            if self.title:
                txt += '%s\n' %(self.title,)
            for entry in self.entries:
                if entry['type']=='static':
                    txt+='%s\n' %(Template(entry[language]).safe_substitute(resources['parameters']))
                    resources['action'] = 'request'
                    resources['ussdResponseString'] = txt
                elif entry['type'] == 'dynamic':
                    print 'fetching dynamic content'
                    resources = self.fetch_content(entry['source'],resources)
            if self.footer:
                resources['ussdResponseString'] += '%s' %(str(self.footer),)
        resources = self.set_navigation(resources)
        return resources

    def set_navigation(self,resources):
        navigation = resources['navigation']
        if len(navigation) == 0:
            navigation.append(self.id)
            resources['navigation'] = navigation
        elif str(navigation[(len(navigation)-1)]) != str(self.id):
            navigation.append(str(self.id).strip())
            resources['navigation'] = navigation
        return resources

    def get_previous_menu(self,resources):
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

    
    def process_action(self,resources):
        request = resources['ussdRequestString']
        currentMenuId = resources['currentMenuId']
        (resources['parameters'])['request'] = request
        if str(request).strip() == '#':
                resources = self.get_previous_menu(resources)
        else:
            if self.parameter:
                (resources['parameters'])[self.parameter] = request
            if self.response == 'key':
                for entry in self.entries:
                    if request == entry['key']:
                        currentMenuId = entry['nextMenuId']
                        break
            elif self.response == 'any':
                currentMenuId = (self.entries[0])['nextMenuId']
            resources['currentMenuId'] = currentMenuId
        return resources

    def generate_session_id(self):
        from time import time
        from random import randint
        sessionId = '%d%d' %(int(time()),int(randint(0,2000)))
        return sessionId


if __name__ == '__main__':
    pass
    #print get_root_menu()
    #menus =  create_menus()
    #print menus
    #for k,v in menus.iteritems():
    #    print v,'\n'
    #definition = {'checkpoint': False, 'entries': [{'nextMenuId': '1-0-4-1', 'service': False, 'key': '1', 'package': False, 'txt-2': 'Dear customer your request for this offer is being processed. You will receive a confirmation message shortly.', 'txt-1': 'Dear customer your request for this offer is being processed. You will receive a confirmation message shortly.', 'type': 'static', 'response': 'key', 'name': False}], 'leaf': True, 'id': '1-0-4-1', 'title': False,'service':False,'package':False,'response':'key','footer':False,'parameter':False}
    #menu = Menu(definition)
    
