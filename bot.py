import re
while True:
    line = input(">> ").lower()  # everything down
    if line == "done":
        break
    else:
        print(">> " + line)
