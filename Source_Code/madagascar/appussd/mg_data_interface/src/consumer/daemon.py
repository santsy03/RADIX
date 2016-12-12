#!/usr/bin/env python
'''
Daemonizing library for python that implements the double fork UNIX magic
'''
import sys, os, time, atexit
from signal import SIGTERM 

class Daemon(object):
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null',
    stdout='/dev/null',
    stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, err: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (err.errno, 
														err.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, err: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (err.errno, 
														err.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        stdi = file(self.stdin, 'r')
        stdo = file(self.stdout, 'a+')
        stde = file(self.stderr, 'a+', 0)
        os.dup2(stdi.fileno(), sys.stdin.fileno())
        os.dup2(stdo.fileno(), sys.stdout.fileno())
        os.dup2(stde.fileno(), sys.stderr.fileno())
    
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
    
    def delpid(self):
        '''
        Delete the pid
        '''
        os.remove(self.pidfile)

    def checkpid(self, pid):
        '''
        Check if pid is in process list
        '''
        is_alive = True
        try:
            os.kill(pid, 0)
        except OSError:
            is_alive = False
        return is_alive

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pidfile = file(self.pidfile,'r')
            pid = int(pidfile.read().strip())
            pidfile.close()
        except IOError:
            pid = None
        if pid != None:
            #check if pid is in process lists ie it is really running
            is_alive = self.checkpid(pid)
	    if is_alive:
                message = "pidfile %s already exist. Daemon already running?\n"
                sys.stderr.write(message % self.pidfile)
                sys.exit(1)
            
            else:
                self.delpid()
        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pidfile = file(self.pidfile,'r')
            pid = int(pidfile.read().strip())
            pidfile.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process    
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will 
        be called after the process has been
        daemonized by start() or restart().
        """
