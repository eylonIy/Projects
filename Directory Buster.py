import os
def Connection(url):
    result = os.popen(f"ping {url}")
    if "Lost = 0" in result.read():
        return True
    else:
        return False
import urllib3
def DirB():
    session=urllib3.PoolManager()
    while True:
        try:
            file=input("Enter a wordlist")
            Dirs = open(f"{file}","r")
            break
        except:
            print("Not a valid file")
        flag = True
        req=session.request("GET",r"https://hack-yourself-first.com")
        while flag:
            if not Connection():
                break
            else:
                for x in Dirs:
                    if session.request("GET",f"https://hack-yourself-first.com/{Dirs}").status() == 200:
                        print("Success")
                        print(f"https://hack-yourself-first.com/{Dirs}")
                    elif session.request("GET",f"https://hack-yourself-first.com/{Dirs}").status() == 404:
                        print("No such directory")
                        print(f"https://hack-yourself-first.com/{Dirs}")
DirB()