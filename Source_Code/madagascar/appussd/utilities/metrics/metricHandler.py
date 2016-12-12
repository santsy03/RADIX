#/usr/sbin/env python


import RadixClient2


#RadixClient2.init_Radix({'RADIX_BUCKET_PREFIX': 'x'})
#RadixClient2.counter('countertest',300)

class heartBeat ():
    def __init__(self,host=None,port=None,sample_rate=None,prefix='x'):
        self.obj = {}
        self.obj['Radix_HOST'] = host or '127.0.0.1'
        self.obj['Radix_PORT'] = port or 8125
        self.obj['SAMPLE_RATE'] = sample_rate 
        self.obj['RADIX_BUCKET_PREFIX'] = prefix
        self.heartBeat_Object = RadixClient2#.init_Radix(self.obj)
        self.heartBeat_Object.init_Radix(self.obj)

    def beat(self,nameSpace):
        return self.heartBeat_Object.counter(nameSpace,)

    def timer(self,nameSpace):
        return self.heartBeat_Object.timer(nameSpace,1)

    def period(self,nameSpace,start):
        from datetime import datetime
        stop = datetime.now()
        period = int(((stop - start).microseconds))# get difference in seconds and convert to milliseconds
        #nameSpace = nameSpace.substitute(period = period)
        self.heartBeat_Object.timer(nameSpace,period)
        return period



if __name__=='__main__':
    nameSpace = 'wahuni'
    p = heartBeat()
    p.beat(nameSpace)
    p.timer(nameSpace)
    import datetime
    d = datetime.datetime(2012, 12, 6, 15, 18, 34, 649146)
    print p.period('ha',d)
    
