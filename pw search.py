import time
with open("rockyou.txt", "r", encoding="latin-1") as f:
        x = f.readlines()
def searcher():
    index = 0
    usr_input = input("What do you look for? ")
    indextolookfor = list()
    for shit in x:
        shit = shit.strip().lower()
        index = index + 1
        if usr_input in shit:
            indextolookfor.append(index)
    print("I have found", len(indextolookfor),"passwords.")
    input("Press enter to proceed.")
    index = 0
    for i in indextolookfor:
        index = index + 1
        print(str(index) + ".","[" + str(i) + "]", x[i-1])
    print("This shit is quick now, pal!")
    input()
print("Welcome to my searcher")
searcher()


