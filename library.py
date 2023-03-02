import requests as re
from bs4 import BeautifulSoup
from tradingview_ta import Interval, TA_Handler
import json as js
import datetime
import locale
from database import Database


class Tv_data:
    def __init__(self):
        self.header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
        self.util = Tv_utility()
        self.period = "1d"
        self.blanco_url = "https://fintables.com/api/screener?period=2022/12&filter=published_at||!kapanis||!gunluk_getiri||!piyasa_degeri||!net_kar||!yillik_net_kar_degisimi||!fk||!pddd||"

    def bilanco(self, hisse:str):
        rdata = ""
        res = re.get(self.blanco_url)
        data = js.loads(res.text)
        fdata = len(data["data"])
        try:
            for i in range(fdata+1):
                name = data["data"][i]
                if(name["0"].find(hisse.upper()) != -1):
                    break
        except IndexError:
            raise NameError("Hisse adı tapılmadı.")
        hisse_adi = name["0"]
        b_tarih = name["1"]
        kapanis = name["2"]
        ggetiri = name["3"]
        pdegeri = name["4"]
        netkar = name["5"]
        ynetkar = name["6"]
        fk = name["7"]
        pddd = name["8"]


        rdata = f"""
 ____________________________________________
        ----------------------------------
        Son bilanço tarihi: 
                 [ {b_tarih} ]
        ----------------------------------
        Hisse adı: {hisse_adi}
        ----------------------------------
        Kapanış fiyatı: {kapanis}
        ----------------------------------
        Günlük getiri: {ggetiri}
        ----------------------------------
        Piyasa değeri: {pdegeri}
        ----------------------------------
        Net kar: {netkar}
        ----------------------------------
        Yıllık net kar: {ynetkar}
        ----------------------------------
        F/K: {fk}
        ----------------------------------
        PD/DD: {pddd}
        ----------------------------------
        _________________________
        """
        return rdata

    def gorselLinkGetir(self, hisse:str):
        url = f"https://tr.tradingview.com/symbols/BIST-{hisse}/"
        page = re.get(url,headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")

        gorselLink = soup.find_all("div",attrs={"class":"tv-widget-idea__cover-wrap"})
        son3Gorsel=[]
        for i in range(3) :
            son3Gorsel.append(gorselLink[i].find("img").get("data-src"))
        return son3Gorsel


    def temel(self, hisse:str):
        url = f"https://tr.tradingview.com/symbols/BIST-{hisse}/financials-statistics-and-ratios/"
        page = re.get(url,headers=self.header)
        soup = BeautifulSoup(page.content, "html.parser")
        jsons = soup.find_all("script",attrs={"type":"application/prs.init-data+json"})
        bizim= jsons[3].__dict__['contents'][0]
        veri = js.loads(bizim)
        aciklama = veri[next(iter(veri))]['descriptions']
        yaziHali = ""
        for i in aciklama:
            if 'text' in aciklama[i]:
                yaziHali += aciklama[i]['text'] + "\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        yaziHali += "Veriler Tradingview tarafından sağlanmaktadır."
        return yaziHali


    def teknik(self, _symbol:str):
        coin = TA_Handler(
                        symbol=_symbol,
                        screener="turkey",
                        exchange="BIST",
                        interval=self.util.intervalSec(self.period))
        ind = coin.get_analysis().indicators
        price = coin.get_analysis().indicators['close']
        rec = coin.get_analysis().oscillators['COMPUTE']
        ma = coin.get_analysis().indicators
        recMa = coin.get_analysis().moving_averages['COMPUTE']
        ma_s = f"\n{self.util.emoji(recMa['SMA20'])}SMA20 : {round(ma['SMA20'],2)}\n{self.util.emoji(recMa['SMA50'])}SMA50 : {round(ma['SMA50'],2)}\n{self.util.emoji(recMa['SMA100'])}SMA100 : {round(ma['SMA100'],2)}\n{self.util.emoji(recMa['SMA200'])}SMA200 : {round(ma['SMA200'],2)}\n###############\n" \
                        f"{self.util.emoji(recMa['EMA20'])}EMA20 : {round(ma['EMA20'],2)}\n{self.util.emoji(recMa['EMA50'])}EMA50 : {round(ma['EMA50'],2)}\n{self.util.emoji(recMa['EMA100'])}EMA100 : {round(ma['EMA100'],2)}\n{self.util.emoji(recMa['EMA200'])}EMA200 : {round(ma['EMA200'],2)}"
        
        ind_s = f"\nHisse Adı : {_symbol}\nPeriyot : {self.period}\n\n###############\nFiyat : {price}\n{ma_s}\n###############\n{self.util.emoji(rec['RSI'])} RSI : {round(ind['RSI'],2)}\n{self.util.emoji(rec['CCI'])} CCI20 : {round(ind['CCI20'],2)} \n{self.util.emoji(rec['ADX'])} ADX : {round(ind['ADX'],2)}\n{self.util.emoji(rec['AO'])} AO : {round(ind['AO'],2)} \n{self.util.emoji(rec['Mom'])} MOM : {round(ind['Mom'],2)}\n{self.util.emoji(rec['W%R'])} WilliamsR {round(ind['W.R'],2)}\n⚪ Volume : {round(ind['volume'],2)}\n"
        return ind_s


class Tv_utility:
    def __init__(self):
        self.sunucuKonum = locale.getlocale()[0]
        self.db = Database()

    def yuvarla(self, data):
        data = str(data).replace(".0","").replace(".","")
        ydata = ""
        label = ""
        isMilyon = False
        if(len(data) < 10):
            ydata =  f"{int(data)/1000000}"
            isMilyon = True
        else:
            ydata =  f"{int(data)/1000000000}"
            isMilyon = False
        if(isMilyon):
            label = " Milyon"
        else:
            label = " Milyar"
        if(len(ydata.split(".")[1]) > 4):
            return ydata[:-4]+label
        else:
            return ydata+label



    def admin_control(self, user_id):
        data = list()
        adm = self.db.admins()
        for ad in adm:
            data.append(ad[0])
        if(str(user_id) in data):
            return True
        else:
            return False


    def intervalSec(self, data):
        try:
            if data == '1m':
                return Interval.INTERVAL_1_MINUTE
            if data == '5m':
                return Interval.INTERVAL_5_MINUTES
            if data == '15m':
                return Interval.INTERVAL_15_MINUTES
            if data == '30m':
                return Interval.INTERVAL_30_MINUTES
            if data == '1h':
                return Interval.INTERVAL_1_HOUR
            if data == '2h':
                return Interval.INTERVAL_2_HOURS
            if data == '4h':
                return Interval.INTERVAL_4_HOURS
            if data == '1d':
                return Interval.INTERVAL_1_DAY
            if data == '1w':
                return Interval.INTERVAL_1_WEEK
            else:
                return None
        except:
            pass

        
    def emoji(self, recommendation):
        try:
            if recommendation == "NEUTRAL":
                return "⚪"
            elif recommendation == "BUY":
                return "🟢"
            elif recommendation == "SELL":
                return "🔴"
        except:
            pass


    def zaman(self):
        while True:
            bugun = datetime.datetime.today()
            fark = datetime.timedelta(hours=3) if self.sunucuKonum != "tr_TR" else datetime.timedelta(hours=0)
            tr = bugun + fark
            saat = tr.hour
            dakika = tr.minute
            if saat == 0 and dakika == 15:
                self.db.reset_all()