import os
import thread
import time

'''def runActive():
    os.system('python active.py')
    time.sleep(10)

def runPassive():
    os.system('python direct.py')

t = threading.Thread(target=runPassive)
t = threading.Thread(target=runActive)'''

os.system('python direct.py &')

while(True):
    os.system('python active.py')
    time.sleep(10)
#thread.start_new_thread(runPassive,)
#thread.start_new_thread(runActive,)
