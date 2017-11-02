#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,time,logging 
from daemon import Daemon


class pyrobot(Daemon):
    def _run(self):
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s --> %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/tmp/myrobot.log',
                filemode='w')
        
        ts = time.strftime("%Y-%m-%d %H:%M:%S" ,time.localtime())
        logging.info("Pyrobot started on %s" % ts)
        print("Pyrobot started on %s" % ts)

        i=1
        while True:
            logging.info("Pyrobot have run %d times" % i)
            print("Yeah, pyrobot have run %d times" % i)
            time.sleep(5)
            i += 1


if __name__ == "__main__":
    daemon = pyrobot('/tmp/daemon-pyrobot.pid',
            '/dev/null','/tmp/myrobot.out','/tmp/myrobot.err')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print( "Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print( "usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
