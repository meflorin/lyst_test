#!/usr/bin/env python

import sys
import fileinput
from classes.CronShedulerParser import CronShedulerParser

cronjobs = []

def main():
        
    nbArgv = len(sys.argv)
    cronTime = None
    
    if (nbArgv > 2):
        cronTime = sys.argv[1]
        for line in fileinput.input(sys.argv[2:]):
            cronjobs.append(line)         
    else:
        print('not enough arguments')
        
    cronParser = CronShedulerParser(cronjobs, cronTime)
    cronParser.setDelimiter('/bin')
    cronParser.processCronJobs()
    messages = cronParser.getMessages()
     
    for i in range(len(cronjobs)-1):
        print(cronjobs[i] + messages[i])
    
    
main()