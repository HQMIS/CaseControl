#-*-coding:utf-8-*-

# script: CaseControl.py
# author: huangqimin@baidu.com

# note: 
# 1、In Command ls, File's name output question：
#    “.” and "2", length is not the same

from cmd import Cmd
import os
import sys
import getopt   ### Python 参数处理模块
import time
import shutil

class Pash(Cmd):

    def __init__(self, user_name, completekey='tab'):
        Cmd.__init__(self)
        self.app_path = os.getcwd()
        self.cwd = "/".join(sys.argv[0].split("\\")[:-1])
        self.server_path = "//xxx.xx.xxx.xxx/share/CaseControl/PIS/"
        self.intro = 'UbcToolKit 3.1.1 (default, Dec 24 2012, 00:00:00) \n[MSC v.1500 32 bit (Intel)] on win32\nType "copyright", "history" or "feedback" for more information.\n\n' + "Now Time is: " + time.strftime("%Y-%m-%d %X", time.localtime(time.time())) + "\nDarling " + user_name + ": Welcome to UbcToolKit" + os.linesep
        
        self.output = {"type":"", "value":[], "redirect":""}
        self.changeUser(user_name)

    ### 路径改变后，需要更新提示符
    def updatePrompt(self):
        self.current_path = os.getcwd()
        self.current_path = self.current_path.replace("C:\\", "/")
        self.current_path = self.current_path.replace("\\", "/")
        self.prompt = "%s@baidu.com %s $ " % (self.user_name, self.current_path)

    def changeUser(self, name):
        self.user_name = name
        self.do_cd(self.cwd)

    ### 如果输入的命令为空，则神马都不做
    def emptyline(self):
        pass

    ### 如果是未定义的命令, 提示之
    def default(self, line):
        print "Unknown Command: ", line, len(line)

    ### 命令补全，供所有命令的complete_xxx
    ### 一开始，所有的命令都需写下面一段
    ### 现在只需调用该函数即可
    def _complete_(self, text, line, begidx, endidx):
        text = line.rsplit()[-1]
        text = text if "/" in text else "./" + text
        path, prefix = text.rsplit("/", 1)
        return [name for name in os.listdir(path+"/") 
            if name.startswith(prefix)]

    def _help_(self, command, cmd, intro):
        print 
        print "Help on Command " + command + ":" + os.linesep
    
        print "NAME"
        print "    " + command + os.linesep
    
        print "PARAMENTER"
        print "    |------------------------------------------------------------------------"
        for index, item in enumerate(cmd):
            print "    | " + item
            print "    |     " + intro[index]
            print "    |------------------------------------------------------------------------"
        print 
 
    ### 系统命令--ls
    ### 显示文件(夹)列表
    ### 
    def do_ls(self, opt):
        if opt =="":
            opt = os.getcwd()
        elif opt[0] == "/":
            opt = "C:"+opt
        else:
            pass
        isfile = os.path.exists(opt)    # check opt is exist&file or not
        if isfile:
            lsValue = []
            for filename in os.listdir(opt or "."):
                if os.path.isdir(opt+"/"+filename):
                    lsValue.append("Y"+filename)
                else:
                    lsValue.append("N"+filename)
            self.output.update({
                "type": "ls",
                "value": lsValue
            })
        else:
            if opt[:3] == "-l " or opt[:2] == "-l":    # ls -l path    # 一开始写成了 opt[:3] == "-l "
                opt = opt[3:]
                if opt == "":
                    opt = os.getcwd()
                elif opt[1] == "/":
                    opt = "C:"+opt
                else:
                    pass
                isfile = os.path.exists(opt)
                if isfile:
                    llValue = []
                    llValue.append("NName".ljust(18)+"Size(KB)".ljust(18)+"Last modified".ljust(18)+"Type".ljust(18))
                    for file in os.listdir((opt or ".")):
                        path = opt + "/" + file    # path of files
                        if os.path.isdir(path):
                            llValue.append("Y"+file.ljust(18)+str(os.stat(path).st_size).ljust(18)+(str(time.localtime(os.stat(path).st_ctime).tm_year)+"/"+str(time.localtime(os.stat(path).st_ctime).tm_mon)+"/"+str(time.localtime(os.stat(path).st_ctime).tm_mday)).ljust(18)+("<DIR>".ljust(18) if os.path.isdir(file) else " "*18))
                        else:
                            llValue.append("N"+file.ljust(18)+str(os.stat(path).st_size).ljust(18)+(str(time.localtime(os.stat(path).st_ctime).tm_year)+"/"+str(time.localtime(os.stat(path).st_ctime).tm_mon)+"/"+str(time.localtime(os.stat(path).st_ctime).tm_mday)).ljust(18)+("<DIR>".ljust(18) if os.path.isdir(file) else " "*18))
                    self.output.update({
                        "type": "ls -l",
                        "value": llValue,
                    })
                else:
                    print "The path input isn't exist!!!"
            else:
                print "The path input isn't exist!!!"

    def help_ls(self):
        cmd = ["ls", "ls -l"]
        intro = ["Show File List, Four in each line", "Show Detail Infomation of File"]
        self._help_("ls", cmd, intro)
        
    def complete_ls(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ### 系统命令--cd
    ### 切换目录
    ###
    def do_cd(self, opt):
        opt = opt or "/"
        try:
            os.chdir(opt)
        except OSError as inst: 
            print inst[1], ": ", opt
        self.updatePrompt()

    def help_cd(self):
        cmd = ["cd C: || cd D: || cd E", "cd .."]
        intro = ["Change Current Path to C:// || D:// || E://", "Change Current Path to Upper Level Directory"]
        self._help_("cd", cmd, intro)

    def complete_cd(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### clone/pull
    # clone/pull case to local
    ###
    
    def do_clone(self, opt):
        if "" == opt:
            self.help_clone()
        else:
            if os.path.isdir(self.cwd+"/Case"):
                pass
            else:
                os.mkdir(self.cwd+"/Case")             
            paraList = opt.split(" ")
            for para in paraList:
                try:
                    shutil.rmtree(self.cwd+"/Case/"+para)
                except:
                    pass
                try:
                    shutil.copytree(self.server_path+para, self.cwd+"/Case/"+para)
                except:
                    print "网络连接异常".decode("utf8").encode("gb2312")
        
    def do_pull(self, opt):
        if "" == opt:
            self.help_pull()
        else:
            if os.path.isdir(self.cwd+"/Case"):
                pass
            else:
                os.mkdir(self.cwd+"/Case")             
            paraList = opt.split(" ")
            for para in paraList:
                try:
                    shutil.rmtree(self.cwd+"/Case/"+para)
                except:
                    pass
                try:
                    shutil.copytree(self.server_path+para, self.cwd+"/Case/"+para)
                except:
                    print "网络连接异常".decode("utf8").encode("gb2312")
             
    def help_clone(self): 
        cmd = ["clone", ]
        intro = ["Enter Help Info of Clone", ]
        try:
            for file in os.listdir(self.server_path):
                cmd.append(file)
                intro.append("Clone Case of "+file+" to Local from Server")
        except:
            pass
        self._help_("clone", cmd, intro)
              
    def help_pull(self):
        cmd = ["pull", ]
        intro = ["Enter Help Info of Pull", ]
        try:
            for file in os.listdir(self.server_path):
                cmd.append(file)
                intro.append("Pull Case of "+file+" to Local from Server")
        except:
            pass
        self._help_("clone", cmd, intro)
    
    def complete_clone(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    def complete_pull(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### push
    # push case to server
    ###
    
    def do_push(self, opt):
        if "" == opt:
            self.help_push()
        else:
            if os.path.isdir(self.cwd+"/Case"):
                pass
            else:
                os.mkdir(self.cwd+"/Case")             
            paraList = opt.split(" ")
            for para in paraList:
                try:
                    shutil.rmtree(self.server_path+para)
                except:
                    #print "Failed to remove"
                    pass
                try:
                    shutil.copytree(self.cwd+"/Case/"+para, self.server_path+para)
                except:
                    print "网络连接异常".decode("utf8").encode("gb2312")
                    
    def help_push(self):
        cmd = ["push", ]
        intro = ["Enter Help Info of Push", ]
        try:
            for file in os.listdir(self.cwd+"/Case/"):
                cmd.append(file)
                intro.append("Push Case of "+file+" to Server from Local")
        except:
            pass
        self._help_("clone", cmd, intro)

    def complete_pull(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### detail
    # show the detail of case
    ###
    
    def listdir(self, leval, path):
        for i in os.listdir(path):
            if "log" == i:
                pass
            else:
                if os.path.isdir(path+i):
                    print('|  '*(leval + 1) + "+" + i)
                    self.listdir(leval+1, path+i+"/")
                else:
                    print('|  '*(leval + 1) + i)
                
    def do_detail(self, opt):
        if "" == opt:
            self.help_detail()
        else:         
            paraList = opt.split(" ")
            for para in paraList:
                try:
                    print 
                    self.listdir(0, self.cwd+"/Case/"+para+"/")
                    print
                except:
                    pass
                
    def help_detail(self):
        cmd = ["detail", ]
        intro = ["Enter Help Info of Detail", ]
        try:
            for file in os.listdir(self.cwd+"/Case/"):
                cmd.append(file)
                intro.append("Show Case's Detail Info "+file)
        except:
            pass
        self._help_("detail", cmd, intro)

    def complete_detail(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### submit
    # submit
    ###
    
    def do_submit(self, opt):
        if "" == opt:
            self.help_submit()
        else:           
            paraList = opt.split(" ")
            if 1 == len(paraList):
                print "Error, Please Input Submit Reason"
            else:
                reason = " ".join(paraList[1:])
                rowList = []
                try:
                    f = open(self.cwd+"/Case/"+paraList[0]+"/log", "r")
                    rowList = f.readlines()
                    f.close()
                except:
                    pass

                rowList.reverse()
                rowList.append(""+os.linesep)
                rowList.append(""+os.linesep)
                rowList.append("    "+reason+os.linesep)
                rowList.append(""+os.linesep)
                rowList.append("Date: " + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+os.linesep)
                rowList.append("Author: " + self.user_name+os.linesep)
                rowList.reverse()
                
                f = open(self.cwd+"/Case/"+paraList[0]+"/log", "w")  
                f.writelines(rowList)
                f.close()
                    
    def help_submit(self):
        cmd = ["submit", ]
        intro = ["Enter Help Info of submit", ]
        try:
            for file in os.listdir(self.cwd+"/Case/"):
                cmd.append(file)
                intro.append("Submit "+file)
        except:
            pass
        self._help_("submit", cmd, intro)

    def complete_submit(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### log
    # Show the Log, Show the History
    ###
    
    def do_log(self, opt):
        if "" == opt:
            self.help_log()
        else:           
            paraList = opt.split(" ")
            for para in paraList:
                try:
                    f = open(self.cwd+"/Case/"+para+"/log", "r")
                    print
                    for row in f:
                        print row,
                    f.close()
                except:
                    pass
                    
    def help_log(self):
        cmd = ["log", ]
        intro = ["Enter Help Info of Log", ]
        try:
            for file in os.listdir(self.cwd+"/Case/"):
                cmd.append(file)
                intro.append("History of "+file)
        except:
            pass
        self._help_("log", cmd, intro)

    def complete_submit(self, text, line, begidx, endidx):
        return self._complete_(text, line, begidx, endidx)

    ################################################################################################################

    ### Type "copyright", "history" or "feedback"
    
    def do_copyright(self, opt):
        print os.linesep+"Copyright (c) 2013 Baidu CloudsOS YiQA PIS.\nAll Rights Reserved."+os.linesep
      
    def do_history(self, opt):
         print os.linesep+"1st Edition: 1.1.1\n    Demo Version of CaseControl" + os.linesep

    def do_feedback(self, opt):
        print os.linesep+"Author:huangqimin\nHI: HQMIS\nEmailto: huangqimin@baidu.com"+os.linesep

    ################################################################################################################


    ### 连续命令
    def do_multi(self, cmds):
        for cmd in cmds:
            self.onecmd(cmd)

    ### 退出程序, 关闭数据库连接
    def do_exit(self, opt):
        bye = self.user_name+", Bye Bye"
        print os.linesep+os.linesep+bye.center(80)
        time.sleep(3)
        sys.exit()

    def do_EOF(self, opt):
        print 
        self.do_exit(opt)

    def postcmd(self, stop, line):
        type = self.output.get("type", "")
        value = self.output.get("value", [])
        rf = self.output.get("redirect", "")
        self.output = {"type":"", "value":[], "redirect":""} 
 
        fp = open(rf, "w") if rf else sys.stdout

        if type == "ls":
            if rf:
                #value = [valueList[1:] for valueList in value]
                for i, filename in enumerate(value):
                    fp.write(filename[1:]+"\n")
            else:
                fileList = value
                if fileList == []:
                    pass
                else:
                    for i in range(len(fileList)):
                        if fileList[i][0] == "Y":
                            #print fileList[i][1:].ljust(25),
                            print fileList[i][1:]+"_"*(18-len(fileList[i][1:])),
                        else:
                            #print fileList[i][1:].ljust(25),
                            print fileList[i][1:]+"_"*(18-len(fileList[i][1:])),
                        if (i+1)%4 == 0:    # each line shows 4 files' name
                            print
                    if (i+1)%4:    #如果不是正好4的倍数个，则，输出一个换行符
                        print
        elif type == "ls -l":
            if rf:
                #value = [valueList[1:] for valueList in value]
                for i in range(len(value)):
                     value[i] = value[i][1:]
                fp.write("\n".join(value))
            else:
                for fileInfo in value:
                    if fileInfo[0] == "Y":
                        print fileInfo[1:],
                    else:
                        print fileInfo[1:],
                    print

if __name__ == "__main__":
    UserNameFilePath = "/".join(sys.argv[0].split("\\")[:-1]) + "/UserName"
    if os.path.exists(UserNameFilePath):
        f = open(UserNameFilePath, "r")
        uname = f.readline()
        f.close()
    else:
        print "It's the First Time for You Using UbcToolKit\nPlease Input Your Name(Like huangqimin)"
        uname = raw_input("UserName: ")
        f = open(UserNameFilePath, "w")
        f.write(uname)
        f.close()
    pash = Pash(uname)
    pash.cmdloop()
