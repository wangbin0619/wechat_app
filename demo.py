
from wxpy import *

bot = Bot(cache_path=True)

@bot.register()
def recv_send_msg(recv_msg):
    print('Recevied Message: ',recv_msg.text)   
    recv_msg.forward(bot.file_helper,prefix='Received Msg: ')
    return '' 

embed()
