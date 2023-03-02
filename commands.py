from library import Tv_data, Tv_utility
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from database import Database
from settings import Settings


class Commands:
    def __init__(self, bot, chat_id, user_id, all_command):
        self.bot = bot
        self.chat_id = chat_id
        self.user_id = user_id
        self.tvd = Tv_data()
        self.tvu = Tv_utility()
        self.db = Database()
        self.admin = self.tvu.admin_control(self.user_id)
        self.all_command = all_command
        self.err =  """                                         
        -----------------------------------------------
            1 minute -   1m
        ---------------------------------
            5 minute  -  5m
        ---------------------------------
            15 minute -  15m
        ---------------------------------
            30 minute -  30m
        ---------------------------------
            1 hours   -  1h
        ---------------------------------
            2 hours   -  2h
        ---------------------------------
            4 hours   -  1h
        ---------------------------------
            1 week    -  1w
        ---------------------------------
            1 day     -  1d
        ---------------------------------
        ________________________
                             
           default 1 minute   
        ________________________
            """

    def command(self, command_one, command_two):
        rep = self.db.get_limit(self.user_id)
        if(self.admin):
            self.db.reset_limit(self.user_id)
        if(int(rep) > 15):
            self.bot.sendMessage(self.chat_id,"Günlük limitiniz tükendi!")
        else:
            if command_one =='/start':
                self.bot.sendMessage(self.chat_id,"test")
            elif(command_one == "/reset"):
                if(command_two == "user"):
                    if(self.admin):
                        self.bot.sendMessage(self.chat_id,"Günlük limit sıfırlandı!")
                        self.db.reset_limit(self.all_command[2])
                    else:
                        self.bot.sendMessage(self.chat_id,"Bu komutu sadece adminler çalışdıra bilir!")
                elif(command_two == "all"):
                    if(self.admin):
                        self.bot.sendMessage(self.chat_id,"Tüm limitler sıfırlandı!")
                        self.db.reset_all()
                    else:
                        self.bot.sendMessage(self.chat_id,"Bu komutu sadece adminler çalışdıra bilir!")
            elif(command_one == "/admin"):
                if(command_two == "add"):
                    if(self.admin):
                        self.bot.sendMessage(self.chat_id,"Admin elavə edildi!")
                        self.db.add_admin(self.all_command[2])
                    else:
                        self.bot.sendMessage(self.chat_id,"Bu komutu sadece adminler çalışdıra bilir!")
                elif(command_two == "all"):
                    if(self.admin):
                        # self.bot.sendMessage(self.chat_id,"Tüm limitler sıfırlandı!")
                        # self.db.reset_all()
                        pass
                    else:
                        self.bot.sendMessage(self.chat_id,"Bu komutu sadece adminler çalışdıra bilir!")

            elif(command_one == "/info"):
                    if(len(command_two) > 0):
                            if(command_two == "limit"):
                                info = self.db.get_limit(self.user_id)
                                self.bot.sendMessage(self.chat_id,f"Günlük limitiniz {15-info}!")
                            elif(command_two == "all"):
                                if(self.admin):
                                    info = self.db.all_user_info()
                                    self.bot.sendMessage(self.chat_id,info)
                                else:
                                    self.bot.sendMessage(self.chat_id,"Bu komutu çalışdıra bilmek içiin admin yetkisine sahip olmanız gerekir! ")

                            elif(command_two == "user"):
                                command_three = self.all_command[2]
                                print(command_three)
                                if(self.admin):
                                    try:
                                        info = self.db.info(command_three)
                                        self.bot.sendMessage(self.chat_id,info)
                                    except Exception as e:
                                        print(e)
                                        self.bot.sendMessage(self.chat_id,"Karşılık gelen kullanıcı yok")

                                else:
                                    self.bot.sendMessage(self.chat_id,"Bu komutu çalışdıra bilmek içiin admin yetkisine sahip olmanız gerekir! ")

                            
            elif(command_one == "/temel"):
                if(len(command_two) > 0):
                    data = ""
                    try:
                        data = self.tvd.temel(command_two.lower())
                    except IndexError:
                        self.bot.sendMessage(self.chat_id, "Hisse bulunmadı !")
                    self.bot.sendMessage(self.chat_id, str(data))
                    command_two = ""
                else:
                    self.bot.sendMessage(self.chat_id, "Hisse senedinin adini dahil edin!")

            elif(command_one == "/bilanco"):
                if(len(command_two) > 0):
                    data = ""
                    try:
                        data = self.tvd.bilanco(command_two.lower())
                    except NameError:
                        self.bot.sendMessage(self.chat_id, "Hisse bulunmadı !")
                    self.bot.sendMessage(self.chat_id, str(data))
                    command_two = ""
                else:
                    self.bot.sendMessage(self.chat_id, "Hisse senedinin adini dahil edin!")
            elif(command_one == "/grafik"):
                if(len(command_two) > 0):
                    data = ""
                    try:
                        data = self.tvd.gorselLinkGetir(command_two.lower())
                    except IndexError:
                        self.bot.sendMessage(self.chat_id, "Hisse bulunmadı !")
                    for graph in data:
                        self.bot.sendPhoto(self.chat_id, graph)
                    command_two = ""
                else:
                    self.bot.sendMessage(self.chat_id, "Hisse senedinin adini dahil edin!")

            elif(command_one == "/teknik"):
                if(len(command_two) > 0):
                    data = ""
                    try:
                        data = self.tvd.teknik(command_two.lower())
                    except Exception:
                        self.bot.sendMessage(self.chat_id, "Hisse bulunmadı !")
                    self.bot.sendMessage(self.chat_id, data)
                    command_two = ""
                else:
                    self.bot.sendMessage(self.chat_id, "Hisse senedinin adini dahil edin!")
          

            else:
                self.bot.sendMessage(self.chat_id, "Bilinmeyen emr")
