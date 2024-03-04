""" 
    Modified from from Charles J. Ammon - Online Notes,
    https://sites.psu.edu/charlesammon/2017/01/31/parsing-usgs-quakeml-files-with-python/

    Updated Python2 -> Python3
"""

namespaces = {
    "q": "http://quakeml.org/xmlns/quakeml/1.2",
    "d": "http://quakeml.org/xmlns/bed/1.2",
    "catalog": "http://anss.org/xmlns/catalog/0.1",
    "tensor": "http://anss.org/xmlns/tensor/0.1",
}
#
# To make outputting information simple, I insure that certain values are in each dictionary,
#   whether they are defined in the xml or not. These dictionaries set up default values,
#   but as the xml is parsed, defined key value pairs are updated.
#
defaultPick = {
    "stationCode": "--",
    "networkCode": "--",
    "channelCode": "--",
    "locationCode": "--",
    "phase": "NA",
    "time": "NA",
}
#
defaultArrival = {
    "genericAmplitude": "NA",
    "type": "NA",
    "unit": "NA",
    "period": "NA",
    "evaluationMode": "NA",
    "timeResidual": "NA",
    "timeWeight": "NA",
}
#
defaultAmplitude = {
    "pickID": "NA",
    "genericAmplitude": "NA",
    "period": "NA",
    "unit": "NA",
    "evaluationMode": "NA",
}


def get_namespaces():
    return namespaces


def getEventParameters(tree):
    event_parameters = tree.findall("d:eventParameters", namespaces)
    return event_parameters


def getEvents(event_parameters):
    events = [p.findall("d:event", namespaces) for p in event_parameters][0]
    return events


def getEventOrigins(event):
    origins = event.findall("d:origin", namespaces)
    return origins
