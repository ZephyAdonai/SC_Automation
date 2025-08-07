import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect
import time as t
from SC_Functions import write_log as log
from SC_Functions import userinfo
from web_directories import instagram as instagram
##############################################
##### Creates and saves user credentials #####
##############################################
def credentials():
    
    log("NEW SESSION: Retrieving credentials...", "s")
    
    while True:
        email = input("Insert Email: ")
        pw = input("Insert Password: ")
        un = input("Insert Username: ")
        confirm = input("Are these the right credentials? (YES/NO): ").lower().strip()
        
        match confirm:
            case 'no':
                print("Retrying credentials... \n")
            case 'yes':
                print("Credentials confirmed")
                creds = userinfo(email,pw,un)
                log("NEW SESSION: User credentials saved.", "s")
                return creds
            case _:
               print("Invalid Input, try again.")

##########################################
##### Creates and save login session #####
##########################################
async def create_Session(playwright: Playwright, info, media) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(media.values["webdir"])
    await page.get_by_role("textbox", name=media.values["password"]).fill(info.pw)
    await page.get_by_role("textbox", name=media.values["username"]).fill(info.user)
    
    try:
        await page.get_by_role("button", name=media.values["submit"][0], exact=True).click()
    except:
            log("NEW SESSION: USER HAS ENTERED INVALID CREDENTIALS", "e")
            
    #############################################
    ##### Two-Factor Authentification check #####
    #############################################       
    try:
        
        log("NEW SESSION: Processing Two-Factor Authentication...", "u")
        
        await page.get_by_role("textbox", name=media.values["2factor"]).click()
        auth_dir = "https://www.instagram.com/accounts/onetap/?next=%2F"
        
        while True:
            code = input("Retrieve your 2FA code by phone/2FA App: ")
            
            if code.isdigit():
                await page.get_by_role("textbox", name=media.values["2factor"]).fill(code)
                await page.get_by_role("button", name=media.values["submit"][1]).click()
                await page.wait_for_load_state("load")
                
                log("NEW SESSION: Verifying 2FA code...", "s")
                
                await asyncio.sleep(5)
                if page.url.startswith(auth_dir):
                    break
                else:
                    print("Incorrect Code. Please try again.")
                    
                    log("NEW SESSION: User has provided the incorrect 2FA Code, retrying...", "u")

            elif not code.isdigit():
                print("The code is digit based. Please only enter numbers.")
                
                log("NEW SESSION: User provided an invalid input, retrying...", "u")
                
                #await page.goto("https://www.instagram.com/accounts/onetap/?next=%2F")
    except:
        
        log("NEW SESSION: Two-Factor Authentication is not enabled", "s")
        
    finally:
        if media.values["webdir"] == "https://www.instagram.com/":
            await page.get_by_role("button", name="Save info").click()
            #await page.get_by_role("link", name="Direct messaging", exact=False).click()
            #await page.get_by_role("button", name="Not Now").click()
            session = instagram.save_session()
            await context.storage_state(path=session)
            
            log(f"NEW SESSION: Successfuly created new session. [Ref({session})]", "s")
            
    #    await page.get_by_role("button", name="Send message").click()
    #    await page.get_by_role("textbox", name="To:").click()
    #    await page.get_by_role("button", name="test1").click()
    #    await page.get_by_role("button", name="Chat").click()
    #    await page.get_by_text("Choose an emojiMessage...").click()
    #    await page.get_by_text("Choose an emojiMessage...").click()
    #    await page.get_by_role("textbox", name="Message").fill("test1")

    # ---------------------
    await context.close()
    await browser.close()


async def user_session(info, media) -> None:
    async with async_playwright() as playwright:
        await create_Session(playwright, info, media)
        
def create_session():
    try:
        selectmedia = int(input("[ 1 - Instagram | 2 - Twitter | 3 - Tiktok ]: "))
        info = credentials()
        print("System logging in....")
    except:
        log("User response was an invalid input.", "e")
        print("Invalid Input. ")
    else:
        match selectmedia:
            case 1:
                asyncio.run(user_session(info, instagram))
    
create_session()
#https://www.instagram.com/direct/inbox/
#https://www.instagram.com/zephyadonai/followers/
# await page.get_by_role("link", name="New post Create").click()
# await page.get_by_role("link", name="Post Post").click()
# await page.get_by_role("button", name="Select from computer").click()
# if await page.is_visible('selector-for-2fa-element'):
# await page.wait_for_selector("#2fa-code", timeout=5000)  # 5 sec timeoutwe