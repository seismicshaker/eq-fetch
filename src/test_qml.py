#! /usr/bin/env python3
"""
https://sites.psu.edu/charlesammon/2017/01/31/parsing-usgs-quakeml-files-with-python/

https://docs.python.org/3/library/xml.etree.elementtree.html

https://github.com/Jamalreyhani/pyquakeml/blob/master/src/pyquakeml.py

https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
"""

from xml.etree import ElementTree

import quakeML as qml

tree = ElementTree.parse("19840812.xml")
root = tree.getroot()

event_params = qml.getEventParameters(tree)
events = qml.getEvents(event_params)

for event in events:
    for child in event:
        print(child.tag)
        for cc in child:
            print(" ", cc.tag)
    exit()
