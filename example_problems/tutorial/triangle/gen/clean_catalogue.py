#!/usr/bin/env python3
import os

def clean_catalogue():
    files_to_delete = []
    main_directory = "../instances_catalogue"
    for foldername in os.listdir(main_directory): 
        if foldername[-6:] == "single":
            for file in os.listdir("../instances_catalogue/"+foldername):
                if "double" in file:
                    files_to_delete.append("../instances_catalogue/"+foldername+"/"+file)
                    files_to_delete.append("../instances_catalogue/all_instances/"+file)
        elif foldername[-6:] == "double":
            for file in os.listdir("../instances_catalogue/"+foldername):
                if "single" in file:
                    files_to_delete.append("../instances_catalogue/"+foldername+"/"+file)
                    files_to_delete.append("../instances_catalogue/all_instances/"+file)
    return files_to_delete

files = clean_catalogue()
for file in files:
    os.remove(file)
    
exit(0)


