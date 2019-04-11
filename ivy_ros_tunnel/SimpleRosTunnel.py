import os
import sys
import threading as th
import time
import socket

from ivy.std_api import *
import logging
import rospy
from std_msgs.msg import String

class SimpleIvyRosTunnel(th.Thread):
    
    def __init__(self, ivyBroadcast="127.255.255.255:2010", ivyFilter='(.*)'):
        super(SimpleIvyRosTunnel, self).__init__(name=self.__class__.__name__ + "_"
                                                        + socket.gethostname())
        
        self.ivyBroadcast = ivyBroadcast
        self.ivyFilter = ivyFilter
        self.running = False

        IvyInit(self.name)
        logging.getLogger('Ivy').setLevel(logging.WARN)
        rospy.init_node(self.name)
        self.rosPublisher = rospy.Publisher(self.name, String, queue_size = 10)
        self.rosSubscribers = {}

    def format_name(self, agent):
        return agent.replace('@','at').replace(' ', '_').replace('\\','')

    def run(self):

        """
        this function run in background and check for new topics to publish on the ivy bus
        """
        self.running = True
        while self.running:
            publishedTopics = rospy.get_published_topics()
            
            for topic in publishedTopics:
                if not self.__class__.__name__ in topic[0]:
                    # print("Discarding ", topic[0])
                    continue
                if not "std_msgs/String" == topic[1]:
                    # print("Discarding" , topic[0])
                    continue
                if self.name in topic[0]:
                    # print("Discarding ", topic[0])
                    continue
                if not any([topic[0] == published for published in self.rosSubscribers.keys()]):
                    print("Subscribing to ", topic[0])
                    self.rosSubscribers[topic[0]] = rospy.Subscriber(topic[0],
                                                                     String,
                                                                     self.ivy_publish)
            time.sleep(0.5)
    
    def ivy_publish(self, data):
        # print("Publishing on ivy : \"", str(data.data), "\"")
        IvySendMsg(data.data)

    def ros_publish(self, agent, msg):
        # print("Agent : ", str(agent))
        if not self.name in str(agent):
            self.rosPublisher.publish(msg)

    def start(self):
        # print("Start listening")
        IvyStart(self.ivyBroadcast)
        IvyBindMsg(lambda agent, msg: self.ros_publish(agent, msg), '(.*)')
        super(SimpleIvyRosTunnel, self).start()

    def stop(self):
        print("\nStopping...")
        self.running = False
        self.join(timeout=3.0)
        IvyStop()
        print("Done !")

