import mechanize
import re, random
import threading, time

config_file   = ".config.txt"
pages_file    = "pages.txt"
comments_file = "comments.txt"


liker = 0
class webstagram(threading.Thread):
    def __init__(self,pages,user,passwd,all_comments):
        self.pages    =   pages
        self.user     =   user
        self.passwd   =   passwd
        self.br       =   self.browser()
        self.comments = all_comments
        threading.Thread.__init__(self)


    def browser(self):
        br = mechanize.Browser()
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_robots(False)
        br.addheaders = [("user-agent","Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-US) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")]
        return br

    def loginin(self):
        self.br.open("https://instagram.com/accounts/login/")
        self.br.select_form(nr=0)
        self.br.form['username']  =   self.user #klinker_meister
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

    def commenter(self, photoID):
        my_comment = random.choice(self.comments)
        self.br.open("http://web.stagram.com/post_comment/", "message="+my_comment+"&messageid="+photoID)

    def pertag(self, theme):
        try:
            global liker
            self.br.open("http://web.stagram.com/tag/"+theme+"/")
            if not "No photo tagged with #" in self.br.response().read():
                linkza = []
                number = 0

                for a in self.br.links():
                    if a.url.startswith("/p/") :
                        mybadlinks = a.url
                        mybadlinks = mybadlinks.split("/p/")[1].replace("/","")
                        print     mybadlinks
                        if mybadlinks not in linkza:
                            linkza.append(mybadlinks)


                time.sleep(2)
                for linkzb in linkza:
                    print linkzb
                    self.br.open("http://web.stagram.com/do_like/","&pk="+linkzb+"&t=")
                    self.commenter(linkzb)
                    liker+=1
                    print "NUMBER OF LIKES: "+ str(liker)
                    if liker==254:
                        print "254 likes done now will wait 1 hour"
                        time.sleep(3660)
                        liker=0
            else:
                pass
        except Exception,e:
            print e
            time.sleep(2)
            self.pertag(theme)


    def perkeyword(self,theme):
        try:
            global liker
            self.br.open("http://web.stagram.com/keyword/"+theme+"/")
            linkza = []
            number=0
            print theme
            while theme+"?page" in self.br.response().read() and number<20:
                for a in self.br.links():
                    if a.url.startswith("/n/") :
                        mybadlinks = a.url
                        mybadlinks = mybadlinks.split("/n/")[1].replace("/","")
                        print "USER"
                        print     mybadlinks
                        if mybadlinks not in linkza and mybadlinks!=self.user:
                            linkza.append(mybadlinks)
                number+=1
                self.br.open("http://web.stagram.com/keyword/"+theme+"?page="+str(number))
                time.sleep(2)
            for linkzb in linkza:
                print linkzb
                self.br.open("http://web.stagram.com/n/"+linkzb)
                linkzc = []
                time.sleep(2)
                for b in self.br.links():
                    if b.url.startswith("/p/") :
                        mybadlinks2 = b.url
                        mybadlinks2 = mybadlinks2.split("/p/")[1].replace("/","")
                        print     mybadlinks2
                        if mybadlinks2 not in linkzc:
                            linkzc.append(mybadlinks2)
                time.sleep(2)
                for linkzd in linkzc:
                    print linkzd
                    self.br.open("http://web.stagram.com/do_like/","&pk="+linkzd+"&t=")
                    self.commenter(linkzd)
                    liker+=1
                    print "NUMBER OF LIKES: "+ str(liker)
                    if liker==254:
                        print "254 likes done now will wait 1 hour"
                        time.sleep(3660)
                        liker=0
        except Exception,e:
            print e
            time.sleep(2)
            self.perkeyword(theme)

    def run(self):
        global liker
        try:
            self.loginin()
        except Exception,e:
            print e
        #some tag or page
        for theme in self.pages:
            print theme
            theme = theme.replace(" ","").replace("\n","")
            try:
                print "PER TAG"
                self.pertag(theme)
            except Exception,e:
                print e
                time.sleep(1)
                self.pertag(theme)
            try:
                print "PER KEYWORD:"
                self.perkeyword(theme)
            except Exception,e:
                print e
                time.sleep(1)
                self.perkeyword(theme)

user,passwd = open(config_file,'r').read().split(":")[1],open(".config.txt",'r').read().split(":")[2].replace("\n","").replace(" ","")
pages = open(pages_file,'r').readlines()
comments = open(comments_file,'r').readlines()
all_comments = []
for comment in comments:
    all_comments.append( comment.replace("\n","") )

Mythread = webstagram(pages,user,passwd,all_comments)
Mythread.start()

