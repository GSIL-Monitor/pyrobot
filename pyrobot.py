#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,time,logging 
from daemon import Daemon
from mailcmd import mailcmd


class pyrobot(Daemon):
    def _run(self):
        logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(filename)s--> %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='/tmp/pyrobot.log',
                filemode='w')
        
        ts = time.strftime("%Y-%m-%d %H:%M:%S" ,time.gmtime(time.time()+28800))
        logging.info("Pyrobot started on %s" % ts)
        print("Pyrobot started on %s" % ts)

        i=1
        while True:
            run_mailcmd()
            logging.info("Pyrobot have run %d times" % i)
            print("Yeah, pyrobot have run %d times" % i)
            time.sleep(60)
            i += 1


def run_mailcmd():

    m = mailcmd('imap.gmail.com','993',
            'smtp.gmail.com','465',
            'robot@yufu.org','qdlzxkgk')

    cmd=m.getcmd()
    if cmd:
        msg="Hello,你好\nI've got some command:\n\n"
        msg+='<ul><li>'+'</li><li>'.join(cmd)+'</li></ul>'
        msg+='\n\n PyRobot 正在全力运行...\n'
        #m.sendtext(msg)
        m.sendhtml(msg)

if __name__ == "__main__":
    daemon = pyrobot('/tmp/daemon-pyrobot.pid',
            '/dev/null','/tmp/pyrobot.out','/tmp/pyrobot.err')
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
