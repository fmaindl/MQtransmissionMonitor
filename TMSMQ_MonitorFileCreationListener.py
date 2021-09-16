import watchdog.events
import watchdog.observers
from datetime import datetime
from TMSMQ_MonitorEmailTransmission import EmailHandler
import logging
from TMSMQ_MonitorFileReader import FileReader
from config import ALERT_MESSAGE,SUMMARY_MESSAGE

  
  
class EventHandler(watchdog.events.PatternMatchingEventHandler):

    #used to track the number of failed messages
    global error_count
    error_count = 0

    #used to keep track of event/load_id combination during the downtime
    global failure_list
    failure_list = []

    def __init__(self):
        #Initialization of the EventHandler object
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.failed', '*.delivered'],
                                                             ignore_directories=True, case_sensitive=False)
    def on_moved(self, event):

        #instantiate a reference to the global variables
        global error_count
        global failure_list

        #Course of action if a new failed message is detected
        if 'failed' in event.dest_path: 
            try:
                #Read XML file that failed
                event_info = FileReader.ReadLoadEventFile(event.dest_path)
                #Add the file info to the list
                failure_list.append(event_info)
            except:
                print("oops didn't work")

            #Add this failed message to the global count  
            error_count += 1

            logging.info("Error count is now at {}".format(error_count))
            logging.info("Failed TMS Event File Detected - File Name --> - % s." % event.dest_path)
 
            #If it's the first occurence in the current downtime session, send an alert message
            if error_count == 1:
                try:
                    CurrentTime = datetime.now()
                    logging.debug("Launching Alert Email Creation Process")
                    email = EmailHandler.CreateEmail(ALERT_MESSAGE,CurrentTime)
                    EmailHandler.SendEmail(email)
                except:
                    logging.error("Something went wrong during transmission of e-mail... Oops!")

            else:
                logging.info("Skipping e-mail transmission, e-mail already sent. Currently at {} failed messages.".format(error_count))

        #If a new successfully delivered message is detected in a downtime session, send a summary e-mail
        elif 'delivered' in event.dest_path and error_count >= 1:
            logging.info("Service Restored")
            logging.info("Total Error Count: {}".format(error_count))

            #Reset the error_count to 0, this indicates that we are out of a downtime session and return to normal
            error_count = 0
            CurrentTime = datetime.now()
            try:
                logging.debug("Launching Service Restoration Email Creation Process")
                email = EmailHandler.CreateEmail(SUMMARY_MESSAGE,CurrentTime,failure_list)
                EmailHandler.SendEmail(email)
            except:
                logging.error("Something went wrong during transmission of e-mail... Oops!")
                
            #Reinitialise the failed message list
            failure_list = []