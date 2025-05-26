import re
from playwright.sync_api import Playwright, sync_playwright, expect
import random
import time as t



spam = "I don’t know if you’re new here, so I’ll let you off the hook this time. Using emojis is frowned upon here on this great site, and for good reason. Instagram normies often use them, and you don’t want to be a normie, do you? If I catch you using an emoji in the future, I’ll be forced to issue a downvote to your comment. Why should you care, you may ask? Well to begin, you will lose karma on your account, which is a useful social status tool and also a way to show others you know your way around Reddit. If you were to continue the use of emojis, I would be forced to privately message you about your slip-up. Any further offenses past that would leave me no other option than to report your account. I don’t think I have to explain why you don’t want that. But anyways, no harm done yet! Follow these simple rules and you’ll enjoy your future on Reddit! Have a blessed (and hopefully emoji-free) day, stranger."

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="session.insta")
    page = context.new_page()
    page.goto("https://www.instagram.com/")
    t.sleep(3)                                                
    page.goto("https://www.instagram.com/direct/inbox/")
    input("Press enter when you're in the chat of your victim.")
    
    count = 0
    
    while count < 500: #Change this value depening on how many messages you want to send, or rather how much you hate someone
        page.fill('div[role="textbox"][aria-label="Message"]', spam)
        t.sleep(0.2)
        page.keyboard.press("Enter")
        t.sleep(0.2)
        count += 1

    input("Press Enter to close the browser...")
    # ---------------------
    #context.close()
    #browser.close()
    
with sync_playwright() as playwright:
    run(playwright) 


##################################################################################################################

import re
from playwright.sync_api import Playwright, sync_playwright, expect
import random
import time as t

spam = "I don’t know if you’re new here, so I’ll let you off the hook this time. Using emojis is frowned upon here on this great site, and for good reason. Instagram normies often use them, and you don’t want to be a normie, do you? If I catch you using an emoji in the future, I’ll be forced to issue a downvote to your comment. Why should you care, you may ask? Well to begin, you will lose karma on your account, which is a useful social status tool and also a way to show others you know your way around Reddit. If you were to continue the use of emojis, I would be forced to privately message you about your slip-up. Any further offenses past that would leave me no other option than to report your account. I don’t think I have to explain why you don’t want that. But anyways, no harm done yet! Follow these simple rules and you’ll enjoy your future on Reddit! Have a blessed (and hopefully emoji-free) day, stranger."

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False )
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://discord.com/")
    page.get_by_role("link", name="Log In").click()
    t.sleep(5)                                                    #Insert your email
    page.get_by_role("textbox", name="Email or Phone Number*").fill("greenstreet56713@gmail.com")
    page.get_by_role("textbox", name="Password*").click() #Yo insert your password below this
    page.get_by_role("textbox", name="Password*").fill("zeph12345")
    page.get_by_role("button", name="Log In").click()
    t.sleep(5)
    page.get_by_role("button", name="Find or start a conversation").click()
    t.sleep(2)                                                #Example: WeOneUp | THIS IS NOT THE #ID, ITS THE USERNAME
    page.get_by_role("combobox", name="Quick switcher").fill("JayDaGoat")
    t.sleep(1)
    #################   RIGHT HERE   #################
    page.get_by_text("JayDaGoatjaythebest").click()
    #################  ^ You need to fill this value with their username and then their # ID. No space between #################
    # Example,  my user is ZephyAdonai, my # ID (below my username) is just zephyadonai, so you'd put ZephyAdonaizephyadonai
    t.sleep(1)
    page.get_by_role("textbox", name="Message @JayDaGoat").click()
    count = 0
    while count < 500: #Change this value depening on how many messages you want to send, or rather how much you hate someone
        page.fill('div[role="textbox"]', spam)
        t.sleep(0.2)
        page.keyboard.press("Enter")
        t.sleep(0.2)
        count += 1

    # ---------------------
    context.close()
    browser.close()
