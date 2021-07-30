from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import Adafruit_DHT
from board import *
import json
import time
from datetime import datetime

#set credentials
host= #enter endpoiint
rootCAPath= #enter root ca certificate
certificatePath= #enter certificate
privateKeyPath= #enter your private key
clientId= #enter an ID
topic= # enter a topic
port= #enter the port you need


#configure mqtt
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)



# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()


#initiate publishing
while True:
    date= datetime.now()
    sdate= str(date)
    humidity, temperature= Adafruit_DHT.read_retry(11,4) #parameters may differ based on the gpio pins you use
    message ={}
    message['Temperature'] = temperature
    message['Humidity'] = humidity
    message['Datetime'] = sdate
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    time.sleep(5)