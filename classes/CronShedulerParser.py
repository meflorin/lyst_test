class CronShedulerParser:
    
    cronjobs = []
    cronTime = None
    __whichDay = { True: 'today', False: 'tomorrow' }
    __cronTimeHour = None
    __cronTimeMinute = None
    __delimiter = ''
    __messages = []
    
    def __init__(self, cronjobs = [], cronTime = None):
        self.cronjobs = cronjobs
        self.cronTime = cronTime
        self.__cronTimeHour, self.__cronTimeMinute = self.__getCronTimeParts()

    def setDelimiter(self, delimiter):
        self.__delimiter = delimiter
        
    def getDelimiter(self):
        return self.__delimiter
        
    def processCronJobs(self):
        
        if (len(self.cronjobs)> 0):
            for current in self.cronjobs:
                nextCronTime = self.__parseCronJob(current)
                nextCronTimeMessage = self.__getCronJobMessage(nextCronTime)
    
    def getMessages(self):
        return self.__messages
    
    def __validateInputs(self, hour, minute):
        
        if isinstance(hour, int):
            if (hour < 0 and hour > 23): 
                return False
        
        if isinstance(minute, int):
            if (minute < 0 and minute > 59): 
                return False
            
        if (isinstance(minute, str) and minute != '*'):
            return False
        
        if (isinstance(hour, str) and hour != '*'):
            return False
        
        return True
        
    def __getCronTimeParts(self):
        
        if type(self.cronTime) != type(None):
            cronTimeParts = self.cronTime.split(':')
            return [
                int(cronTimeParts[0]),
                int(cronTimeParts[1])
                ]
        else:
            return [None, None]
        
    def __parseCronJob(self, cronLine):
        
        cronLine = cronLine.strip()
        
        if(len(cronLine) > 0):
                                        
            if cronLine.find(self.__delimiter) > -1:
                
                info = cronLine.split(self.__delimiter)
                
                if (len(info) > 0):
                    
                    cronTimeCalendar = info[0].strip()
                    
                    if (len(cronTimeCalendar) > 0):
                        
                        cronTimeCalendarInfo = cronTimeCalendar.split(' ')
                        nextCronTime = self.__getCronNextTime(
                            hour = int(cronTimeCalendarInfo[1]) if cronTimeCalendarInfo[1].isdigit() else cronTimeCalendarInfo[1],
                            minute =  int(cronTimeCalendarInfo[0]) if cronTimeCalendarInfo[0].isdigit() else cronTimeCalendarInfo[0],                            
                            )
               
                        return nextCronTime
                            
        else:
            return []
                        
    def __getCronNextTime(self, hour = '*', minute = '*'):
        
        if self.__validateInputs(hour, minute) is False:
            return []
        
        # * *
        if (hour == '*' and minute == '*'):
            return [self.__cronTimeHour, self.__cronTimeMinute, True]

        # 45 *
        if (hour == '*' and minute != '*'):
            
            if (int(minute) > self.__cronTimeMinute):
                return([self.__cronTimeHour, minute, True])
            
            if (int(minute) <= self.__cronTimeMinute):
                #check if not passed midnight
                if(self.__cronTimeHour + 1 >= 24):
                    return [0, minute, False]
                else:
                    return [self.__cronTimeHour + 1, minute, True]
                
        # * 19
        if (hour != '*' and minute == '*'):
            
            #if hour passed, next day
            if (hour < self.__cronTimeHour):
                return [hour, 0, False]
            
            if (hour > self.__cronTimeHour):
                return [hour, 0, True]
            
            if (hour == self.__cronTimeHour):
                if (self.__cronTimeMinute == 59):
                    if (hour == 23):
                        return [hour, 0, False]
                    else:                        
                        return [hour + 1, 0, True]
                else:                        
                    return [hour,self.__cronTimeMinute + 1, True]
                
        # 12 13
        if (hour != '*' and minute != '*'):
            
            if (hour == self.__cronTimeHour):
                if (minute <= self.__cronTimeMinute):
                    return [hour, minute, False]
                else:
                    return [hour, minute, True]
                
            if (hour < self.__cronTimeHour):
                return [hour, minute, False]
            
            if (hour > self.__cronTimeHour):
                return [hour, minute, True]
         
        return []
        
    def __getCronJobMessage(self, cronMessageParts = [], appendToMessages = True):
        
        if (len(cronMessageParts) == 0 or len(cronMessageParts) < 3):
            message = ' N/A'
        
        else:
            message = self.__formatTwoDigits(cronMessageParts[0]) + ':' + self.__formatTwoDigits(cronMessageParts[1]) + ' ' + self.__whichDay[cronMessageParts[2]]

        if appendToMessages : self.__messages.append(message)
        
        return message
    
    def __formatTwoDigits(self, message):
        
        if (message < 10) : return '0' + str(message)
        
        return str(message)