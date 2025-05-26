import os
from datetime import datetime 


#####################################
##### DEV PROGRAM LOGS FUNCTION #####
#####################################
def write_log(message, key):
    match (key.strip().lower()): 
        case 'e':###CREATE ERRORLOG###
            logfile = os.path.join(os.getcwd(),"logs","errorlog.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###ERROR###| {message} |###{datetime.now()}###")
                
        case 's':###CREATE SESSION LOG####
            logfile = os.path.join(os.getcwd(),"logs","sessionlog.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###SESSION-NOTIF###| {message} |###{datetime.now()}###")
                
        case 'u':###CREATE USERLOG####
            logfile = os.path.join(os.getcwd(),"logs","userlog.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###USERLOGS###| {message} |###{datetime.now()}###")


    
##################################
##### Saves User Credentials #####
##################################

class userinfo:
    def __init__(self, email,password,username):
        self.password = password
        self.username = username
        self.email = email
        self.credentials = (self.email, self.password, self.username)
    def displayinfo(self):
        print("Displaying Login Credentials \n")
        print(f"Password: {self.password} | Username: {self.username} | Email: {self.email}") 


#####################################################
##### Requires program to wait for page to load #####
#####################################################
async def wait():
    await asyncio.gather(
    page.wait_for_load_state('load'),
    page.click('#some-button')
    )