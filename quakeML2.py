#
# To make outputting information simple, I insure that certain values are in each dictionary,  
#   whether they are defined in the xml or not. These dictionaries set up default values,
#   but as the xml is parsed, defined key value pairs are updated.
#
defaultPick = {'stationCode':'--','networkCode':'--','channelCode':'--',
                         'locationCode':'--','phase':'NA','time':'NA'}
#
defaultArrival = {'genericAmplitude':'NA','type':'NA','unit':'NA',
                  'period':'NA', 'evaluationMode':'NA','timeResidual':'NA',
                  'timeWeight':'NA'}
#
defaultAmplitude = {'pickID':'NA','genericAmplitude':'NA','period':'NA',
                  'unit':'NA', 'evaluationMode':'NA'}                  
#
#---------------------------------------------------------------------------------
# def getEventOrigins(xevent):
#     xorigins = xevent.findall('d:origin',ns)
#     return xorigins
#
#---------------------------------------------------------------------------------
def parse_origins(xevent,namespaces):
    xorigins = xevent.findall('d:origin',namespaces)
    origins = []
    for xorigin in xorigins:
        anOrigin = xorigin.attrib.copy()
        anOrigin.update({
        'otime': get_xitem_value_as_text(xorigin,'d:time','d:value'),
        'latitude' : get_xitem_value_as_text(xorigin,'d:latitude','d:value'),
        'longitude' : get_xitem_value_as_text(xorigin,'d:longitude','d:value'),
        'depth' : get_xitem_value_as_text(xorigin,'d:depth','d:value'),
        'dotime' : get_xitem_value_as_text(xorigin,'d:time','d:uncertainty'),
        'dlatitude' : get_xitem_value_as_text(xorigin,'d:latitude','d:uncertainty'),
        'dlongitude' : get_xitem_value_as_text(xorigin,'d:longitude','d:uncertainty'),
        'ddepth' : get_xitem_value_as_text(xorigin,'d:depth','d:uncertainty')
        })
        #
        origins.append(anOrigin)
    #
    return origins 
#
#---------------------------------------------------------------------------------   
def parse_magnitudes(xevent,namespaces):
    xmags = xevent.findall('d:magnitude',namespaces)
    mags = []
    for xmag in xmags:
        mdict = xmag.attrib.copy()        
        mdict.update({'mag': get_xitem_value_as_text(xmag,'d:mag','d:value')})       
        mdict.update({'magType': get_xitem_as_text(xmag,'d:type')})       
        value = get_xitem_as_text(xmag,'d:evaluationMode')
        if(value!='NA'):
            mdict.update({"evaluationMode" : value})
            
        value = get_xitem_as_text(xmag,'d:originID')
        if(value!='NA'):
            mdict.update({"originID" : value})
            
        value = get_xitem_value_as_text(xmag,'d:creationInfo', 'd:agencyID')
        if(value!='NA'):
            mdict.update({"agencyID" : value})
        #
        mags.append(mdict)
    return mags
#
#---------------------------------------------------------------------------------
def parse_picks(xev):
    xpicks = xev.findall('d:pick',ns)
    picks = []
    for pick in xpicks:
        pdict = defaultPick.copy()
        pdict.update(pick.attrib.copy())
        
        value = get_xitem_value_as_text(pick,'d:time','d:value')
        if(value!='NA'):
            pdict.update({"time" :value})

        value = get_xitem_as_text(pick,'d:phaseHint')
        if(value!='NA'):
            pdict.update({"phase" :value})

        value = get_xitem_as_text(pick,'d:evaluationMode')
        if(value!='NA'):
            pdict.update({"evaluationMode" :value})

        pdict.update(pick.find('d:waveformID',ns).attrib)
        picks.append(pdict)
    return picks
