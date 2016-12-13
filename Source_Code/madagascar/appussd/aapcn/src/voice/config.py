voice_bundles_to_be_recorded = ['222','197']
weekend_days = ['Sat','Sun']
offer_deletion_packages = [207,220,227,228,229,230,231,252,232,250,253]
unallowed_service_classes = [521]
service_class_check_packages = [232,233,225,235]
whitelisting_packages = [226,203,256]
retailer_packages_check = ['207','220']
weekend_check_packages = ['233','253']
time_restricted_packages = ['194','195','203','220','254']



uc = 1011
ut = 1011

DA_BALANCE = True

'''
configs for telescopic provisioning module
'''
MEGNIGHT_PACKAGE_ATTRIBUTES = {}
# MEGNIGHT_PACKAGE_ATTRIBUTES[ count ] = [price(Ar), volume(Mo), validity(hours), DA, refill_id, UC/UT ID, offer_id]
MEGNIGHT_PACKAGE_ATTRIBUTES['1'] = [100, 20, 1150, 'MB33', '1150', 1044]
MEGNIGHT_PACKAGE_ATTRIBUTES['2'] = [100, 20, 1151, 'MB33', '1151', 1044]


#TIME_RESTRICTION = dict(hour=16, min=59)

MEGNIGHT_DA = []
for each in MEGNIGHT_PACKAGE_ATTRIBUTES:
        MEGNIGHT_DA.append(MEGNIGHT_PACKAGE_ATTRIBUTES[each][2])

