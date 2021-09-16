import xml.etree.ElementTree
import logging

  
  
class FileReader():

    def ReadLoadEventFile(file):
        try:
            #Loading XML file in memory
            xml_tree = xml.etree.ElementTree.parse(file)
        except:
            print("Couldn't open the xml file")

        #Returns the root element of the tree
        root = xml_tree.getroot()

        try:
            #Find the Value of EventName tag
            event = root.find('EventName').text
        except:
            logging.error("Event Name not found")
            exit()
        try:
            #Find the Value of SystemLoadID tag
            load_id = root.find('SystemLoadID').text
        except:
            logging.error("Load ID not found in the xml document")

        #concatenating event and load_Id
        evnt_ld = event + '-' + load_id

        logging.info("Load {} for event {} was found".format(load_id,event))

        return evnt_ld

