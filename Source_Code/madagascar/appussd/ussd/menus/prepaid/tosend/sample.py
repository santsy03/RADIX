from pprint import pprint
from sample_data import sample_flow
from core import Menu

flows = sample_flow
menus = []

for flowId,flowDefinitions in flows.iteritems():
    #pprint(flowDefinitions)
    for flowId,flowDefinition in flowDefinitions.iteritems():
        #pprint(flowDefinition)
        for levelId,levelValue in flowDefinition['levels'].iteritems():
            #pprint(levelValue)
            for menuId,menuDefinition in levelValue['menus'].iteritems():
                #pprint(menuDefinition)
                menus.append(Menu(menuDefinition))

for menu in  menus:
    print str(menu)


