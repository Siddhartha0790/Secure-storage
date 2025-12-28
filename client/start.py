


from working.test import getfile,postfile

username = "SID"
password = "SID"
with open("file.txt", "rb") as f:
    file_bytes = f.read()


getfile(username,password,16)



