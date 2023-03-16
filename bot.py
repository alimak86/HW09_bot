import re
import time
import sys

exit_list = ["good bye", "close", "exit", "close"]

CONTACTS = {} ## dictionary of the contacts

## list of commands to use

HELLO_CMD = "hello"
ADD_CMD = "add"
CHANGE_CMD = "change"
PHONE_CMD = "phone"
SHOW_CMD = "show all"
HLP_CMD = "help"

COMMANDS = [HELLO_CMD, ADD_CMD, CHANGE_CMD, PHONE_CMD, SHOW_CMD, HLP_CMD]

def parser(line):
    return re.sub("[^0-9a-zA-Z+()-]"," ",line).split()

GREETING = "How can I help you ? For the commands description please type help"
NOTHING = "There is nothing to execute"
UNDERSTOOD = "Understood"

def wait():
    print(">> Please wait....")
    time.sleep(2)

def check_name(name):
    match = re.fullmatch("[a-zA-Z]+",name)
    while not match:
        print(">> Please input correct name. It should include only letters")
        name = input(">> ").lower()
        match = re.fullmatch("[a-zA-Z]+",name);
    return name

def check_phone(phone):
    match = re.fullmatch(r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-6]{2}",phone)
    while not match:
        print(">> Please input correct phone. Typically it is +1(647)861-9006 or similar")
        phone = input(">> ").lower()
        match = re.fullmatch(r"[+]?[0-9]{1,2}(\([0-9]{3}\)|[0-9]{3})[0-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}",phone)
    return phone

def add_process(words):
    command = words[0]
    if len(words) == 3: ## all required arguments were taken
        name = check_name(words[1]) ## check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2]) ## check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()
    elif len(words) == 2: ## one argument is missing - phone
        name = check_name(words[1]) ## check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1") ## check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()                
    else: ## all arguments were missing only add
        print(">> " + "Found command add in your request. Will need a name and a phone of the contact")
        name = check_name("-1") ## check the name
        print(">> " + "Need phone info for " + name)                
        phone = check_phone("-1") ## check the phone
    return command + " " + name + " " + phone

def change_process(words):
    command = words[0]
    if len(words) == 3: ## all required arguments were taken
        name = check_name(words[1]) ## check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2]) ## check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()
    elif len(words) == 2: ## one argument is missing - phone
        name = check_name(words[1]) ## check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1") ## check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()                
    else: ## all arguments were missing only add
        print(">> " + "Found command change in your request. Will need name and phone of the contact")
        name = check_name("-1") ## check the name
        print(">> " + "Need phone info for " + name)                
        phone = check_phone("-1") ## check the phone
    return command + " " + name + " " + phone

def phone_process(words):
    command = words[0]
    if len(words) == 2: ## all required arguments were taken
        name = check_name(words[1]) ## check the name
        print(">> " + "It is all right. Will chase for the phone of " + name)
        wait()
    else: ## all arguments were missing only add
        print(">> " + "Found command phone in your request. Will need name of the contact")
        name = check_name("-1") ## check the name
    return command + " " + name

PROCESS = { ADD_CMD: add_process,\
            CHANGE_CMD: change_process,\
            PHONE_CMD: phone_process
           }

def input_error(command_func):
    def inner(list):
        corrected_list = []
        for record in list: ## list of commands extracted from the user input
            #######################################################print(record)
            words = record.split() ## split the possible action
            command = words[0] ## it is always command
            corrected_list.append(PROCESS[command](words))
            ####################################################33 print(corrected_list)
        return command_func(corrected_list)
    return inner

def nothing():
    return NOTHING 

def greet(list = []):
    return GREETING

@input_error
def add_contact(list): ## list contains lists of possible actions to add
    ##############################print(list)
    output = ""
    for record in list:
        words = record.split()
        #############################print(words)
        name = words[1]
        phone = words[2]
        CONTACTS[name] = phone
        output+=name + " "
    return "Added " + output + "into the contacts"

@input_error
def change(list): ## list contains lists of possible actions to add
    ################################print(list)
    output = ""
    for record in list:
        words = record.split()
        name = words[1]
        found = CONTACTS.get(name,0)
        ##############################print(found)
        if found:
            phone = words[2]
            CONTACTS[name] = phone
            output+=name + " "
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped" )
    return "Phones were modified for: " + output 

@input_error
def phone(list): ## list contains lists of possible actions to add
    ################################print(list)
    print("-" * 36)
    print("{:^36}|".format("Current list of the contacts"))
    print("-" * 36)
    for record in list:
        words = record.split()
        name = words[1]
        found = CONTACTS.get(name,0)
        ##############################print(found)
        if found:
            print("{:^16} | {:^16} |".format(name,CONTACTS[name]))
            print("-" * 36)
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped" )        
    return "Done"


def show(list = []):
    print("-" * 36)
    print("{:^36}|".format("Current list of the contacts"))
    print("-" * 36)
    for contact in CONTACTS:
        print("{:^16} | {:^16} |".format(contact,CONTACTS[contact]))
        print("-" * 36)
    return "Done"

def help(list = []):
    return """\n* add - add a contact and a phone\n  
* change - change a contact phone \n
* phone - list a phone of the contact \n
* show all - list all the contacts \n
* help - list menu of the commands \n"""

def command_parser(line):
    return re.findall("add[ ]+[a-zA-Z]+[ ]+[+][1-9][(][0-9]{3}[)][0-9]{3}-[0-9]{4}",line)

PARSER = {
          HELLO_CMD: lambda x: re.findall(HELLO_CMD,x),\
          ADD_CMD: lambda x: re.findall(ADD_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*",x),\
          CHANGE_CMD: lambda x: re.findall(CHANGE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*",x),\
          PHONE_CMD: lambda x: re.findall(PHONE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*",x),\
          SHOW_CMD: lambda x: re.findall(SHOW_CMD + "[ ]*[a-zA-Z0-9\+\-()]*",x),\
          HLP_CMD: lambda x: re.findall(HLP_CMD,x)
         }

RESPONSE = {
              HELLO_CMD: greet, \
              ADD_CMD: add_contact, \
              CHANGE_CMD: change,\
              PHONE_CMD: phone,\
              SHOW_CMD: show,\
              HLP_CMD: help
             }

def main():
    while True:
        line = input(">> ").lower()
        if line in exit_list:
            print(">> Good bye!")
            break
        else:
            for word in COMMANDS:
                command_list = PARSER[word](line)
                if len(command_list):
                    handler = RESPONSE[word]
                    print(">> " + str(handler(command_list)))

#####print(check_phone("+386478617006"))
######print(check_name("+1(647)861 wrwf"))
###line = "add Alisa +16478617006 show all"
##command_line = PARSER["add"](line)
##handler = RESPONSE["add"]
##print(handler(command_line))
##3command_line = PARSER["show"](line)
###handler = RESPONSE["show"]
################print(handler(command_line))
###wait()
if __name__ == "__main__":
    main()


