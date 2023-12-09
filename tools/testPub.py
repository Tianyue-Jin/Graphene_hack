import random
import string
import lorem
import zmq
from logger import getmylogger
import time


class SimSensor():

    def __init__(self):

        self.topicMap = {
        
            'A' : self.generate_float_data,
            'B' : self.generate_word_data
        }

    def generate_float_data(self):
        return ':'.join(map(str, [random.uniform(0.0, 1.0) for _ in range(5)]))

    def generate_word_data(self):
        sentance = lorem.sentence()
        return sentance

    def generate_data_for_topic(self) -> str:
        topics = list(self.topicMap.keys())
        topic_id = random.choice(topics)
        return topic_id + '/' + self.topicMap[topic_id]() #execute function
    


def main(rate):
    pub = ctx.socket(zmq.PUB)
    pub.bind(pubAddr)

    while(True):
        data = sensor.generate_data_for_topic()
        if data != "":
            try:
                pub.send_string(data)  
                if debug:
                    print(data)
                time.sleep(rate) 
            except Exception as e:
                log.error("Exeption in pubslish :", e)
            except KeyboardInterrupt:
                return 
            
           
    


if __name__ =="__main__":
    # Publishes sesnro data over zmq socket at 100ms
    log = getmylogger(__name__)
    debug = True
    pubAddr =  "ipc://SHARED"
    ctx = zmq.Context()
    sensor = SimSensor()
    main(0.1)


