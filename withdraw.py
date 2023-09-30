import re
import os
import time
import itchat
import platform
from itchat.content import *
  
# AUTHOR : Jihuai
# time： 30/09/2023
# pip3 install itchat-uos==1.5.0.dev0
## pip3 install itchat
msg_info = {}
face_package = None

#handle the accepted message
@itchat.msg_register([TEXT,PICTURE,FRIENDS,CARD,MAP,SHARING,RECORDING,ATTACHMENT,VIDEO],isFriendChat=True, isMpChat= True)
def handle_rsg(msg):
    global face_package
    #message accept time
    msg_time_receive = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    try:
        msg_from = itchat.search_friends(userName = msg["FromUserName"])["Nickname"]
    except:
        msg_from = 'Wechat official Accounts'
    #message sending time 
    msg_time_send = msg['CreateTime']
    #message ID
    msg_id = msg['MsgId']
    msg_content = None
    msg_link = None
    
    #text or friend suggestion
    if msg['Type'] == 'Text' or msg['Type'] =='Friends':
        msg_content = msg['Text']
        print('[Text/Friends]: %s' %msg_content)
    elif msg['Type'] == 'Attachment' or msg['Type'] == "Video" or msg['Type'] == 'Picture' or msg['Type'] == 'Recording':
        msg_content = msg['FileName']
        msg['Text'](str(msg_content))
    msg_info.update({
        msg_id:{
            "msg_from":msg_from,
            "msg_time_send":msg_time_send,
            "msg_time_receive":msg_time_receive,
            "msg_Type":msg["Type"],
            "msg_content":msg_content,
            "msg_link" :msg_link
        }
    })
    face_package = msg_content
    
@itchat.msg_register(NOTE, isFriendChat= True, isGroupChat=True, isMpChat= True)
def monitor(msg):
    if '撤回了一条消息' in msg['Content']:
        recall_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>",msg['Content']).group(1)
        recall_msg = msg_info.get(recall_msg_id)
        print('[Recall]: %s'%recall_msg)
        
        if len(recall_msg_id)<11:
            itchat.send_file(face_package,toUserName = 'filehelper')
        else:
            msg_prime = '---' + recall_msg.get('msg_from')+recall_msg.get('msg_content')
            if recall_msg['msg_Type'] == 'Attachment' or recall_msg['msg_Type'] =='Picture':
                
                file = '@fil@%s' %(recall_msg['msg_content'])
                
                #发给文件传输助手
                itchat.send(msg=file , toUserName='filehelper')
                os.remove(recall_msg['msg_content'])
            msg_info.pop(recall_msg_id)
            
if __name__ == '__main__':
    if platform.platform()[:7] == 'Windows':
        itchat.auto_login(enableCmdQR= False,hotReload= True)
    else:
         itchat.auto_login(enableCmdQR= True,hotReload= True)
    itchat.run()
