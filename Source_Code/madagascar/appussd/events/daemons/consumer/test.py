def test_setup():
    from events.daemons.consumer.server_event_consume import setup
    from utilities.logging.core import log
    resources = setup()
    log(resources, 'test', 'info')

if __name__ == '__main__':
    test_setup()
