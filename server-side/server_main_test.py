# Author: Hubert

import time, sys, os, json, ast
from datetime import datetime
import binascii
import pika
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load .env
dotenv_path = Path('./server-side/.env')
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
file_log = logging.FileHandler(f'server-side/logs/debug_{datetime.now().strftime(r"%Y-%m-%d_%H.%M.%S")}.log', encoding='utf-8')
file_log.setFormatter(logging.Formatter(format_str))
log.addHandler(file_log)
log.setLevel(logging.DEBUG)

def main():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parm1 = pika.ConnectionParameters(
        host=RABBIRMQ_HOST, port=RABBITMQ_PORT, credentials=credentials
        )
    all_parm = [parm1]
    connection = pika.BlockingConnection(all_parm)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    def callback(ch, method, properties, body):

        log.info(" [x] Received %r" % body)
        
        # log.info(" [x] Received %r" % ch)
        # log.info(" [x] Received %r" % method)
        # log.info(" [x] Received %r" % properties)
        
        time.sleep(2)

        # tmp = json.loads(body.decode())
        # cipher_polys = ast.literal_eval(tmp["cipherPolys"])
        # signature = binascii.unhexlify(tmp["sign"])
        # print(f"\ncipher_polys : {cipher_polys}\n\nsignature : {signature}")

        pass
    channel.basic_consume(
        queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()