# -*-encoding:utf-8-*-
import os
import re
import shutil
import time

from wxpy import *

bot = Bot(cache_path=True)


# 说明：可以撤回的有文本文字、语音、视频、图片、位置、名片、分享、附件
# {msg_id:(msg_from,msg_to,msg_time,msg_time_rec,msg_type,msg_content,msg_share_url)}
msg_dict = {}

# 文件存储临时目录
rev_tmp_dir = "/home/wangbin/RevDir/"
if not os.path.exists(rev_tmp_dir): 
    os.mkdir(rev_tmp_dir)

# 表情有一个问题 | 接受信息和接受note的msg_id不一致 巧合解决方案
face_bug = None

# 将接收到的消息存放在字典中，当接收到新消息时对字典中超时的消息进行清理 | 不接受不具有撤回功能的信息
# [TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS, NOTE]
# @itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
@bot.register(msg_types=[TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def handler_receive_msg(msg):

    global face_bug
    # 获取的是本地时间戳并格式化本地时间戳 e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 消息类型
    msg_type = msg.type
    # 消息ID
    msg_id = msg.id
    # 消息时间
    msg_time = msg.create_time
    # 消息发送人昵称 | 这里也可以使用RemarkName备注　但是自己或者没有备注的人为None
    if msg.member != None:
        msg_from = msg.member
    else:
        msg_from = msg.chat

    # 消息内容
    msg_content = None
    # 分享的链接
    msg_share_url = None
    if msg_type == 'Text' \
            or msg_type  == 'Friends':
        msg_content = msg.text
    # elif msg_type == 'Recording' \
    #         or msg_type == 'Attachment' \
    #         or msg_type == 'Video' \
    #         or msg_type == 'Picture':
    #     msg_content = r"" + msg.file_name
    #     # 保存文件
    #     msg['Text'](rev_tmp_dir + msg.['FileName'])
    # elif msg_type == 'Card':
    #     msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    #    elif msg_type == 'Map':
    #        x, y, location = re.search("'OriContent']).group(1, 2, 3)
    #        if location is None:
    #            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
    #        else:
    #            msg_content = r"" + location
    # elif msg_type == 'Sharing':
    #     msg_content = msg['Text']
    #     msg_share_url = msg['Url']
    face_bug = msg_content
    # 更新字典
    print("ID: %d Type: %s Chat: %s Member: %s Content: %s" \
        %(msg_id, msg_type, msg.chat, msg_from, msg_content))

    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg_type,
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )
    # 打印字典内容
    # for key,value in msg_dict.items():
    #     print("DICT: Key %d : Value: %s" %(key, str(value)))

# 收到note通知类消息，判断是不是撤回并进行相应操作
# @itchat.msg_register([NOTE])
@bot.register(msg_types=[NOTE])
def send_msg_helper(msg):
   global face_bug
   msg_content = msg.text
   print("NOTE received: %s" %(msg_content))
   if re.search(r"\<\!\[cdata\[.*撤回了一条消息\]\]\>", msg_content) is not None:
       # 获取消息的id
       old_msg_id = re.search("\(.*?)\<\>", msg_content).group(1)
       old_msg = msg_dict.get(old_msg_id, {})
       if len(old_msg_id) < 11:
           print("!! invalid old_msg_id %d " %(old_msg_id))
           bot.file_helper.send_file(rev_tmp_dir + face_bug)
           os.remove(rev_tmp_dir + face_bug)
       else:
           msg_body = "告诉你一个秘密~" + "\n" \
                      + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                      + old_msg.get('msg_time_rec') + "\n" \
                      + "撤回了什么 ⇣" + "\n" \
                      + r"" + old_msg.get('msg_content')
           # 如果是分享存在链接
           if old_msg['msg_type'] == "Sharing": 
               msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

           # 将撤回消息发送到文件助手
           bot.file_helper.send(msg_body)
           # 有文件的话也要将文件发送回去
           if old_msg["msg_type"] == "Picture" \
                   or old_msg["msg_type"] == "Recording" \
                   or old_msg["msg_type"] == "Video" \
                   or old_msg["msg_type"] == "Attachment":
               file = rev_tmp_dir + old_msg['msg_content']
               bot.file_helper.send_file(file)
               os.remove(rev_tmp_dir + old_msg['msg_content'])
           # 删除字典旧消息
           msg_dict.pop(old_msg_id)


embed()