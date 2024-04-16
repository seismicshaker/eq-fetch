#! /usr/bin/env python3

from xml.etree import ElementTree

import quakeML as qml

tree = ElementTree.parse("19840812.xml")
root = tree.getroot()

event_params = qml.getEventParameters(tree)
events = qml.getEvents(event_params)
print(len(events))
