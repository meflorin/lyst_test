#!/usr/bin/env python

import sys
import fileinput
from classes.CronShedulerParser import CronShedulerParser

def main():
        
    cronjobs = []
    nbArgv = len(sys.argv)
    cronTime = None
    
    if (nbArgv > 1):
        cronTime = sys.argv[1]
        for line in fileinput.input(sys.argv[2:]):
            cronjobs.append(line)
        
        cronParser = CronShedulerParser(cronjobs, cronTime)
        cronParser.setDelimiter('/bin')
        cronParser.processCronJobs()
        messages = cronParser.getMessages()
        
        for i in range(len(cronjobs)):
            print(messages[i] + " - " + cronParser.getDelimiter() + cronjobs[i].split(cronParser.getDelimiter())[1])
    else:
        print('not enough arguments')
    
main()