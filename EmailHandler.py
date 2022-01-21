import smtplib
from datetime import date
import json
from Hub import MAIL_HUB , getData , updateDataFile
from EmailStats import STATS , updatePostStats, updatePreStats


# This code will be scheduled to run eveyday at 12:00 noon

#------------- Functions -------------------------------------

#Sends the email
def sendEmail(sub,mssg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        email = "rachanaroxx10@gmail.com"
        password = "ijrwcrqamfsrlwpn"
        
        smtp.login(email,password)
        
        subject = sub
        body = mssg

        message = f"Subject:{subject}\n\n{body}"

        smtp.sendmail(email, email, message)

#Check if the email should be sent today
def sendToday(dt):
    if( str(date.today()) == dt):
        return True
    return False


#---------------------------- MAIN FUNCTION -----------------------------------


# Driver Code
def main():

    # Get email and stat data from files
    hubdata = getData(MAIL_HUB)
    stats = getData(STATS)

    # Get next email in queue
    inqueue = hubdata["DeliveryQueue"]
    donequeue = hubdata["SentQueue"]
    nextmailfile = inqueue[0]

    #CHANGE LATER! Set delivery date as today for testing purposes
    deliverydate = str( date.today() )
    
    #Check if email should be delivered today
    if sendToday(deliverydate):     

        updatePreStats(stats,hubdata,nextmailfile) 

        # Get mail data
        nextmail = getData(nextmailfile)

        # Prepare subject and message of email
        Sno = hubdata["SerialNo"]
        delay = nextmail["delay"]

        subj = f"<{Sno}> A Message From {delay} ago!"
        mssg = nextmail["message"]

        try:
            # Send Email
            sendEmail(subj,mssg)

            donequeue.append(inqueue.pop(0))


        except Exception as e:
            print(e)

        # Remove email from incoming mail queue and add to sent mail queue
        #donequeue.append( inqueue.pop() )
        
        nextmailfile = inqueue[1]

        # Update Statistics data
        updatePostStats(stats,hubdata,nextmail)

        # Update statistics data to file
        updateDataFile(stats,STATS)

        # Increment total number of mails
        hubdata["SerialNo"] +=1

        # Update email data to hub file
        updateDataFile(hubdata,MAIL_HUB)


if __name__ == "__main__":
    main()