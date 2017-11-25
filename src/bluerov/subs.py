#!/usr/bin/env python

import json
import rospy
import time
import yaml


class Subs(object):
    def __init__(self):
        # Dict with all data
        self.data = {}
        # Get data from topic list
        self.topics = [
        ]

        self.subscribe_topics()

    def get_data(self):
        return self.data

    def set_data(self, path, value={}):
        # The first item will be empty
        keys = path.split('/')[1:]
        current_level = self.data
        for part in keys:
            # If dict don't have the path, create it !
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        if value is not {}:
            current_level.update(yaml.load(str(value)))

    def subscribe_topic(self, topic, msg_type, queue_size=1):
        self.set_data(topic)
        rospy.Subscriber(topic, msg_type, self.callback, callback_args=topic, queue_size=queue_size)

    def subscribe_topics(self):
        for topic, msg_type in self.topics:
            self.subscribe_topic(topic, msg_type)

    def callback(self, data, topic):
        self.set_data(topic, data)


if __name__ == '__main__':
    import sensor_msgs.msg

    try:
        rospy.init_node('get_mav_data')
    except rospy.ROSInterruptException as error:
        print('pubs error with ROS: ', error)
        exit(1)

    sub = Subs()
    sub.subscribe_topic('/mavros/battery', sensor_msgs.msg.BatteryState)

    def print_voltage():
        try:
            rospy.loginfo(sub.get_data()['mavros']['battery']['voltage'])
        except Exception as error:
            print(error)

    while not rospy.is_shutdown():
        print_voltage()
        time.sleep(1)
