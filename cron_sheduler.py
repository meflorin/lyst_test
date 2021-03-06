#!/usr/bin/env python

import sys
from classes.CronShedulerParser import CronShedulerParser

def main():

    if (len(sys.argv) > 1 and sys.stdin.isatty() == False):
                
        cronjobs = []
        cronTime = sys.argv[1]
        
        line = sys.stdin.readline()
        while line:
            cronjobs.append(line.strip())
            line = sys.stdin.readline()
        
        cronParser = CronShedulerParser(cronjobs, cronTime)
        cronParser.processCronJobs()
        messages = cronParser.getMessages()
        
        for i in range(len(cronjobs)):
            print(messages[i] + " - " + cronParser.getDelimiter() + cronjobs[i].split(cronParser.getDelimiter())[2])
    else:
        print('Not enough or wrong arguments!')

if __name__ == "__main__":
    main()