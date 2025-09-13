####################################
import os
from datetime import datetime 
import asyncio
import sqlite3 as sql

###################################

def fetch_session(username):
    with sql.connect("user_data.db") as conn:
        db = conn.cursor()
        db.execute("SELECT session FROM users WHERE username = ?", (username,))
        ses = db.fetchone()

    return ses[0]

def fetch_user(username):
    with sql.connect("user_data.db") as conn:
        db = conn.cursor()
        db.execute(f"SELECT username FROM users WHERE username = ?", (username,))
        user = db.fetchone()
    
    return user[0]

def add_data(username, password, session):
    with sql.connect("user_data.db") as conn:
        db = conn.cursor()
        db.execute("INSERT INTO users (username, password, session) VALUES (?, ?, ?)",(username, password, session))

def select_login():
    with sql.connect("user_data.db") as conn:
        db = conn.cursor()
        db.execute(
            """
            SELECT username FROM users
            
            """
        )
    users = db.fetchall()
    print("Available sessions:")
    users = [user[0] for user in users]
    for user in users:
        print(user)
    while True:
        choice = input("""
                    Please select the account you wish to automate.

                    TYPE THE USERNAME OF THE ACCOUNT: 
                    """)
        if choice in users:
            return choice
        else:
            print("Please try again.")

    



#####################################
##### DEV PROGRAM LOGS FUNCTION #####
#####################################
def write_log(message, key):
    match (key.strip().lower()): 
        case 'e':###CREATE ERRORLOG###
            logfile = os.path.join(os.getcwd(),"logs.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###ERROR###| {message} |###{datetime.now()}###")
                
        case 's':###CREATE SESSION LOG####
            logfile = os.path.join(os.getcwd(),"logs.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###SESSION-NOTIF###| {message} |###{datetime.now()}###")
                
        case 'u':###CREATE USERLOG####
            logfile = os.path.join(os.getcwd(),"logs.txt")
            with open(logfile, "a") as log:
                log.write(f"\n###USERLOGS###| {message} |###{datetime.now()}###")


    
##################################
##### Saves User Credentials #####
##################################

class userinfo:
    def __init__(self,email,password,username):
        self.pw = password
        self.user = username
        self.email = email
        self.credentials = (self.email, self.pw, self.user)
    def displayinfo(self):
        print("Displaying Login Credentials \n")
        print(f"Password: {self.pw} | Username: {self.user} | Email: {self.email}") 


#####################################################
##### Requires program to wait for page to load #####
#####################################################
async def wait(page):
    await asyncio.gather(
    page.wait_for_load_state('load'),
    page.click('#some-button')
    )
    
    
#########################
##### Get User-List #####
#########################
async def get_users(page):
    await page.wait_for_selector('div[role="dialog"]', timeout=10000)
    follower_elements = page.locator('div[role="dialog"] a[href^="/"][tabindex="0"]')
    follower_links = await follower_elements.evaluate_all('''elements => elements.map(el => el.getAttribute('href').replace('/', ''))''')
    seen = set()
    followers = []
    for f in follower_links:
        if (f and f.strip() and 
            not f.startswith('?') and 
            not f.startswith('http') and
            f not in seen):
            seen.add(f)
            followers.append(f.strip())
    return followers