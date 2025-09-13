import utils.web_directories as wb
import utils.SC_automations as sca
import utils.SC_functions as scf

print("""
      [_S_OCIAL _A_UTOMATIONS]
      """)
while True:
      print("""

      1 - START NEW SESSION | You will be asked to give and confirm credentials, the program saves your session and username locally. 
      2 - SELECT ACCOUNT | Select an account with a saved session. You can then prompt a message to your followers or empty your content folder.
      3 - EXIT | Exits the program. 
      
            """)
      choice_ = int(input(">>> "))
      try:
            match choice_:
                  case 1:
                        sca.create_session()
                  case 2:
                        user = scf.select_login()
                        if user:
                              print("""
                                    
                                    Please select an automation.
                                    
                                    1 - EMPTY CONTENT FOLDER | The program will post all content within your folder. 
                                    2 - MESSAGE FOLLOWERS | The program will message a selected number of your followers.
                                    
                                    """)
                              match user:
                                    case 1:
                                          sca.post_content(user)
                                    case 2:
                                          sca.auto_message(user)
                  case 3:
                        break
      except:
            scf.write_log("UNKOWN ERROR OCCURED", "e")