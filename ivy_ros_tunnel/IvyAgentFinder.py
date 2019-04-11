import os
import sys
import threading as th

from ivy.std_api import *
import logging
import rospy
from std_msgs.msg import String

class IvyAgentFinder:
    
    def __init__(self, ivyBroadcast="127.255.255.255:2010"):
        
        self.ivyBroadcast = ivyBroadcast
        self.name = "IvyAgentFinder_" + str(id(self))

        IvyInit(self.name)
        logging.getLogger('Ivy').setLevel(logging.WARN)
        rospy.init_node(self.name)
        self.checkTimer = th.Timer(1.0, self.update_ivy_agents)
        self.checkTimer.start()

        self.agentTopic = {}

    def format_name(self, agent):
        return agent.replace('@','at').replace(' ', '_').replace('\\','')

    def update_topics(self, agent, msg):
        # print("Agent \"" + self.format_name(str(agent)) + "\" sent \"" + msg + "\"")
        agentName = self.format_name(str(agent))
        try:
            self.agentTopic[agentName].publish(msg)
        except:
            self.agentTopic[agentName] = rospy.Publisher(agentName,
                                                         String,
                                                         queue_size = 10)
    def update_ivy_agents(self):
        topics = rospy.get_published_topics()
        print(topics)
        # for topic in topics:
        #     if not any(topic in agent[0] for agent in self.agentTopic):
        #         print("New topic !")

    def start(self):
        print("Start listening")
        IvyStart(self.ivyBroadcast)
        IvyBindMsg(lambda agent, msg: self.update_topics(agent, msg), '(.*)')

    def stop(self):
        print("\nStopping IvyBus...")
        IvyStop()
        self.checkTimer.stop()
        print("Done !")

