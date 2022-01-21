from Hub import MAIL_HUB
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


#------------- NOTES ----------------------------------------

# Comment the shit out of everything

# ------------ INITIALIZING GLOBAL STUFF ---------------------------

# Global variables:
#   newmailinfo -> dict
#   NEW_MAIL -> string

# newmailinfo -> Dict to store data about new email
newmailinfo = {}

# newmailinfo keys:
#   senddate -> Date email was sent
#   delay -> Number of months/weeks/etc. between send and delivery date
#   deliverydate -> Date email should be delivered
#   message -> Content of email

# Getting serial number from hub file
mailf = open(MAIL_HUB , 'r')

globalmailinfo = json.load(mailf)
Sno = globalmailinfo["SerialNo"]

mailf.close()

# NEW_MAIL -> NAME of the json file for the new email
NEW_MAIL= f" ({Sno}) {date.today()}.json"


#----------------- FUNCTIONS --------------------------------------


# Check no. of days until email is sent
def daysLeft(mailfile):

    with open(mailfile) as mailf:

        mailinfo = json.load(mailf)

        # Get delivery date of email
        dd = datetime.strptime( mailinfo["deliverydate"] , "%Y-%m-%d").date()

        # Get no. of days as int datatype from timedelta datatype
        return int( ( str( dd - date.today() ).split() )[0] )

# Delay email by a number of months
def addMonths(mdelay: int):
    
    return date.today() + relativedelta(months= +mdelay)

# Delay email by a number of weeks
def addWeeks(wdelay: int):

    return date.today() + relativedelta(weeks= +wdelay)

# Get delivery date from user
def getDeliveryDate():

    global newmailinfo
    deliverydate = date(1,1,1)

    #Getting input from user
    select = int( input("Delay by:\n1. Months \t 2. Weeks \n"))

    if select == 1:

        #Add "mdelay" number of months
        mdelay = int(input("Number of months: "))
        deliverydate = addMonths(mdelay)

        #Add delay data to newmailinfo dictionary
        newmailinfo["delay"] = f"{mdelay} Months"

    elif select == 2:

        # Add "wdelay" number of weeks
        wdelay = int( input("Number of Weeks: ") )
        deliverydate = addWeeks(wdelay)

        # Add delay data to newmailinfo dictionary
        newmailinfo["delay"] = f"{wdelay} Weeks"

    # Add delivery date and no. of days left data to newmailinfo dictionary
    newmailinfo["deliverydate"] = str(deliverydate)

# Get content of email
def getMessage():

    global newmailinfo

    mssg = input("Your Message to Your Future Self:\n")

    newmailinfo["message"] = mssg

# Store new mail data in a file
def storeNewEmail():
    with open( NEW_MAIL , "w") as mailf:
        json.dump(newmailinfo, mailf)
    
# Update hub file 
def updateHub():

    #---Reading from file---

    mailf = open(MAIL_HUB, "r")

    # Get current queue
    globalmailinfo = json.load(mailf)
    filequeue = globalmailinfo["DeliveryQueue"]

    mailf.close()

    #---Writing to File---

    mailf = open(MAIL_HUB, "w")

    try:

        # If queue is not empty, place the file in the correct place in line
        if filequeue:

            # flg checks if the file was added to the middle queue
            # If flg is still 0, add the new file to the end of the queue
            flg = 0

            # Loop through all files in queue
            for i in range( len( filequeue ) ):

                # Place file in ascending order of days left until delivery
                if daysLeft(NEW_MAIL) < daysLeft( filequeue[i] ):

                    #Insert file into middle of queue
                    filequeue.insert(i,NEW_MAIL)
                    flg = 1
                    break

            if flg == 0:
                
                #Insert file to end of queue
                filequeue.append(NEW_MAIL)
            
        # If queue is empty, directly add file 
        else:
            filequeue.append(NEW_MAIL)

        #Update Queue and SerialNo values
        globalmailinfo["DeliveryQueue"] = filequeue
        globalmailinfo["SerialNo"] +=1
    
    except Exception as e:

        # Print the error but continue the program
        # If I don't do this, the global/hub mail file data is erased when opened as "w" but the program crashes before data can be written to it. 
        # Now I still see the error but the program just re-writes the old data 

        print(e)
        pass

    # REMOVE LATER - For testing queue status
    print( globalmailinfo["DeliveryQueue"] )

    # Update email data to hub file
    json.dump(globalmailinfo,mailf)


#--------------- MAIN FUNCTION ------------------------------------


# Driver code
def main():
    global newmailinfo

    newmailinfo["senddate"] = str( date.today() )

    # Gets date of delivery from user 
    # Updates deliverydate and delay keys
    getDeliveryDate()

    # Gets content of email from user
    # Updates message key
    getMessage()

    # Stores new email dict in file
    storeNewEmail()

    # Adds new email file to queue of files to be sent
    # Increments total email counter
    # Updates to global/hub file
    updateHub()


if __name__ == "__main__":
    main()