#
#---------------------------------------------------------------------------------
def parse_arrivals(xorigin):
    xarrivals = xorigin.findall('d:arrival',ns)
    arrivals = []
    for xarr in xarrivals:
        adict = defaultArrival.copy()
        value = get_xitem_as_text(xarr,'d:pickID')
        if(value!='NA'):
            adict.update({"pickID" :value})
        value = get_xitem_as_text(xarr,'d:phase')
        if(value!='NA'):
            adict.update({"phase" :value})
        value = get_xitem_as_text(xarr,'d:azimuth')
        if(value!='NA'):
            adict.update({"azimuth" :value})
        value = get_xitem_as_text(xarr,'d:distance')
        if(value!='NA'):
            adict.update({"distance" :value})
        value = get_xitem_as_text(xarr,'d:takeoffAngle')
        if(value!='NA'):
            adict.update({"takeoffAngle" :value})
        value = get_xitem_as_text(xarr,'d:timeResidual')
        if(value!='NA'):
            adict.update({"timeResidual" :value})
        value = get_xitem_as_text(xarr,'d:timeWeight')
        if(value!='NA'):
            adict.update({"timeWeight" :value})
        arrivals.append(adict)
    return arrivals    
    
#---------------------------------------------------------------------------------
#  Extract the arrival items from the xml
#
def parse_amplitudes(xevent):
    xamplitudes = xevent.findall('d:amplitude',ns)
    amplitudes = []
    for xamp in xamplitudes:
        adict = xamp.attrib.copy()
        adict.update(defaultAmplitude)

        value = xamp.find('d:waveformID',ns)
        if(value != None):
            adict.update(value.attrib)
        
        value = get_xitem_value_as_text(xamp,'d:genericAmplitude','d:value')
        if(value!='NA'):
            adict.update({"genericAmplitude" :value})

        value = get_xitem_as_text(xamp,'d:unit')
        if(value!='NA'):
            adict.update({"unit" :value})

        value = get_xitem_value_as_text(xamp,'d:period','d:value')
        if(value!='NA'):
            adict.update({"period" :value})
        
        value = get_xitem_as_text(xamp,'d:evaluationMode')
        if(value!='NA'):
            adict.update({"evaluationMode" :value})
        
        value = get_xitem_as_text(xamp,'d:twindowbegin')
        if(value!='NA'):
            adict.update({"twindowbegin" :value})
        
        value = get_xitem_as_text(xamp,'d:twindowend')
        if(value!='NA'):
            adict.update({"twindowend" :value})
        
        value = get_xitem_as_text(xamp,'d:twindowref')
        if(value!='NA'):
            adict.update({"twindowref" :value})
             
        amplitudes.append(adict)

    return amplitudes

#---------------------------------------------------------------------------------
#
# 'distance', 'timeResidual', 'publicID', 'timeWeight', 'time', 
#     'networkCode', 'evaluationMode', 'stationCode', 'pickID', 
#     'azimuth', 'phase', 'channelCode', 'takeoffAngle', 'locationCode'
#
#---------------------------------------------------------------------------------
def merge_arrivals_picks(arrivals,picks):
    merged = []
    for a in arrivals:
        pid = a['pickID']
        p = search_pdicts('publicID', pid, picks)
        m = a.copy()
        if(p != None):
            m.update(p[0])
        merged.append(m)
    return merged

#---------------------------------------------------------------------------------
# Make a simple tab separated table of the picks with weights greater 
#    than minWeight
def list_arrival_time_picks(arrivalTimePicks, minWeight=0.0):
    print 'StationChannel\tphase\ttime\tdistance\tazimuth\tResidual\tWeight'
    for ap in arrivalTimePicks:
        if float(ap['timeWeight']) &gt;= minWeight:
            try:
                s0 = ap['stationCode']+'-'+ap['networkCode']+'-'+ap['channelCode']+'-'+ap['locationCode']
                s0 += '\t'+ap['phase']+'\t'+ap['time']
                s0 += '\t'+ap['distance']+'\t'+ap['azimuth']
                s0 += '\t'+ap['timeResidual']+'\t'+ap['timeWeight']
                print s0
            except:
                print 'Incomplete arrival time observation.'       
#
#---------------------------------------------------------------------------------
def list_magnitudes(mags):
    print 'magType\tagencyID\tmagnitude'
    for mag in mags:
        print "%s\t%s\t%s" % (mag['magType'], mag['agencyID'],mag['mag'])
#
#---------------------------------------------------------------------------------
# get the preferred origin from the eventInfo dict and the origins list
#
def get_preferred_origin(eventInfo,origins):
        preforigin = eventInfo['preferredOriginID'].lower().split("/")[-1]
        for origin in origins:
            pID = origin['publicID'].lower().split("/")[-1]
            if(pID == preforigin):
                return origin
