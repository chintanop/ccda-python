import datetime

def timestamp_to_integer(val):
    #print "parsing month year:"+val 

    if not val:
        return None

    if len(val)>8:
        val = val[:8]

    if len(val)<=8:
        year = val[:4]
        print val+" => "+year

    if len(val)==6:
        month = val[-2:]
        print "month "+month
    else:
        month = "1"
   
    day = "1"
    if len(val)==8:
        day = val[-2:]
        month = val[-4:-2]


    #TODO: for mins and secos
    print "Creatign date :"+year+" "+month+" "+day

    dt = datetime.datetime(year=int(year), month=int(month), day=int(day))

    sincepoch = (dt - datetime.datetime(1970,1,1)).total_seconds()

    return sincepoch

