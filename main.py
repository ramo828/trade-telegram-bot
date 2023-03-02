from bot import FinanceBot
from library import Tv_utility
import threading
from settings import Settings

bot = FinanceBot(Settings.telegram_api)
util = Tv_utility()

thread1 = threading.Thread(target=bot.run)
thread2 = threading.Thread(target=util.zaman)

thread1.start()
thread2.start()

thread1.join()
thread2.join()