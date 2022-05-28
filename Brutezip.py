import random
import multiprocessing
import os
import sys
import time
import pyzipper
import platform

"""
Hello and welcome to my program designed to brute force password secured zips.
To make it work you will have to do 3 things.
- Change the file name at extract function;
- Switch between key_list or num_list at generator function.
- Define the passwords lengths you want to iterate through in the __main__ by modifying variable "x".
The software will automatically generate multiprocesses depending on the core count
and the password lengths you want to process through. The software always get into consideration the worst case
scenario if you try to input more "lengths" than the core count by cutting off the lower password length to iterate
through. 
- You might need to use "pip install pyzipper" - libary.


"""
#Take password from generator and try it on the zip.
def extract(password):
    try:
        with pyzipper.AESZipFile('dada.zip', 'r', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as extracted_zip:
            extracted_zip.extractall(pwd=str.encode(password))
            #Let know if password has been found and save it in a file.
            print("The pasword that worked", output, time.process_time())
        with open("pw_crack_output.txt","a") as f:
            x = str("The pasword that worked " + output + "\n")
            f.write(x)
    #Wrong password? Skip the traceback and try again.
    except:
        pass
# Randomly generate the password based on keylist or num/list and the password length.
def generator(num_length):
    n = 10000
    i = 0
    while True:
        global output
        output = ""
        x = random.choices(key_list, k=int(num_length))
        output = "".join(x)
        #Send the password to extract function
        extract(output)
        #Count the amount of iterations and print them out.
        i += 1
        if i == n:
            print(str(n / 1000) + "k", "Key length:", num_length)
            n *= 2
            continue
#List of chars you want to iterate through.
key_list = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!',
            '"', '#', '$', '%', '&', '"', '"', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?',
            '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~')
num_list = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

if __name__ == "__main__":
    print("Welcome to zip brute force™")
    #CPU info.
    print("CPU:",platform.processor()+"    CORE COUNT", os.cpu_count())
    #Ask for the amount of threads to use.
    try:
        cpu = int(input("Input the amount of cores/threads you want to use: "))
    #Empty or wrong input? Use all cores.
    except:
        cpu = os.cpu_count()
    # What is the password length you want to brute force?
    # You can try to break multiple lengths at the same time, by appending them to the list x.
    x = [6]
    #search num is an adjusted list for the sake of multi processing.
    search_num = []
    #Generating search_num - The optimized multiprocess password length list.
    if len(x) < cpu:
        while len(search_num) < cpu and cpu % len(x) == 0:
            for element in x:
                search_num.extend([element, element])
                if len(search_num) == cpu:
                    break
        while len(search_num) < cpu and cpu % len(x) != 0:
            for element in x:
                search_num.append(element)
                if len(search_num) == cpu:
                    break
        search_num.sort()
        print("Iterating through passwords lengths:", x, "Number of processes:", len(search_num), "|USING:", str(cpu),
              "cores out of", os.cpu_count())
        print("iterating through", key_list)
    elif len(x) > cpu:
        print("Warning! The quantity of processes:", len(x), "is greater than cpu count:", cpu)
        print("The password lengths you want to process: ", x)
        print("iterating through", key_list)
        while len(search_num) < cpu:
            for element in x:
                search_num.append(element)
                if len(search_num) == cpu:
                    break
            print("-----------------------------------------------------------------------")
            print("Automatically adjusted password length:", search_num)
            print("Iterating through passwords lengths:", x, "Number of processes:", len(search_num), "|USING:", str(cpu),
              "cores out of", os.cpu_count())
            print("iterating through", key_list)
    else:
        search_num = x
        print("Iterating through passwords lengths:", x, "Number of processes:", len(search_num), "|USING:", str(cpu),
              "cores out of", os.cpu_count())
        print("iterating through", key_list)
        #Create multiprocesses based on the search_num list.
    with multiprocessing.Pool(cpu) as pool:
        result = pool.map(generator, search_num)
