class CronShedulerParser:
    
    cronjobs = []
    cronTime = None
    _whichDay = { True: 'today', False: 'tomorrow' }
    _cronTimeHour = None
    _cronTimeMinute = None
    _delimiter = ' '
    _messages = []
    
    def __init__(self, cronjobs = [], cronTime = None):
        self.cronjobs = cronjobs
        self.cronTime = cronTime
        self._cronTimeHour, self._cronTimeMinute = self._getCronTimeParts()

    def setDelimiter(self, delimiter):
        self._delimiter = delimiter
        
    def getDelimiter(self):
        return self._delimiter
        
    def processCronJobs(self):
        
        if (len(self.cronjobs)> 0):
            for current in self.cronjobs:
                nextCronTime = self._parseCronJob(current)
                nextCronTimeMessage = self._getCronJobMessageTime(nextCronTime)
    
    def getMessages(self):
        return self._messages
    
    def _validateInputs(self, hour, minute):
        
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
        
    def _getCronTimeParts(self):
        
        if type(self.cronTime) != type(None):
            cronTimeParts = self.cronTime.split(':')
            return [
                int(cronTimeParts[0]),
                int(cronTimeParts[1])
                ]
        else:
            return [None, None]
        
    def _parseCronJob(self, cronLine):
        
        cronLine = cronLine.strip()
        
        if(len(cronLine) > 0):
                                        
            if cronLine.find(self._delimiter) > -1:
                
                info = cronLine.split(self._delimiter)
                
                if (len(info) >= 3):
                                            
                    nextCronTime = self._getCronNextTime(
                        hour = int(info[1]) if info[1].isdigit() else info[1],
                        minute =  int(info[0]) if info[0].isdigit() else info[0]
                        )
            
                    return nextCronTime
                            
        else:
            return []
                        
    def _getCronNextTime(self, hour = '*', minute = '*'):
        
        if self._validateInputs(hour, minute) is False:
            return []
        
        # * *
        if (hour == '*' and minute == '*'):
            return [self._cronTimeHour, self._cronTimeMinute, True]

        # 45 *
        if (hour == '*' and minute != '*'):
            
            if (int(minute) > self._cronTimeMinute):
                return([self._cronTimeHour, minute, True])
            
            if (int(minute) <= self._cronTimeMinute):
                #check if not passed midnight
                if(self._cronTimeHour + 1 >= 24):
                    return [0, minute, False]
                else:
                    return [self._cronTimeHour + 1, minute, True]
                
        # * 19
        if (hour != '*' and minute == '*'):
            
            #if hour passed, next day
            if (hour < self._cronTimeHour):
                return [hour, 0, False]
            
            if (hour > self._cronTimeHour):
                return [hour, 0, True]
            
            if (hour == self._cronTimeHour):
                if (self._cronTimeMinute == 59):
                    if (hour == 23):
                        return [hour, 0, False]
                    else:                        
                        return [hour + 1, 0, True]
                else:                        
                    return [hour,self._cronTimeMinute + 1, True]
                
        # 12 13
        if (hour != '*' and minute != '*'):
            
            if (hour == self._cronTimeHour):
                if (minute <= self._cronTimeMinute):
                    return [hour, minute, False]
                else:
                    return [hour, minute, True]
                
            if (hour < self._cronTimeHour):
                return [hour, minute, False]
            
            if (hour > self._cronTimeHour):
                return [hour, minute, True]
         
        return []
        
    def _getCronJobMessageTime(self, cronMessageParts = [], appendToMessages = True):
        
        if (len(cronMessageParts) == 0 or len(cronMessageParts) < 3):
            message = ' N/A'
        
        else:
            message = self._formatTwoDigits(cronMessageParts[0]) + ':' + self._formatTwoDigits(cronMessageParts[1]) + ' ' + self._whichDay[cronMessageParts[2]]

        if appendToMessages : self._messages.append(message)
        
        return message
    
    def _formatTwoDigits(self, message):
        
        if (message < 10) : return '0' + str(message)
        
        return str(message)