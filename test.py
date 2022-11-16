import signal
import sys
import time


class A:
    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)


a = A()

signal.signal(signal.SIGINT, a.signal_handler)
time.sleep(2)
print(len(sys.argv))
print('Press Ctrl+C')
