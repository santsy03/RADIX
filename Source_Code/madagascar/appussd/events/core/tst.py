def test_create_renewal():
    from events.core.core import setup, create_event
    from datetime import datetime, timedelta
    resources = setup()
    parameters = {}
    parameters['msisdn'] = '261336173681'
    parameters['event_id'] = 1
    parameters['service_id'] = 2
    parameters['execute_at'] = datetime.now() + timedelta(days = 2)
    parameters['can_execute'] = 1
    parameters['parameters'] = '1'
    resources['parameters'] = parameters
    create_event(resources)

def test_get_services():
    from events.core.core import setup, get_services
    resources = setup()
    print get_services(resources)

def test_get_service_functions():
    from events.core.core import setup, get_services, load_service_modules
    resources = setup()
    services =  get_services(resources)
    resources['services'] = services
    functions = load_service_modules(resources)
    for service in services:
        functions[str(service[0])](resources)

def test_get_renewals():
    from events.core.core import setup, get_events
    resources = setup()
    events = get_events(resources)
    print events

def test_handle_events():
    from events.core.core import handle_event, setup
    resources = setup()
    msg = '261336173681|2|3|893014|5,94,2,911244400051951'
    parameters = {}
    parameters['msg'] = msg
    resources['parameters'] = parameters
    handle_event(resources)


if __name__ == '__main__':
    test_create_renewal()
    #test_get_services()
    #test_get_service_functions()
    #test_get_renewals()
    #test_handle_events()
