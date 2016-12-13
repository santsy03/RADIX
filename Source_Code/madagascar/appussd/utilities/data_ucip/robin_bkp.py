from itertools import cycle
from collections import deque

def roundrobin(*iterables):
    q = deque(iter(it) for it in iterables)
    for itr in cycle(q):
        try:
            yield itr.next()
        except StopIteration:
            print "xxxxxx"
            if len(q) > 0:
                q.pop()
            else:
                break


def generate_ip(hosts):
    host = '172.25.154.12'
    for ip in roundrobin(hosts):
        host = ip

    return host


if __name__ == "__main__":
    hosts = ['172.25.154.86','172.25.154.16','172.25.154.12']
    print generate_ip(hosts)
