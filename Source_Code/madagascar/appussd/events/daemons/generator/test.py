def test_setup():
    from events.daemons.generator.server_event_enqueue import setup
    from utilities.logging.core import log
    resources = setup()
    resources
    log(resources, 'test', 'info')

if __name__ == '__main__':
    test_setup()
