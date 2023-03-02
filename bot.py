import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from commands import Commands
from database import Database

db = Database()
class FinanceBot:
    def __init__(self, api):
        self.command_one = ""
        self.command_two = ""
        self.bot = telepot.Bot(api)
        self.bot.deleteWebhook()



    def handle(self, msg):
        user = msg["from"]
        user_id = user["id"]

        if(db.id_exist(user_id) == 0):
            db.register(user)
        else:
            db.set_limit(user_id)

        chat_id = msg['chat']['id']
        command = msg['text'].split(" ")
        comm = Commands(self.bot, chat_id, user_id, command)
        try:
            self.command_one = command[0]
            self.command_two = command[1]
        
            print('Komut 1: %s' % self.command_one)
            print('Komut 2: %s' % self.command_two)
            comm.command(self.command_one, self.command_two)

        except IndexError:
            pass
    


    def run(self):
        try:
            self.bot.message_loop(self.handle)
            print('Komut bekleniyor...')
        except TimeoutError:
            print("TimeOut xetasi bas verdi")
            pass

        while 1:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                print('\n Program sonlandı')
                exit()
            except:
                print('Hata')