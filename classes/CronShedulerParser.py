class CronShedulerParser:
    
    cronjobs = []
    cronTime = None
    __delimiter = ''
    __messages = []
    
    def __init__(self, cronjobs = [], cronTime = None):
        self.cronjobs = cronjobs
        self.cronTime = cronTime

    def setDelimiter(self, delimiter):
        self.__delimiter = delimiter
        
    def processCronJobs(self):
        
        if (len(self.cronjobs)> 0):
            for current in self.cronjobs:
                currentLineMessage = self.parseCronJob(current)
                self.__messages.append(currentLineMessage)                
    
    def getMessages(self):
        return self.__messages
    
    def __getCronTimeParts(self):
        
        if type(self.cronTime) != type(None):
            cronTimeParts = self.cronTime.split(':')
            return [
                int(cronTimeParts[0]), 
                int(cronTimeParts[1]), 
                int(cronTimeParts[0]) * 60 + int(cronTimeParts[1])
                ]
        else:
            return []
        
    def parseCronJob(self, cronLine):
        
        cronLine = cronLine.strip()
        
        if(len(cronLine) > 0):
            
            cronTimeParts = self.__getCronTimeParts()
            
            if (len(cronTimeParts) > 2):
                
                if cronLine.find(self.__delimiter) > -1:
                    
                    info = cronLine.split(self.__delimiter)
                    
                    if (len(info) > 0):
                        
                        cronTimeCalendar = info[0].strip()
                        
                        if (len(cronTimeCalendar) > 0):
                            
                            cronTimeCalendarInfo = cronTimeCalendar.split(' ')
                            
                            message = self.getCronJobMessage(
                                cronTimeCalendarInfo[2],
                                cronTimeCalendarInfo[1],
                                cronTimeParts
                            )
                                                    
                            return message
                            
            else:
                return ''
        else:
            return ''
                        
    def getCronJobMessage(self, hour, minute, cronTimeParts):
        
        if (minute == '*' and hour != '*'):
            return "every minute every hour from now"
        
        if (minute == '*' and hour != '*'):
            if (int(hour) >= cronTimeParts[1]):
                return "every minute starting from " + hour + " hour today "
            if (int(hour) < cronTimeParts[1]):
                return "every minute starting from " + hour + "hour tomorrow "

        if (minute != '*' and hour == '*'):            
            return "every hour starting from " + minute + "minute  today "
            
        seconds = int(hour) * 60 + int(minute)

        if (seconds < cronTimeParts[2]):
            return hour + ':' + minute + ' tomorrow'
        else:
            return  hour + ':' + minute + ' today'
