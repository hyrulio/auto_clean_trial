#!/usr/bin/env python3
import os
import sys

if os.geteuid() != 0:
    print("\n[!] ACCESS DENIED")
    print("P.U.R.G.E requires admin (administrator) privileges to clean system logs and varias files")
    print("Please run: 'sudo python3 purge.py' or make/edit your alias to include 'sudo' at the start")
    print("Sorry for the inconvenience and hope you return with proper permissions")
    sys.exit()

def find_browser_path(folder_name):
    print(f"[Searching] Looking for folder: {folder_name}..")
    home = os.path.expanduser("~")
    neighborhoods = [
        os.path.join(home, ".config"),
        os.path.join(home, ".cache"),
        os.path.join(home, ".var/app")
    ]
    for spot in neighborhoods:
        if not os.path.exists(spot):
            continue
        
    for root, dirs, _ in os.walk(spot):
        for directory in dirs:
            if folder_name.lower() in directory.lower():
                full_path = os.path.join(root, directory)
                
                print(f"[Found] Path discovered: {full_path}")
                return full_path
    
    print(f"[!] Could not find {folder_name} in .config or .cache")
    return None
    
warned_user = False
storage_to_clean = []
browser_to_clean = []
media_to_clean = []
safe_storage = ["Temporary Files", "Thumbnail Cache"]
safe_browser = ["Cache"]
safe_media = ["Trash Bin", "Broke Symlinks"]
auto_clean = ["safe_storage", "safe_browser", "safe_media"]
print("Programmed Utility for Regular Garbage Elimination")
print("                     P.U.R.G.E                    ")
print("")
mode = input("Customize cleanup? (y/n): ").lower().strip()

while mode != 'y' and mode != 'no':
    if not warned_user:
        print("\n[!] Invalid input.")
        print("Please type 'y' to custmize or 'no' for automatic")
        warned_user = True
    mode = input("Try again (y/no): ").lower().strip()
        
if mode == 'no':
    print("Automatic..")
    storage_to_clean = safe_storage.copy()
    browser_to_clean = safe_browser.copy()
    media_to_clean = safe_media.copy()
if mode == 'y':
    print("\n 1; Storage Options")
    print("1) Temporary Files\n2) System Logs\n3) Thumbnail Cache")
    
    choices1 = input("Select numbers (e.g, 1 3): ").split()
    
    if not choices1:
        storage_to_clean = safe_storage.copy()
    elif '0' in choices1:
        storage_to_clean = []
    else:
        if '1' in choices1:
            storage_to_clean.append("Temporary Files")
        if '2' in choices1:
            storage_to_clean.append("System Logs")
        if '3' in choices1:
            storage_to_clean.append("Thumbnail Cache")
    
    print("\n 2; Browser Options")
    print("1) History\n2) Cookies\n3) Cache")
    
    choices2 = input("Select numbers: ").split()
    
    if not choices2:
        browser_to_clean = safe_browser.copy()
    elif '0' in choices2:
        browser_to_clean = []
    else:
        if '1' in choices2:
            browser_to_clean.append("History")
        if '2' in choices2:
            browser_to_clean.append("Cookies")
        if '3' in choices2:
            browser_to_clean.append("Cache")
    
    print("\n 3; Media Options")
    print("1) Trash Bin\n2) Broke Symlinks\n3) Old Downloads\n4) Large Log Files")
    
    choices3 = input("Select numbers: ").split()
    
    if not choices3:
        media_to_clean = safe_media.copy()
    elif '0' in choices3:
        media_to_clean = []
    else:    
        if '1' in choices3:
            media_to_clean.append("Trash Bin")
        if '2' in choices3:
            media_to_clean.append("Broke Symlinks")
        if '3' in choices3:
            media_to_clean.append("Old Downloads")
        if '4' in choices3:
            media_to_clean.append("Large Log Files")
            
print("\n" + "="*40)
print("P.U.R.G.E Final Report")
print("="*40)

if mode == 'no':
    print("Selected Mode: Safe Automatic Cleanup")
else:
    print("Selected Mode: Custom Cleanup")
    
print(f"\n[Storage]: {', '.join(storage_to_clean)}")
print(f"[Browser]: {', '.join(browser_to_clean)}")
print(f"[Media]: {', '.join(media_to_clean)}")
print("="*40)

confirm = input("\nDo these look correct? (yes/no): ").lower().strip()

if confirm == "yes":
    print("\n[!] Initiating Cleanup..")
    
    if "Temporary Files" in storage_to_clean:
        print("Clearing temporary files..")
        os.system('sudo rm -rf /tmp/*')
    if "System Logs" in storage_to_clean:
        print("Deleting system logs..")
        os.system('sudo rm -rf /var/log*.log')
    if "Thumbnail Cache" in storage_to_clean:
        print("Wiping thumbnails..")
        os.system('sudo rm -rf ~/.cache/thumbnails/*')
        
        print("Storage wipe complete")
            
    if browser_to_clean:
        user_browser = input("\nEnter browser name for cleaning: ").strip()
        discovered_path = find_browser_path(user_browser)
        
        if discovered_path:
            sub_paths = {
                "History": "Default/History",
                "Cookies": "Default/Cookies",
                "Cache": "Default/Cache"
            }
            
            for option in browser_to_clean:
                if option in sub_paths:
                    target = os.path.join(discovered_path, sub_paths[option])
                    if os.path.exists(target):
                        print(f" -> finding {option}..")
                        if option == "Cache":
                            os.system(f'rm -rf {target}/*')
                        else:
                            os.system(f'rm -f {target}')
                            
            print("Browser clean complete")
    
    if "Trash Bin" in media_to_clean:
        print("Clearing trash bin..")
        os.system("sudo rm -rf ~/.local/share/Trash/*")
    if "Broke Symlinks" in media_to_clean:
        print("Tossing broken symlinks..")
        os.system("sudo find ~/ -xtype l -delete")
    if "Old Downloads" in media_to_clean:
        print("Erasing old downloads..")
        os.system("sudo find ~/Downloads -mtime +30 -delete")
    if "Large Log Files" in media_to_clean:
        print("Deleting large log files..")
        os.system("sudo find /var/log -size +50M -delete")
    
    print("\nDone: Your system P.U.R.G.E is completed")
else:
    print("\nCleanup aborted, No files were harmed")