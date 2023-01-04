from random import randint
from logging.handlers import RotatingFileHandler
import logging
import socket
import gzip
import os

class Namer:
    def __call__(self, name):
        return name + ".gz"

class Rotator:
    def __call__(self, source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            with gzip.open(dest, "wb") as df:
                df.write(data)
        os.remove(source)

class Logger:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname('localhost')     # Replace Localhost with self.hostname
        self.transaction = randint(100000, 999999)
        self.email = 'natthasath.sak@nida.ac.th'
        self.extra = {'clientip': self.ip_address, 'transaction': self.transaction, 'user': 'webapp'}
        self.log_path = './log/'
        self.log_file = 'sendmail.log'
        self.log_format = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d]   %(clientip)s:%(transaction)s   %(user)-8s    %(message)s')

    def implement(self):
        handler = RotatingFileHandler(filename=self.log_path+self.log_file, mode='a', maxBytes=2*1024*1024, backupCount=5, encoding=None, delay=0)
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.log_format)
        handler.rotator = Rotator()
        handler.namer = Namer()
        logger = logging.getLogger('root')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        while True:
            logger.info(f'Send Email to: {self.email}', extra=self.extra)

Logger().implement()