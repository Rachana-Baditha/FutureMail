import json

#----------- Global Variables ------------------------------


MAIL_HUB = "GlobalEmailInfo.json"

# MAIL_HUB keys:
# SerialNo -> Total number of emails sent
# DeliveryQueue -> Queue of email files to be sent in order of when to be sent
# SentQueue -> Queue of email files which have been sent


#---------------------------Functions------------------------


#Read data from json file
def getData(file):

    with open(file, "r") as gmi:
        data = json.load(gmi)
    
    return data

#Update data to json file
def updateDataFile(data,file):
    with open(file,"w") as gmi:
        json.dump(data,gmi)