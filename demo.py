# -*- coding: utf-8 -*-

from wxpy import *

bot = Bot(cache_path=True)

num_msg = 0

# @bot.register()
# def recv_send_msg(recv_msg):
    
#     global num_msg 
#     num_msg = num_msg + 1
#     print("Recevied Message: %d type %s" %(num_msg, recv_msg.type))  
#     recv_msg.forward(bot.file_helper, prefix='转发消息: ')
#     return '' 

####### 监控星羽联盟群中的周日报名信息，周四报名时抢报
# 定位星羽联盟群
badminton_group = ensure_one(bot.groups().search('星羽联盟'))

# 定位报名机器人
group_robot = ensure_one(badminton_group.search('运动去'))

# 将群机器人的消息转发到文件传输助手
# @bot.register(badminton_group, TEXT)
@bot.register(badminton_group, TEXT)
def forward_robot_message(recv_msg):

    global num_msg 
    num_msg = num_msg + 1
    print("Received Message: %d type: %s group: %s" %(num_msg, recv_msg.type, recv_msg.chat))

    str_reply = "ignore..."

    if recv_msg.member == group_robot :

        print("Message Content: %s" %(recv_msg.text))

        index_sunday = recv_msg.text.find("周二")
        index_shenggu = recv_msg.text.find("在胜古体育馆打羽毛球")
        index_in = recv_msg.text.find("已报人员名单：")
        index_waiting = recv_msg.text.find("替补人员名单：")
        index_me = recv_msg.text.find("王斌")

        print("sunday %d shenggu %d in %d waiting %d wangbin %d " \
                %(index_sunday, index_shenggu, index_in, index_waiting, index_me))

        if index_sunday >= 0 and index_shenggu > index_sunday and index_in > index_shenggu :
            if index_me == -1:
                if index_waiting == -1:
                    # 发送报名
                    str_reply = "报名周日"
                else:
                    str_reply = "替补周日"
                    # 发送替补

        recv_msg.forward(bot.file_helper, prefix='报名机器人信息： ')

    str_tmp = "我的回复： " + str_reply
    bot.file_helper.send(str_tmp)

    return ""

embed()
