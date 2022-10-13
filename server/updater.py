import psutil
import sys
from subprocess import Popen

proc = None

def servertester():
    global proc

    #sys.stdout = open('/home/ubuntu/server/server_log.log', 'a')
    for process in psutil.process_iter():
        if process.cmdline() == ['python3', '/home/ubuntu/server/socket_server.py']:
            #sys.exit('Process found: exiting.')
            #print("Process found: exiting")
            return "Process found: exiting"

    proc = Popen(['python3', '/home/ubuntu/server/socket_server.py'])
    #print('Process not found: starting it.')
    #sys.stdout.close()
    return ('Process not found: starting it.')

def serverkill():
    proc.kill()
    return("Killed server")

#function()