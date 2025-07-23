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

# To make outputting information simple, I insure that certain values are in
#   each dictionary, whether they are defined in the xml or not.
#   These dictionaries set up default values, but as the xml is parsed, defined
#   key value pairs are updated.

defaultPick = {
    "stationCode": "--",
    "networkCode": "--",
    "channelCode": "--",
    "locationCode": "--",
    "phase": "NA",
    "time": "NA",
}

defaultArrival = {
    "genericAmplitude": "NA",
    "type": "NA",
    "unit": "NA",
    "period": "NA",
    "evaluationMode": "NA",
    "timeResidual": "NA",
    "timeWeight": "NA",
}

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


def parse_origins(xevent, ns):
    xorigins = xevent.findall("d:origin", ns)
    origins = []
    for xorigin in xorigins:
        anOrigin = xorigin.attrib.copy()
        anOrigin.update(
            {
                "otime": get_xitem_value_as_text(xorigin, "d:time", "d:value"),
                "latitude": get_xitem_value_as_text(
                    xorigin, "d:latitude", "d:value"
                ),
                "longitude": get_xitem_value_as_text(
                    xorigin, "d:longitude", "d:value"
                ),
                "depth": get_xitem_value_as_text(
                    xorigin, "d:depth", "d:value"
                ),
                "dotime": get_xitem_value_as_text(
                    xorigin, "d:time", "d:uncertainty"
                ),
                "dlatitude": get_xitem_value_as_text(
                    xorigin, "d:latitude", "d:uncertainty"
                ),
                "dlongitude": get_xitem_value_as_text(
                    xorigin, "d:longitude", "d:uncertainty"
                ),
                "ddepth": get_xitem_value_as_text(
                    xorigin, "d:depth", "d:uncertainty"
                ),
            }
        )
        #
        origins.append(anOrigin)
    #
    return origins


#
# ---------------------------------------------------------------------------------
def parse_magnitudes(xevent, ns):
    xmags = xevent.findall("d:magnitude", ns)
    mags = []
    for xmag in xmags:
        mdict = xmag.attrib.copy()
        mdict.update(
            {"mag": get_xitem_value_as_text(xmag, "d:mag", "d:value")}
        )
        mdict.update({"magType": get_xitem_as_text(xmag, "d:type")})
        value = get_xitem_as_text(xmag, "d:evaluationMode")
        if value != "NA":
            mdict.update({"evaluationMode": value})

        value = get_xitem_as_text(xmag, "d:originID")
        if value != "NA":
            mdict.update({"originID": value})

        value = get_xitem_value_as_text(xmag, "d:creationInfo", "d:agencyID")
        if value != "NA":
            mdict.update({"agencyID": value})
        #
        mags.append(mdict)
    return mags


#
# ---------------------------------------------------------------------------------
