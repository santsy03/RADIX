from string import Template
counter = 'counter'
timer = 'timer'

#-----------Airtime-Airtel_Money Application-----------#
#--Time Metrics Namespaces--#
db_time_template = 'application.airtel_money.database.time'
air_time_template = 'application.airtel_money.air.time'
airtel_money_time_template = 'application.airtel_money.am_server.time'
round_time_template = 'application.airtel_money.round_trip.time'
#--Counter Metrics NameSpaces--#
ussd_hits_template = 'application.airtel_money.ussd_hits'
am_responses_hits_template = 'application.airtel_money.am_responses_hits'

##---------------International bundles-----------------##
prepaid_internationalBundles_provisioningSuccessTemplate = Template('application.internationalBundles.prepaid.provisioning.success.$bundle')
prepaid_internationalBundles_provisioningFailureTemplate = Template('application.internationalBundles.prepaid.provisioning.failure.$bundle')


'''application counters'''
memc_hits = 'application.memcache.hits'
memc_failed = 'application.memcache.failure'

'''external nodes interaction timers'''

