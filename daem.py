import os, sys
from sqlbak.logger import log_method

class Daem:

    @log_method
    def daem(self):
        """
        UNIX double fork mechanism.
        """
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            sys.exit(1)
        else:
            os.chdir("/")
            os.setsid()
            os.umask(0)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            sys.exit(1)

    @log_method
    def start(self):
        self.daem()
        self.run()

    @log_method
    def run(self):
        """
        This method should be overridden when subclass Daem.
        """
        return

# okay decompiling /home/lm/PycharmProjects/backs/pyc/sqlbak/daem.pyc
