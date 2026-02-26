#!/usr/bin/env python3
import os
import sys
import shutil
import pwd
import time

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
    
    username = os.environ.get('SUDO_USER') or os.getlogin()
    user_home = f"/home/{username}"
    trash_path = f"{user_home}/.local/share/Trash"
    thumb_path = f"{user_home}/.cache/thumbnails"

    if "Temporary Files" in storage_to_clean:
        print("Clearing temporary files..")
        tmp_path = '/tmp'
        for item in os.listdir(tmp_path):
            item_path = os.path.join(tmp_path,item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception:
                continue
    print("Temporary files cleared")
    if "System Logs" in storage_to_clean:
        print("Emptying system logs..")
        log_dir = "/var/log"
        for root, _, files in os.walk(log_dir):
            for file in files:
                if file.endswith(".log") or ".log." in file:
                    log_path = os.path.join(root, file)
                    try:
                        with open(log_path, 'w') as f:
                            pass
                    except PermissionError:
                        continue
                    except Exception as e:
                        print(f"Some are best left untouched")
    print("Logs emptied")
    if "Thumbnail Cache" in storage_to_clean:
        thumb_path = f"/home/{username}/.cache/thumbnails"
        print("Wiping thumbnail cache..")
        if os.path.exists(thumb_path):
            try:
                shutil.rmtree(thumb_path)
                os.makedirs(thumb_path)
                user_info = pwd.getpwnam(username)
                os.chown(thumb_path, user_info.pw_uid, user_info.pw_gid)
                print("Thumbnail cache wiped")
            except Exception as e:
                print(f"Thumbnails can't be cleaned: {e}")    
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
        username = os.environ.get('SUDO_USER') or os.getlogin()
        trash_path = f"/home/{username}/.local/share/Trash"        
        print("Clearing trash bin..")
        
        if os.path.exists(trash_path):
            user_info = pwd.getpwnam(username)
            for subfolder in ["files", "info"]:
                target = os.path.join(trash_path, subfolder)
                if os.path.exists(target):
                    shutil.rmtree(target)
                    os.makedirs(target)
                    os.chown(target, user_info.pw_uid, user_info.pw_gid)
                    print("Trash wipe complete")
                else:
                    print(f"Could not find trash at {trash_path}")
    if "Broke Symlinks" in media_to_clean:
        search_path = f"/home/{username}"
        print("Finding broken symlinks, this may take a moment")
        broken_count = 0
        for root, dirs, files in os.walk(search_path):
            for name in files + dirs:
                full_path = os.path.join(root, name)
                if os.path.islink(full_path):
                    if not os.path.exists(os.readlink(full_path)):
                        print("Tossing Broken Symlinks..")
                        try:
                            os.unlink(full_path)
                            broken_count += 1
                        except Exception:
                            continue
            print(f"Tossed {broken_count} symlink(s)")
    if "Old Downloads" in media_to_clean:
        download_path = f"{user_home}/Downloads"
        kill_list = [".deb", ".gz", ".zip", ".tar.gz"]
        print("Finding old install and archive files (.deb, .gz, etc)..")
        seconds_in_30_days = 30 * 24 * 60 * 60
        current_time = time.time()
        deleted_count = 0
        if os.path.exists(download_path):
            for root, _, files in os.walk(download_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    file_ext = os.path.splitext(name)[1].lower()
                    if file_ext in kill_list:
                        file_age = os.path.getmtime(file_path)
                        if (current_time - file_age) > seconds_in_30_days:
                            try:
                                os.remove(file_path)
                                deleted_count += 1
                            except Exception:
                                continue
        print(f"Cleaned out {deleted_count} file(s)")
    if "Large Log Files" in media_to_clean:
        print("Finding large log files..")
        log_dir = "/var/log"
        size_threshold = 50 * 1024 * 1024
        large_log_count = 0
        for root, _, files in os.walk(log_dir):
            for file in files:
                log_path = os.path.join(root, file)
                try:
                    if os.path.getsize(log_path) > size_threshold:
                        with open(log_path, 'w') as f:
                            f.truncate(0)
                        large_log_count += 1
                except (PermissionError, FileNotFoundError):
                    continue
                except Exception as e:
                    continue
        print(f"Successfully cleared {large_log_count} large log file(s)")
    
    print("\nDone: Your system P.U.R.G.E is completed")
else:
    print("\nCleanup aborted, No files were harmed")
