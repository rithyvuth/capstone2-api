#!/usr/bin/python3

import sys
sys.path.insert(0, '/var/www/api')

from api import app as application

if __name__ == '__main__':
    application.run()
