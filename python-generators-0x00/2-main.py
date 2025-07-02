
import sys
processing = __import__('1-batch_processing')

# print processed users in a batch of 50
try:
    print('trying batch processing')
    processing.batch_processing(50)
    print("AFTER batching")
except BrokenPipeError:
    print("ERROR IN MAIN")
    sys.stderr.close()
