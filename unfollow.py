#!/usr/bin/env python

#This program unfollow the followed profile from the webstagram program
import mechanize
import re
import threading
#import optparse #will add this latter for command line parsing

#may use configs directly from the other programs in the future
#config_file   = re.findall( "config_file   = \""  , open( "webstagramliker_wissam_otaku_chan.py" ).read() )
config_file   = ".config.txt"
usersID_file  = "users.txt"


class unfollow(threading.Thread):
    ##self variables
    def __init__(self,user,passwd,all_usersID):
        self.user        =   user
        self.passwd      =   passwd
        self.br          =   self.browser()
        self.all_usersID =   all_usersID
        threading.Thread.__init__(self)

    #handle the creation of a browser
    def browser(self):
        br = mechanize.Browser()
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_robots(False)
        br.addheaders = [("user-agent","Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-US) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")]
        return br

    #handle the login
    def loginin(self):
        self.br.open("https://instagram.com/accounts/login/")
        self.br.select_form(nr=0)
        self.br.form['username']  =   self.user   #klinker_meister
        self.br.form['password']  =   self.passwd
        self.br.submit()
        self.br.open("http://web.stagram.com/")
        myurl = ""
        for a in self.br.links():
            if "LOGIN" in a.text :
                print a.url
                myurl = a.url
                break
        print myurl
        self.br.open(myurl.replace(" ",""))

    #handle the follow
    def un_follow(self, userID):
        self.br.open( "http://web.stagram.com/do_unfollow/", "&pk=" + str(userID) )
        # here after appending the userID we should not forget to save it to the file
        self.all_usersID.remove( userID )
        print "Unfollowed " + str( userID )
        open( usersID_file, 'w' )
        for user in self.all_usersID:
            open( usersID_file, 'a' ).write( user + "\n" )


    #main function of the class
    def run(self):
        try:
            self.loginin()
        except Exception,e:
            print e

        #will unfollow for the sirs
        for userID in self.all_usersID:
            try:
                self.un_follow(userID)
            except:
                pass

#if __name__ == '__main__':
    #p = optparse.OptionParser(description='Unfollow instagram users that has been followd with the program webstagram.py',
    #                       prog='unfollower',
    #                       version='unfollow.py 0.2',
    #                       usage='%prog config_file usersID_file')
##Initialise every variables
user,passwd, usersIDs = open(config_file,'r').read().split(":")[1],  open(config_file,'r').read().split(":")[2].replace("\n","").replace(" ",""),  open(usersID_file, 'r').readlines()
all_usersID  = []
for usersID in usersIDs:
    all_usersID.append( usersID.replace("\n","") )

##Starts the thread
Mythread = unfollow(user,passwd,all_usersID)
Mythread.start()
