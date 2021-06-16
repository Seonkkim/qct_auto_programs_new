from Daemon import *

import sys

if __name__ == '__main__' :
	if not len(sys.argv) == 2:
		print 'Usage : python main.py start | stop | restart'
		exit(1)
	
	daemon = Daemon('/var/log/auto_repo/auto_repo.pid')
	if sys.argv[1] == 'start':
		daemon.start()
	elif sys.argv[1] == 'stop':
		daemon.stop()
	elif sys.argv[1] == 'restart':
		daemon.restart()
	else:
		print 'Usage : python main.py start | stop | restart'
