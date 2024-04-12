import requests
import os
from bs4 import BeautifulSoup
import glob
import shutil

def GetRelPath(folder):
    """
    Get's the relative path and creates the folder to download images to.
    """
    # Get working dir
    absolute_path = os.path.dirname(__file__)
    rel_path = os.path.join(absolute_path, folder)
    try:
        # Create save folder
        print(f"Creating folder: {folder}...")
        os.mkdir(rel_path)
        print("Success.\n")
        return str(rel_path) + "/"
    except FileExistsError:
        # Folder exists error
        print("\nError: Folder already exists")
        print("Using pre-existing folder to download\n")
        return str(rel_path) + "/"
    except FileNotFoundError:
        # Invalid input error
        print("\nError: Invalid path")
        input("Press ENTER key to exit...")
        quit()

# class CreateEpub:
#     def CreateFolders():
#         pass
#     def CreateMimetype():
#         file_path = path + folder
#         f = open(f"{file_path}mimetype", "w")
#         f.write("application/epub+zip")
#         f.close()
#     def CreateIndex():
#         file_path = path + folder
#         f = open(f"{file_path}index.html", "w")
#         f.write(f"""<?xml version='1.0' encoding='utf-8'?>
#                 <html xmlns="http://www.w3.org/1999/xhtml">
#                 <head>
#                     <title>{usr_folder}</title>
#                 </head>
                
#                 <body>
                
#                 </body>
#                 </html>""")
#         f.close()
#     def MoveFilesTOCWrite():
#         source = path
#         destination = f"{path}{folder}{oebps_folder}{text_folder}"
#         # Get all files
#         all_files = glob.glob(os.path.join(source, '*Chapter*'), recursive=True)
#         amount = len(all_files)
#         print(f"{amount} files.")
#         # Write TOC file
#         file_path = path + folder
#         f = open("f{file_path}toc.xhtml")
#         f.write("""<?xml version='1.0' encoding='utf-8'?>
#                 <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
                
#                 <head>
#                     <title>Table of Contents</title>
#                     <style type="text/css">
#                     li
#                     {
#                         list-style-type: none;
#                         padding-left: 2em;
#                         margin-left: 0;
#                     }
#                     a
#                     {
#                         text-decoration: none;
#                     }
#                     a:hover
#                     {
#                         color: red;
#                     }
#                     </style>
#                 </head>
                
#                 <body>
#                     <h2>Table of Contents</h2>
                    
#                     <ul>
#                 """)
#         # Move file and write
#         for file_path in all_files:
#             dst_path = os.path.join(destination, os.path.basename(file_path))
#             shutil.move(file_path, dst_path)
#             f.write(f"       <li><a href='OEBPS/Text/Chapter {move_index}.xhtml'>Chapter {move_index}</a></li>\n\n")
#             move_index += 1
#             print(f"{file_path} moved successfully.")
#         f.write("""    </ul>
                
#                 </body>
                
#                 </html>""")
#         f.close()
        

# Get URL
summary_url = str(input("Summary page URL: "))
last_chap = int(input("Latest chapter number: "))
index = int(input("Start at chapter number: ")) - 1
move_index = index + 1
usr_folder = str(input("Save to folder: "))
path = GetRelPath(usr_folder)

failed = []

print("Starting...")
while index < last_chap:
    name = "Chapter " + str(index + 1) + ".xhtml"
    chap_link = summary_url + "chapter-" + str(index + 1) + "/"
    data = requests.get(chap_link)
    
    if data.status_code != 200:
        failed.append(index)
        pass
    else:
        html_data = BeautifulSoup(data.content, "html.parser")
        chapter = html_data.find('div', class_='reading-content')
        f = open(f"{path}{name}", 'w')
        f.write(str(chapter))
        f.close()
        print(f"{name} done.")
    index += 1

# Finished message
print("\n\nCompleted successfully.")

# print("Creating epub file...")
# folder = usr_folder + "temp/"
# meta_folder = usr_folder + "META-INF/"
# oebps_folder = usr_folder + "OEBPS/"
# fonts_folder = oebps_folder + "Fonts/"
# text_folder = oebps_folder + "Text/"