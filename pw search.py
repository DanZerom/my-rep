"""
Welcome to my pw finder. Edit rockyou.txt placeholder with a txt file that has a password list (such password list can be found in the internet).

"""
import time
#Open File
with open("rockyou.txt", "r", encoding="latin-1") as f:
        x = f.readlines()
def searcher():
    index = 0
    usr_input = input("What do you look for? ")
    indextolookfor = list()
#Iterate through the list, count the lines.
    for shit in x:
        shit = shit.strip().lower()
        index = index + 1
#append indextolookfor list with "counted" line.
        if usr_input in shit:
            indextolookfor.append(index)
#Print indexes in indextolookfor.
    print("I have found", len(indextolookfor),"passwords.")
    input("Press enter to proceed.")
#Reiterate through indextolookfor and then print the lines.
        index = 0
    for i in indextolookfor:
        index = index + 1
        print(str(index) + ".","[" + str(i) + "]", x[i-1])
    print("This shit is quick now, pal!")
    input()
print("Welcome to my searcher")
searcher()


