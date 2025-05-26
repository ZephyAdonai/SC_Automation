import os

#######################################
##### SocialMedia object creation #####
#######################################
class SM_Object:
    def __init__(self, logindir, userbox, passbox, submitbox):
        self.logindir = logindir
        self.userbox = userbox
        self.passbox = passbox
        self.submitbox = submitbox
        # For login session management
        self.saved_sessions = []
    #############################
    ### Manage login sessions ###
    #############################
    def save_session(self,session):
        session_check = os.path.join(os.getcwd(), f"{session}.json")
        print(f"Saving session [{session}.json]...")
        self.saved_sessions.append(session)
        print(f"Saved session [{session}.json] ")
    