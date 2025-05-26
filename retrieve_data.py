from playwright.sync_api import Playwright, sync_playwright, expect
import time as t


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
    
async def wait():
    await asyncio.gather(
    page.wait_for_load_state('load'),
    page.click('#some-button')
    )

##########################################
##### Creates and save login session #####
##########################################


def usercs():
    switch = True 
    while switch:
        email = input("Insert Email: ")
        pw = input("Insert Password: ")
        un = input("Insert Username: ")
        confirm = input("Are these the right credentials? (YES/NO)").lower().strip()
        match confirm:
            case 'no':
                print("Retrying credentials... \n")
            case 'yes':
                print("Credentials confirmed")
                info = userinfo(email,pw,un)
                switch = False
                return info
            case _:
               print("Invalid Input")
    def run(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/")
        wait()
        page.get_by_role("textbox", name="Phone number, username, or email").fill("greenstreet56713@gmail.com")
        wait()
        page.get_by_role("textbox", name="Password").click()
        page.get_by_role("textbox", name="Password").fill("loveall1")
        wait()
        page.get_by_role("textbox", name="Password").click()
        page.keyboard.press("Enter")
        wait()
        code = input("Please insert authentication code: ")
        wait()
        page.get_by_role("textbox", name="Security Code").fill(code)
        wait()
        page.get_by_role("button", name="Confirm").click()
        wait()
        filename = input("Choose a name for the login session.")                        
        context.storage_state(path=f"session.{filename}")  # Saves login session to a file
        print("Session saved!")                 
        
        context.close()
        browser.close()
    
    with sync_playwright() as playwright:
        run(playwright) 
        
        
def login_to_website(url, username, password):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        wait()
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        wait()
        # Add any additional steps for 2FA or other actions here
        context.storage_state(path="session.json")
        browser.close()
        
login_to_website("https://www.instagram.com/accounts/login/", "your_username", "your_password")

