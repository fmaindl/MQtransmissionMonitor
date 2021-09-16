from TMSMQ_MonitorFileCreationListener import EventHandler
import watchdog.events
import watchdog.observers
import time
import logging
from config import SOURCE_PATH,LOG_PATH





if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename=LOG_PATH, level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S', force=True)
    logging.info("Application Started")

    src_path = SOURCE_PATH

    logging.info("Monitoring Directory at {}".format(SOURCE_PATH))

    #Create the event_handler object
    event_handler = EventHandler()

    logging.debug("event_handler created")

    #Instantiate the observer object
    observer = watchdog.observers.Observer()
    #Assign the event_handler specification to the observer
    observer.schedule(event_handler, path=src_path, recursive=False)
    #Open a thread for the observer
    observer.start()

    logging.debug("observer created")  

    try:
        while True:
            time.sleep(1)
    except:
        logging.info("The application has been shutdown")
        observer.stop()
        
    #Ends the thread of the observer process
    observer.join()


    
