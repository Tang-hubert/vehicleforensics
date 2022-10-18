# Author: Hubert
# Tester: Hubert

# from utils.watchdog import Watchdog
# import bluetooth as bt
# [bluetooth](https://stackoverflow.com/questions/23985163/python3-error-no-module-named-bluetooth-on-linux-mint)

import os, sys, time
from datetime import datetime
import subprocess
from dotenv import load_dotenv
import logging
import pika

import config as cfg

from pathlib import Path

# setting path
# path = sys.path.append('../')

# Load .env
dotenv_path = Path('./client-side/.env')
load_dotenv(dotenv_path=dotenv_path)

# RabbitMQ setup
RABBIRMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

RABBITMQ_USERNAME = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

# Logging Config
# https://www.loggly.com/blog/4-reasons-a-python-logging-library-is-much-better-than-putting-print-statements-everywhere/#gist21143108
log = logging.getLogger(__name__)
format_str = '%(levelname)s\t%(asctime)s -- %(filename)s:%(lineno)s %(funcName)s -- %(message)s'
# log 級別、建立 log 時間、發出 log 的程式檔名、發出 log 的行號、	發出 log 的函式名、log 的訊息內容

console = logging.StreamHandler()
console.setFormatter(logging.Formatter(format_str))
log.addHandler(console)  # prints to console
# file_log = logging.FileHandler(f"debug_{time.time()}.log")
file_log = logging.FileHandler(f'client-side/logs/debug_{datetime.now().strftime(r"%Y-%m-%d_%H.%M.%S")}.log', encoding='utf-8')
file_log.setFormatter(logging.Formatter(format_str))
log.addHandler(file_log)
log.setLevel(logging.DEBUG)


# class Client:
#     def __init__(self, mac, port=1):
#         self.mac = mac
#         self.port = port
#         log.info('Client Inited')

#     def connect(self):
#         self.sock = bt.BluetoothSocket(bt.RFCOMM)
#         log.info('Client connecting ...')
#         self.sock.connect((self.mac, self.port))
#         if self.connected:
#             log.info('Connection Established')

#     def init(self):
#         for cmd in cfg.INIT_COMMAND_LIST:
#             msg = (cmd + '\r').encode('utf-8')
#             _ = self.send(msg)

#     def disconnect(self):
#         log.info('Connection Closed')
#         self.sock.close()
#         self.sock = None

#     def send(self, msg):
#         self.sock.send(msg)
#         log.debug(f'send msg : {msg}')
#         # time.sleep(0.01) # 500ms
#         res: bytes = self.sock.recv(1024)

#         log.debug(f' recv msg : {res}')
#         return res.decode('utf-8')

#     @property
#     def connected(self):
#         # https://github.com/Thor77/Blueproximity/blob/79b20fce260f761785e35a041b30ff7005b8d883/blueproximity/device.py
#         p = subprocess.run(
#             ['hcitool', 'lq', self.mac],
#             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return p.returncode == 0


def main():
    # client = Client(mac=cfg.MAC_ADDR)
    # client.connect()
    # time.sleep(0.2)  # Important
    # client.init()

    # while 1:
    #     try:
    #         for pid in cfg.PID_COMMAND_LIST:
    #             msg = ('01' + pid + '\r').encode('utf-8')
    #             # with Watchdog(2):
    #             #     res = client.send(msg)
    #             res = client.send(msg)
    #         time.sleep(0.05)
    #     except KeyboardInterrupt:
    #         log.debug("** KeyboardInterrupt **")
    #         # client.disconnect()
    #         sys.exit()

    # rabbitMQ producer
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

    parm1 = pika.ConnectionParameters(host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)

    print(parm1)

    all_parm = [parm1]

    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_QUEUE)

    while True:
        Message =datetime.now().strftime('%H:%M:%S') + cfg.MAC_ADDR
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=Message)
        # body: prod to cons

        # print(" [x] Message Sent")
        log.info(" [x] Message Sent" + Message)
 

        time.sleep(2)

if __name__ == '__main__':
    main()
