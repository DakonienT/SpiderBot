# SuperFastPython.com
# example of running a function in another thread
from time import sleep
from threading import Thread
 
# a custom function that blocks for a moment
def task():
    while True:
        # block for a moment
        sleep(1)
        # display a message
        print('This is from another thread')
 
# create a thread
thread = Thread(target=task)
# run the thread
thread.start()
# wait for the thread to finish
while True:
    sleep(0.5)
    print('Waiting for the thread...')