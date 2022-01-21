import json
from Hub import MAIL_HUB
from ExtractInput import daysLeft


#--------------Global Variables---------------

STATS = "StatsHub.json"

# stats keys:
# TotalSent -> Total number of emails sent
# DaysLeft -> Number of days until next email is delivered
# Sent{Year} -> Number of emails sent in {Year}
# Recieved{Year} -> Number of emails recieved in {Year}

#---------------Functions----------------


# Store total number of emails sent from the mail hub
def storeTotalSent(hubinfo):
    return hubinfo["SerialNo"] - 1

def storeDaysLeft(hubinfo):
    queue = hubinfo["DeliveryQueue"]
    return daysLeft(queue[0])


def updatePostStats(stats,hubdata,delivery):
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

    stats["TotalSent"] = storeTotalSent(hubdata)
    stats["DaysLeft"] = storeDaysLeft(hubdata)

    print( f"DEVLIVERY = {delivery}" )

    deliverydt = delivery["deliverydate"]
    yr = deliverydt[0:4]

    if f"Sent{yr}" in stats:
        stats[f"Sent{yr}"] +=1 
    else:
        stats[f"Sent{yr}"] = 1 


def updatePreStats(stats,hubinfo,delivery):

    delivery = delivery.split()[1]
    yr = delivery[0:4]

    if f"Recieve{yr}" in stats:
        stats[f"Recieve{yr}"] += 1
    else:
        stats[f"Recieve{yr}"] = 1


def main():

    #updateStats()
    pass

if __name__ == "__main__":
    main()