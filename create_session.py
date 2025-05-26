from playwright.sync_api import Playwright, sync_playwright, expect
import time as t
import SC_Functions as scf

##########################################
##### Creates and save login session #####
##########################################


def usercs():
    scf.write_log("NEW SESSION: Retrieving credentials...", "s")
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
                info = scf.userinfo(email,pw,un)
                switch = False
                scf.write_log("NEW SESSION: User credentials saved.", "s")
                return info
            case _:
               print("Invalid Input, try again.")
    def run(playwright: Playwright) -> None:
        
        scf.write_log("NEW SESSION: Creating login session... ", "s")
        
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com/accounts/login/#")
        scf.wait()
        page.fill('input[name="username"]', scf.userinfo.username)
        page.fill('input[name="password"]', scf.userinfo.password)
        page.click('button[type="submit"]')
        scf.wait()
        
        code = input("Please insert authentication code: ")
        scf.wait()
        page.get_by_role("textbox", name="Security Code").fill(code)
        
        scf.wait()
        page.get_by_role("button", name="Confirm").click()
        scf.wait()
        
        filename = input("Choose a name for the login session.")                        
        context.storage_state(path=f"{filename}.json")  # Saves login session to a file
        
        print(f"Session created | {filename}.json") 
        scf.write_log(f"NEW SESSION: Loggin session created [{filename}.json]", "s")                
        
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
        scf.wait()
        page.fill('input[name="username"]', scf.userinfo.username)
        page.fill('input[name="password"]', scf.userinfo.password)
        page.click('button[type="submit"]')
        scf.wait()
        # Add any additional steps for 2FA or other actions here
        context.storage_state(path="session.json")
        browser.close()
        
login_to_website("https://www.instagram.com/accounts/login/", "your_username", "your_password")

usercs()

