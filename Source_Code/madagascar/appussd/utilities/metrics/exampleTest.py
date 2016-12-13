import RadixClient2
RadixClient2.init_Radix({'RADIX_BUCKET_PREFIX': 'x'})
RadixClient2.timer('pipeline',500)

RadixClient2.counter('countertest',300)

#timer = RadixClient2.RadixTimer('pipeline')
#timer.start()
# Do stuff
#timer.split('stage1') # Sends timing data for bucket 'x.pipeline.stage1'
# Do more stuff
#timer.split('stage2') # Sends timing data for bucket 'x.pipeline.stage2'
# Do even more stuff
#timer.stop() # Sends timing data for bucket 'x.pipeline.total'
