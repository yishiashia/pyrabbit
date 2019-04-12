import pika
import threading

class rabbitThread(threading.Thread):
  def __init__(self):
    self._running_flag = False
    self.stop = threading.Event()
    self.connection = None
    self.channel = None
    threading.Thread.__init__(self, target=self.consume_message)

  def callback(self, ch, method, properties, body):
    fd = open('rabbit.log', 'a')
    fd.write(" [x] Received %r\n" % body)
    fd.flush()
    fd.close()
    ch.basic_ack(delivery_tag = method.delivery_tag)

  def consume_message(self):
    self._running_flag = True
    credentials = pika.PlainCredentials('YOUR_ACCOUNT', 'YOUR_PASSWORD')
    parameters = pika.ConnectionParameters('127.0.0.1',
                                         5672,
                                         '/',
                                         credentials)
    self.connection = pika.BlockingConnection(parameters)
    self.channel = self.connection.channel()

    self.channel.basic_consume(self.callback, queue='YOUR_QUEUE')
    self.channel.start_consuming()

  def terminate(self):
    self.stop.set()
    if self.channel is not None:
      self.channel.stop_consuming()
    if self.connection is not None:
      self.connection.close()
    self._running_flag = False