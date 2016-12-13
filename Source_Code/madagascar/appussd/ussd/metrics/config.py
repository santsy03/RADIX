from string import Template
'''source counters'''
airTemplate = Template('application.ussd2mg.air.$package')   #missed call alert.
dataPlanBalanceCheckTemplate = Template('application.ussd2mg.modularTariff. $package : request $request') #internet proxy
dataPlanSubscriptionTemplate = Template('application.ussd2mg.modularTariff. $package : request $request : shortcode $key')
servicePlanSubscriptionTemplate = Template('application.ussd2mg.modularTariff. $package : request $request : shortcode $key')
dbTemplate = Template('application.ussd2mg.database. $package')
technoTreeTemplate = Template('application.ussd2mg.technoTreeAbility.$package')
mailServerTemplate = Template('application.ussd2mg.mailServer.$package')

'''external nodes interaction timers'''
airTimeTemplate = 'application.ussd2mg.air.time'
technoTreeTimeTemplate = 'application.ussd2mg.technoTreeAbility.time'
dbTimeTemplate = 'application.ussd2mg.database.time'
mailServerTimeTemplate = 'application.ussd2mg.mailServer.time'
dataPlanSubscriptionTimeTemplate = Template('application.ussd2mg.shortcode:$key.time')
dataPlanBalanceCheckTimeTemplate = Template('application.ussd2mg.shortcode:$key.time') #internet proxy
servicePlanSubscriptionTimeTemplate = Template('application.ussd2mg.shortcode:$key.time')

