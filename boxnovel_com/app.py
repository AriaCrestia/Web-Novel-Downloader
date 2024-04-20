try:
    # Import modules
    print("Importing modules...", end=" ")
    from bs4 import BeautifulSoup
    import os
    import requests
    print("Success.\n\n")
except ModuleNotFoundError as e:
    print(f"Error{e}")
    quit()
# end try

def CreateFolders():
    # Get home user path
    home_path = os.path.expanduser("~")
    # Create default directories
    try:
        os.mkdir(home_path + "/.crestiapps")
    except:  # noqa: E722
        pass
    try:
        os.mkdir(home_path + "/.crestiapps" + "/web_novel_downloader")
    except:  # noqa: E722
        pass
    save_dir = "/.crestiapps/web_novel_downloader/boxnovel"
    try:
        os.mkdir(home_path + save_dir)
    except:  # noqa: E722
        pass

def GetRelPath(folder_name: str):
    """
    Get the relative folder name.
    
    folder_name (str) : the folder name to be checked.
                        if the folder does not exist, it will be created.
                        if the folder name returned is invalid, an error will be raised and the program will end.
    """
    # Make start_pos global
    global start_pos
    # Get home user path
    home_path = os.path.expanduser("~")
    # Create default directories
    save_dir = "/.crestiapps/web_novel_downloader/boxnovel"
    download = "/" + folder_name
    
    try:
        # Create folder
        print("Creating download folder...", end=" ")
        os.mkdir(home_path + save_dir + download + "/")
        print("Success.")
        start_pos = 1
        return home_path + save_dir + download + "/"
    except FileExistsError:
        print("\nThe folder you entered already exists.")
        print("Process will continue in that folder.")
        print("WARNING: Some files may be overwritten")
        start_pos = int(input("Start download at chapter number: "))
        return home_path + save_dir + download + "/"
    except FileNotFoundError as e:
        print(e)
        print("\nThe folder name you entered has some invalid characters.")
        print("Please check the folder name again and input a valid name.")
        input("\nPress ENTER key to exit...")
    # end try

def GetChapter(url: str):
    """Function to get chapter from the url

    Args:
        url (str): the URL to the chapter.

    Returns:
        source_data: the data for the chapter.
    """
    try:
        # Fetch chapter data
        source_data = requests.get(url).content
        return source_data
    except requests.HTTPError:
        return False
    except requests.ConnectionError:
        print("\nInternet connection failed.")
        input("\nPress ENTER key to exit...")
    except requests.exceptions.MissingSchema:
        print("\nInvalid URL.")
        exit()
    # end try

def SaveChapter(path: str, name: str, ext: str, content):
    """Save the chapter data to a file.

    Args:
        path (str): The path whre the chapter will be saved.
        name (str): The name of the file.
        ext (str): The extension of the file.
        content (unknown): the chapter data to be written.
    """
    f = open(f"{path}{name}{ext}", "w")
    f.write(str(content))
    f.close()
    return True

########## Main program begins here ##########

CreateFolders()

## User input values
usr_url = str(input("Enter novel summary page URL: "))
usr_amount = int(input("Enter amount of chapters in novel: "))
usr_folder = str(input("Enter folder to save to: "))

print()

## Initialise values
ext = [".xhtml"]
ext_pos = 0
path = GetRelPath(usr_folder)
print()
count = start_pos - 1
failed = []


## Collection loop
while count < usr_amount:
    data = GetChapter(usr_url + "chapter-" + str(count + 1) + "/")
    # Record failures
    if not data:
        failed.append(usr_url + "chapter-" + str(count + 1) + "/")
        continue
    html_data = BeautifulSoup(data, 'html.parser')
    chapter = html_data.find('div', class_='reading-content')
    save = SaveChapter(path, "Chapter" + str(count + 1), ext[ext_pos], chapter)
    print("Chapter " + str(count + 1) + " finished successfully.", end="\r")
    count = count + 1

## End message
print("                                                                                                 ")
print("Process complete.")
if len(failed) > 0:
    print(str(len(failed)) + "chapter(s) failed.")
    print(failed)