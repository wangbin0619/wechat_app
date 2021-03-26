# -*- coding: utf-8 -*-

from wxpy import *

bot = Bot(cache_path=True)

num_msg = 0
num_reply = 0

# @bot.register()
# def recv_send_msg(recv_msg):
    
#     global num_msg 
#     num_msg = num_msg + 1
#     print("Recevied Message: %d type %s" %(num_msg, recv_msg.type))  
#     recv_msg.forward(bot.file_helper, prefix='转发消息: ')
#     return '' 

####### 监控星羽联盟群中的周日报名信息，周四报名时抢报
# 定位星羽联盟群
# print(bot.groups())
badminton_group = ensure_one(bot.groups().search('星羽联盟🏸'))

# 定位报名机器人
group_robot = ensure_one(badminton_group.search('运动去'))
group_lead = ensure_one(badminton_group.search('阿星'))

# 将群机器人的消息转发到文件传输助手
# @bot.register(badminton_group, TEXT)
@bot.register(badminton_group, TEXT)
def forward_robot_message(recv_msg):

    global num_msg 
    num_msg = num_msg + 1

    global num_reply

    print("\nReceived Message: %d type: %s group: %s" %(num_msg, recv_msg.type, recv_msg.chat))
    print("Message Content: \n %s" %(recv_msg.text))

    str_reply = "忽略。。。"
    prefix_tmp = "（无）"

    if recv_msg.member == group_robot :

        index_sunday = recv_msg.text.find("周二")
        index_shenggu = recv_msg.text.find("在胜古体育馆打羽毛球")
        index_in = recv_msg.text.find("已报人员名单：")
        index_waiting = recv_msg.text.find("替补人员名单：")
        index_me = recv_msg.text.find("王斌")

        print("机器人信息处理： sunday %d shenggu %d in %d waiting %d wangbin %d num_reply %d" \
                %(index_sunday, index_shenggu, index_in, index_waiting, index_me, num_reply))

        if index_sunday >= 0 and index_shenggu > index_sunday and index_in > index_shenggu :
        
            if index_me == -1 and num_reply < 30:
                num_reply = num_reply + 1
                if index_waiting == -1:
                    # 发送报名
                    str_reply = "报名周二"
                else:
                    str_reply = "替补周二"
                    # 发送替补
        prefix_tmp = "<<报名机器人信息>> "

    if recv_msg.member == group_lead :
        print("Message from 阿星 " )
        prefix_tmp = "<<阿星信息>> "
        

    recv_msg.forward(bot.file_helper, prefix=prefix_tmp)

    str_tmp = "<<我的回复>> " + str_reply
    bot.file_helper.send(str_tmp)

    return ""



embed()
