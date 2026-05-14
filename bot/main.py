import time
from controller import ADBController
from vision import Vision
from tasks import BotTasks
from account_setup import AccountSetup

def main():
    print("Initializing Pokemon TCG Pocket Bot...")
    
    # Initialize ADB wrapper
    # Replace 'emulator-5554' with your specific device ID if necessary
    adb = ADBController(device_id=None) 
    
    # Initialize OpenCV vision wrapper
    vision = Vision(template_folder="templates")
    
    # Initialize Tasks wrapper
    tasks = BotTasks(adb, vision)

    # Initialize Account Setup module
    account_setup = AccountSetup(adb, vision)

    print("Checking ADB connection...")
    # Basic ping test
    # If using Nox, Bluestacks, etc., might need adb connect 127.0.0.1:port first
    
    while True:
        print("\nSelect a task:")
        print("1. Farm Solo Battles")
        print("2. Claim Missions")
        print("3. Create & Link New Google Account")
        print("4. List Created Accounts")
        print("5. Exit")
        choice = input("Choice: ")
        
        if choice == "1":
            tasks.farm_solo_battle()
        elif choice == "2":
            tasks.claim_missions()
        elif choice == "3":
            tasks.link_google_account(account_setup)
        elif choice == "4":
            account_setup.list_accounts()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
