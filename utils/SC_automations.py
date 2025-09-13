import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect
import time as t
import utils.SC_functions as scf
from utils.SC_functions import write_log as log
from utils.SC_functions import userinfo
from utils.SC_functions import get_users 
from utils.web_directories import instagram as instagram
import random as r
import os
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


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
async def create_ses(playwright: Playwright, info, media) -> None:
    browser = await playwright.chromium.launch(headless=True)
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
        auth_dir = "https://www.instagram.com/accounts"
        
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
            print(f"Created session for {info.user}.")
            
            ###Adds into local-stored database.###
            scf.add_data(info.user, info.pw, session)

    # ---------------------
    await context.close()
    await browser.close()


async def user_session(info, media) -> None:
    async with async_playwright() as playwright:
        await create_ses(playwright, info, media)
        
def create_session():
    try:
        print("Currently the program is instagram based. Will expand to other social media in the future.")
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
    
#######################################################
##### DM followers with a message of user choice. #####
#######################################################

async def message_followers(playwright: Playwright, username, media, msg, msg_count,) -> None:
    session = scf.fetch_session(username) 
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(storage_state=session)
    page = await context.new_page()
    
    log(f"USER MESSAGE: {msg} ", "u")

    user = scf.fetch_user(username)
    if media is instagram:
        await page.goto(f"{media.values['webdir']}{user}")
        await page.get_by_role("link", name="followers").click()
        
        await page.wait_for_timeout(3000)
        await page.wait_for_selector('div[role="dialog"]', timeout=10000)
        
        log("INITIATED AUTOMATION : MESSAGING FOLLOWERS","s")
        
        scroll = page.locator("div.x6nl9eh")
        for _ in range(5):
            await scroll.evaluate("el => el.scrollBy(0, 500)")
            await page.wait_for_timeout(1000)
        
        messaged = []
        followers = await get_users(page)
        for user in followers[:msg_count]:
            user = r.choice(followers)
            if user not in messaged:
                print(f"Now messaging... {user}")
                await page.goto(f"{media.values["webdir"]}/{user}", timeout=5000)
                
                ##################################################
                ### Checks if the user's profile is available. ###
                ################################################## 
                test = await page.wait_for_selector('role=button[name="Options"]', timeout=5000)
                if test:
                    print(f"Found {user} profile.")    
                    try:
                        await page.get_by_role("button", name="Message", exact=True).click(timeout=10000)
                        print(f"Entering Messages...")
                        t.sleep(1)
                        await page.get_by_role("textbox", name="Message").fill(msg)
                        t.sleep(1)
                        await page.get_by_role("button", name="Send").click()
                        
                        log(f"MESSAGED USER: {user}", "s")
                        print(f"Sent message to {user}.")
                        
                    except PlaywrightTimeoutError:
                        log(f"{user} Doesn't follow {username}, Finding Message Button in Options...", "s")
                        print(f"messaging: {user}")
                        await page.get_by_role("button", name="Options").click(timeout=10000)
                        
                        await page.get_by_role("button", name="Send").click()
                        t.sleep(1)
                        
                        await page.get_by_role("textbox", name="Message").fill(msg)
                        print(f"Entering Messages...")
                        t.sleep(1)
                        
                        await page.get_by_role("button", name="Send").click()
                        print(f"Sent message to {user}.")
                        
                    except Exception as e:
                        print("Unexpected error", e )
                    messaged.append(user)
                    
                    log(f"Successfuly messaged {user}", "s")
                    
    # ---------------------
    await context.close()
    await browser.close()


async def message(username, media, msg, msg_count) -> None:
    async with async_playwright() as playwright:
        await message_followers(playwright, username, media, msg, msg_count)
        
def auto_message(username):
    try:
        msg = input("What would you like to send your followers?: ")
        count = int(input("How many followers do you want to message?: "))
        print("System logging in....")
    except:
        log("User response was an invalid input.", "e")
        print("Invalid Input. ")
    else:
                asyncio.run(message(username, instagram, msg, count))
                
############################################################
### Posts all the content within folder every six hours. ###
############################################################
async def post(playwright: Playwright, content_folder, username) -> None:
    
    #############################################################################
    # Fetches data that matches the username involved with the current session. #
    #############################################################################
    session = scf.fetch_session(username)
    
    if session:
        log(f"NOW EMPTYING CONTENT FOLDER INTO ACCOUNT - {username}....", "s")

        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=session)
        page = await context.new_page()
        
        ###Builds the full pathing of the file to post###
        
        log(f"SYSTEM FOUND [{len(os.listdir(content_folder))}] FILE(S) IN CONTENT FOLDER", "s")
        
        for content in os.listdir(content_folder):
            file = os.path.join(content_folder, content)
            
            print(content)
            await page.goto("https://www.instagram.com/")
            t.sleep(3)
            await page.get_by_role("link", name="New post Create").click(timeout=5000)
            await page.get_by_role("link", name="Post Post").click()
            
            ###Prompts Playwright to find the hidden set_file value###
            async with page.expect_file_chooser() as test:
                await page.get_by_role("button", name="Select from computer").click()
                
            ###Inserts content from content folder to post###
            input_box = await test.value
            await page.wait_for_timeout(3000)
            await input_box.set_files(file)
            
            await page.wait_for_timeout(3000)
            await page.get_by_role("button", name="Next").click(timeout=3000)
            await page.get_by_role("button", name="Next").click(timeout=3000)
            await page.get_by_role("textbox", name="Write a caption...").click(timeout=3000)
            caption = input("What would you like to add as a caption?: ")
            await page.get_by_role("textbox", name="Write a caption...").fill(f"""
                {caption}'
                
                [ AUTOMATED POST BY S_C AUTOMATIONS | Developed by ZephyAdonai ] 
                [Thank you for viewing this post, if you enjoyed it then I'm more grateful! :D ]
                
                """)
            await page.get_by_role("button", name="Share", exact=True).click()
            await page.wait_for_timeout(10000)
            await page.get_by_role("button", name="Close").click()
            log(f"POSTED FILE {content} ON ACCOUNT - {username}", "s")
            if os.path.exists(file):
                log(f"REMOVING FILE [{content}]", "s")
                os.remove(file)
    else:
        log("USER-SESSION DOES NOT EXIST", "e")


    # ---------------------
    await context.close()
    await browser.close()


async def auto_post(content_folder, username) -> None:
    async with async_playwright() as playwright:
        await post(playwright, content_folder, username)

        
def post_content(username):
    try:
        content_folder = os.path.join(os.getcwd(), "content")
        asyncio.run(auto_post(content_folder, username))
    except Exception as e:
        print("unexpected error", e)