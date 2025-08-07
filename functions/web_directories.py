import os
from SC_Functions import write_log as log

###########################################
##### Social Media OBJECT declaration #####
###########################################
"""
 https://www.instagram.com/direct/inbox/
 https://www.instagram.com/zephyadonai/followers/
 await page.get_by_role("link", name="New post Create").click()
 await page.get_by_role("link", name="Post Post").click()
 await page.get_by_role("button", name="Select from computer").click()
 if await page.is_visible('selector-for-2fa-element'):
 await page.wait_for_selector("#2fa-code", timeout=5000)  # 5 sec timeout
"""

    #page.get_by_role("textbox", name="Phone number, username, or").click()
    #page.get_by_role("textbox", name="Password").click()

#######################################
##### SocialMedia object creation #####
#######################################
class SM_Object:
    ##########################
    ## Variable Declaration ##
    ##########################
    def __init__(self,
            webdir,
            userbox,
            passbox, 
            submitbox, 
            tfactor,
            tfs, 
            inbox,
            ):
        #########################################################################################
        #These are mainly selector and button values, to be targeted/filled by userinput later.#/
        #######################################################################################/
        #The object will be directly imported from its file to prevent excessive referencing.#/
        #####################################################################################/
        self.values = {
            "webdir": webdir,
            "username": userbox,
            "password": passbox,
            "submit":(submitbox, tfs),
            "2factor":tfactor,
            "inbox": inbox
            
        }
        self.saved_sessions = []
    #############################
    ### Manage login sessions ###
    #############################
    def save_session(self):
        log("NEW SESSION: Choosing name for session...", "u")
        s_name = input("Enter a name for your session file [NO EXTENSION REQUIRED]: ").strip()
        log("NEW SESSION: Managing and confirming directory of [sessions] folder...", "s")
        folder = "./sessions"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{s_name}.json")
        self.saved_sessions.append(path)
        log("NEW SESSION: Directory and session name confirmed. ", "s")
        return path
    def view_sessions(self):
        print("Saved Sessions:")
        for session in self.saved_sessions:
            print(session)

        
#######################
### INSTAGRAM OBJECT###
#######################3
instagram = SM_Object(
    "https://www.instagram.com/",
    "Phone number, username, or", 
    "Password",
    "Log in",
    "Security Code",
    "Confirm",
    "https://www.instagram.com/direct/inbox/"
    
)

#"https://www.instagram.com/accounts/login/two_factor?next=%2F"