#!/usr/bin/env python
from json import dumps
from sample_data import sample_flow
def test():
    print dumps(sample_flow, indent=2)
if __name__ == '__main__':
    test()
