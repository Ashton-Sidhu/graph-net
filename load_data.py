import json
import os

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from collections import namedtuple
from functools import reduce

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.0'

def deep_get(dictionary, *keys):
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)

def load_data(rdd):
        
    features = [
        "time",
        "hostname",
        "os",
        "process",
        "process_path",
        "parent_process",
        "parent_process_path",
        "user",
        "domain"
    ]

    Event = namedtuple("Event", features)
    
    def write_event(log):
        
        log = json.loads(log[1])
        
        time = deep_get(log, "event", "created")
        hostname = deep_get(log, "host", "hostname")
        os = deep_get(log, "host", "os", "name")
        process = deep_get(log, "process", "name")
        process_path = deep_get(log, "process", "executable")
        parent_process = deep_get(log, "process", "parent", "name")
        parent_process_path = deep_get(log, "process", "parent", "executable")
        user = deep_get(log, "user", "name")
        domain = deep_get(log, "user", "domain")
        

        e = Event(
            time=time,
            hostname=hostname,
            os=os,
            process=process,
            process_path=process_path,
            parent_process=parent_process,
            parent_process_path=parent_process_path,
            user=user,
            domain=domain
        )
        
        # Write to Graph DB

    rdd.foreach(write_event )
    
def main():

    sc = SparkContext(master="spark://192.168.0.10:7077").getOrCreate("load_data")

    ssc = StreamingContext(sc, 5)

    kstream = KafkaUtils.createStream(ssc, '192.168.0.10:2181', 'spark-streaming', {'sysmon': 1})
    
    kstream.foreachRDD(load_data)

    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()
