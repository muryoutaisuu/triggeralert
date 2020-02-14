import splunk.Intersplunk
import splunk.auth
import splunk.saved

from datetime import datetime
import os
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
#from datetime import datetime

def setup_logging():
   """ initialize the logging handler """
   logger = logging.getLogger('splunk.triggeralert')
   SPLUNK_HOME = os.environ['SPLUNK_HOME']
   LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
   LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
   LOGGING_STANZA_NAME = 'python'
   LOGGING_FILE_NAME = "triggeralert.log"
   BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
   LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
   splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
   splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
   logger.addHandler(splunk_log_handler)
   splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
   return logger

logger = setup_logging()

def escape_characters(NAME):
  return NAME.replace('$',' ')

def main():
##get parameters
  keywords,kvs = splunk.Intersplunk.getKeywordsAndOptions() # get parameters
##set parameter defaults
  NAME = ""
  TIME = time.time()
  ESCAPE = False

##set used variables defaults
  sessionkey = None
  appname = None
  appuser = None

##set parameters from input
  if "name" in kvs:
    NAME = kvs["name"]

  if "esc" in keywords:
    ESCAPE = True

##NAME contains blanks (now dollars that should be converted)
  if ESCAPE == True:
    oldname = NAME
    NAME = escape_characters(NAME)
    logger.debug("Search name before and after escape: old: "+oldname+" - new: "+NAME)

##go through search elements
  #results = splunk.Intersplunk.readResults(None, None, True)

##get settings
  results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()
##get sessionkey
  sessionkey = settings.get('sessionKey')
##get appname
  appname = settings.get('namespace')
##get appuser
  appuser = settings.get('owner')
  
##get appname from user parameter
  if "app" in kvs:
    appname = kvs["app"]

##appname contains blanks (now dollars that should be converted)
  if ESCAPE:
    appname = escape_characters(appname)

  logger.debug("Search name: "+str(NAME))
  logger.debug("Session keys: "+"XXX") #str(sessionkey))
  logger.debug("App name: "+str(appname))
  logger.debug("App user: "+str(appuser))
  logger.debug("TIME: "+str(TIME))

  if (NAME != None and sessionkey != None and appname != None and appuser != None and TIME != None):
    job = splunk.saved.dispatchSavedSearch(NAME, sessionKey=sessionkey, namespace=appname, owner=appuser, triggerActions=1, now=TIME)

  splunk.Intersplunk.outputResults(results)

if __name__ == "__main__":
  #try:
  ID = datetime.now().strftime("%Y%m%d:%H%M%S.%f")
  logger.debug("                                                                                ")
  logger.debug("NEW TURN ID "+ID)
  main()
  logger.debug("END TURN ID "+ID)
  sys.exit(0)
  #except Exception as e:
  #  logger.error(str(e))
  #  sys.exit(2)
