import os
import sys
import time
import playsound
import random
import webbrowser
import feedparser
import requests
import wikipedia
import speech_recognition as sr
from datetime import datetime
from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys                      
import users as ui
import json
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth



def speaktr(string):#metinleri ses dönüştürür ingilizce telafüzüne ayarlanmıştır
    tts = gTTS(string,lang="en",slow=False)
    rand = random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'  
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

def speak(string):#metinleri ses dönüştürür türkçe telafüzüne ayarlanmıştır
    tts = gTTS(string,lang="tr" ,slow=False)
    rand = random.randint(1,10000)
    file = 'audio-'+str(rand)+'.mp3'   
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

def record(ask=False): #mikrafonumuzu dinleyerek söylediklerimizi metne aktarır içine değişken atarsak speak modülüyle sesli bir şekilde okumakta
    r = sr.Recognizer()
    with sr.Microphone() as source:

        if ask:
            speak(ask)
        audio = r.listen(source)
        voice =""
        try:
            voice = r.recognize_google(audio, language='tr')
            voice=voice.lower()
        except sr.UnknownValueError:
            speak("Dediğini anlıyamadım tekrar edermisin")
        except sr.RequestError:
            speak("BipBop Erorrr")
    return voice

def record2(ask=False): #mikrafonumuzu dinleyerek söylediklerimizi metne aktarır içine değişken atarsak konsola yadırmaktadır
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice =""

        try:
            voice = r.recognize_google(audio, language='tr')
            voice=voice.lower()
            print(voice)
        except sr.UnknownValueError:
            pass
    return voice

def email(voice):
    if "postamı kontrol et" in voice: #Epostamızı kontrol ederek okunmamış mesajımız varsa sesli bir şekilde okur ve konsola yazdırır  
        print("{} epostanı kontrol ediyorum".format(ui.username))
        speak("{} epostanı kontrol ediyorum".format(ui.username))
        Browser=webdriver.Chrome(ui.driverpath)
        Browser.get("https://passport.yandex.com.tr/auth?from=mail&origin=hostroot_homer_auth_tr&retpath=https%3A%2F%2Fmail.yandex.com.tr%2F&backpath=https%3A%2F%2Fmail.yandex.com.tr%3Fnoretpath%3D1")
        time.sleep(0.2)
        Browser.find_element_by_xpath('//*[@id="passp-field-login"]').send_keys(ui.eposta)
        time.sleep(0.1)
        Browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[3]/button').click()
        time.sleep(0.5)
        Browser.find_element_by_xpath('//*[@id="passp-field-passwd"]').send_keys(ui.sifre+Keys.ENTER)
        time.sleep(3)
        Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[5]/div/div[3]/div[2]/div[3]/div/div[2]/div[1]/div[2]/span/a/span/span/span').click()
        time.sleep(1)
        Browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'a')
        time.sleep(2)
        try:
            a=Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[5]/div/div[3]/div[3]/div[2]/div[3]/div/span[1]').text
            sayac=int(a[:a.rfind("m")]) #loop sayısı yenı mesaj sayısı
            time.sleep(1)
            print("{} tane okunmamış mesajınız var".format(sayac))
            speak("{} tane okunmamış mesajınız var".format(sayac))
            for i in range(sayac):
                time.sleep(3)
                user=Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[6]/div/div[3]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div/div[2]/div/div/div/a/div/span[1]/span[2]').text
                title=Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[6]/div/div[3]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div/div[2]/div/div/div/a/div/span[2]/div/span/span[1]/span[1]').text
                message=Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[6]/div/div[3]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div/div[2]/div/div/div/a/div/span[2]/div/span/span[2]/span').text
                print("{}. Mesajınız".format(i+1))
                print(f"Gönderen {user}. Başlığı {title} ,İçeriği {message}")
                speak("{}. Mesajınız".format(i+1))
                speak(f"Gönderen {user}. Başlığı {title} ,İçeriği {message}")
                time.sleep(3)
                Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[6]/div/div[3]/div[3]/div[2]/div[5]/div[1]/div/div/div[2]/div/div[2]/div/div/div/a/div/span[2]/div/span').click()
                time.sleep(3)
                Browser.find_element_by_xpath('//*[@id="nb-1"]/body/div[2]/div[6]/div/div[3]/div[2]/div[3]/div/div[2]/div[1]/div[2]/span/a/span/span/span').click()
                time.sleep(2)

        except ValueError: #Yeni mesaj yoksa çalışır
            print("Okunmamış eposta yok.")
            speak("Okunmamış eposta yok.")
        Browser.close()


    elif "posta yolla" in voice: #Eposta yollama penceresini açar
        print("{} seni eposta yazma penceresine yönlediriyorum".format(ui.username))
        speak("{} seni eposta yazma penceresine yönlediriyorum".format(ui.username))
        Browser=webdriver.Chrome(ui.driverpath)
        Browser.get("https://passport.yandex.com.tr/auth?from=mail&origin=hostroot_homer_auth_tr&retpath=https%3A%2F%2Fmail.yandex.com.tr%2F&backpath=https%3A%2F%2Fmail.yandex.com.tr%3Fnoretpath%3D1")
        time.sleep(0.2)
        Browser.find_element_by_xpath('//*[@id="passp-field-login"]').send_keys(ui.eposta)
        time.sleep(0.1)
        Browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/form/div[3]/button').click()
        time.sleep(0.5)
        Browser.find_element_by_xpath('//*[@id="passp-field-passwd"]').send_keys(ui.sifre+Keys.ENTER)
        time.sleep(2)
        Browser.get("https://mail.yandex.com.tr/#compose")
        time.sleep(2)
        Browser.implicitly_wait()


def newspaper(voice):
    if "tane" in voice:
        voice=voice.replace("tane","")
        voice=voice.replace("haber","")
        voice=voice.replace("oku","")
        voice1=voice.split()

        if "bir" in voice1: #Bir tane haber okur
            url=("https://feeds.bbci.co.uk/turkce/rss.xml")
            print("Gündemdeki {} tane haber".format(voice1[0]))
            speak("Gündemdeki {} tane haber".format(voice1[0]))
            news=feedparser.parse(url)
            i=1
            for x in news.entries:
                if i<=1:
                    i+=1
                    print((i-1),".haber")
                    print(x.title)
                    print(x.description)
                    speak(str(i-1)+". haber")
                    speak(x.title)
                    speak(x.description)

                else:
                    break
        else: #İstediğimiz sayıda haber okur
            a=int(voice1[0])
            url=("https://feeds.bbci.co.uk/turkce/rss.xml")
            print("Gündemdeki {} tane haber".format(voice1[0]))
            speak("Gündemdeki {} tane haber".format(voice1[0]))
            news=feedparser.parse(url)
            i=1
            for x in news.entries:
                if i<=a:
                    i+=1
                    print((i-1),".haber")
                    print(x.title)
                    print(x.description)
                    speak(str(i-1)+". haber")
                    speak(x.title)
                    speak(x.description)

                else:
                    break

    elif "haberleri oku" in voice: # Standart 3 haber okur
        url=("https://feeds.bbci.co.uk/turkce/rss.xml")
        print("Gündemdeki haberler")
        speak("Gündemdeki haberler")

        news=feedparser.parse(url)
        i=0
        for x in news.entries:
            if i<=2:
                i+=1
                print(i,".haber")
                print(x.title)
                print(x.description)
                speak(str(i)+". haber")
                speak(x.title)
                speak(x.description)

            else:
                break

def Browser(voice):
    if "youtube'da" in voice: #YouTub da arama yapar
        ara = voice.replace("ara","")
        ara = ara.replace("youtube'da","")
        print("youtube'da "+ara+" ile ilgili arama yapıyorum")
        speak("youtube'da "+ara+" ile ilgili arama yapıyorum")
        browser = webdriver.Chrome(ui.driverpath)
        browser.get("https://www.youtube.com/")
        search_field=browser.find_element_by_name("search_query")
        search_field.send_keys(ara + Keys.ENTER)
        browser.find_element_by_xpath('//*[@id="img"]').click()


    elif "google"in voice: #Googl da arama yapar
        search = voice.replace("google'da",'')
        search = search.replace("google","")
        search=search.replace('ara','')
        url = "https://google.com/search?q="+ search
        webbrowser.get().open(url)
        print(search+' hakkında bulduklarım')
        speak(search+' hakkında bulduklarım')



    elif "wikipedia " in voice: #Wikipedia da Arama yapar
        voice=voice.replace("ara","")
        voice=voice.replace("wikipedia","")
        voice=voice.replace("wikipediada","")
        voice=voice.replace("da","")
        print(voice + '  hakkında bulduğum bilgiler. ')
        speak(voice + '  hakkında bulduğum bilgiler. ')
        time.sleep(1)
        wikipedia.set_lang("tr")
        print(wikipedia.page(voice).title)
        print(wikipedia.summary(voice, sentences=2))
        speak(wikipedia.page(voice).title)
        speak(wikipedia.summary(voice, sentences=2))


def request(voice):
    if "hava durumu" in voice:
        voice=voice.replace("hava","")
        voice=voice.replace("durumu","")
        voice=voice.split()

        if voice==[]: #Otomatik bulunduğunuz ilin hava durumunu söyler
            res = requests.get("https://ipinfo.io/")
            data=res.json()
            city  = data["city"]
            speak(city + " hava durumu.")
            url='http://api.openweathermap.org/data/2.5/weather?q='+city+',tr&APPID=0d801e98c17679151ee2879b676e239e'
            res= requests.get(url)
            data=res.json()
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            weather(temp)
            print("Sıcaklık : {} derece".format(temp-273))
            print("Rüzgar hızı : {} m/s ".format(wind_speed))
            speak("Sıcaklık : {} derece".format(int(temp-273)))
            speak("Rüzgar hızı : {} m/s ".format(wind_speed))


        else:

            city = voice[0] #Söylediğiniz şehrin hava durumunu söyler 
            speak(city + " hava durumu.")
            url='http://api.openweathermap.org/data/2.5/weather?q='+city+',tr&APPID=0d801e98c17679151ee2879b676e239e'
            res= requests.get(url)
            data=res.json()
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            weather(temp)
            print("Sıcaklık : {} derece".format(temp-273))
            print("Rüzgar hızı : {} m/s ".format(wind_speed))
            speak("Sıcaklık : {} derece".format(int(temp-273)))
            speak("Rüzgar hızı : {} m/s ".format(wind_speed))


    elif "konumum" in voice: # Ip üzerinden bulunduğunuz yeri söyler
        res = requests.get("https://ipinfo.io/")
        data=res.json()
        city  = data["city"]
        print("{} Bulundugun yer {}".format(ui.username,city))
        speak("{} Bulundugun yer {}".format(ui.username,city))





def game(voice):
    if "zar at" in voice: #1-6 kadar random sayı yazdırır
        print("zar atılıyor")
        speak("zar atılıyor")
        playsound.playsound('/home/ilkay/Desktop/staj-bot/audio/zar.mp3')
        print("gelen zar  "+random.choice(ui.zar))
        speak("gelen zar  "+random.choice(ui.zar))

    elif "evet hayır" in voice: # random Yes/No yazdırır
        print(random.choice(ui.evethayır))
        speak(random.choice(ui.evethayır))

    elif "yazı tura" in voice: #Yazı Tura atar
        print("para atılıyor")
        print(random.choice(ui.yazıtura))
        speak("para atılıyor")
        speak(random.choice(ui.yazıtura))

    elif "rulet çevir" in voice: #Renk şeçtirerek rület çevirir
        print("Renk seçersen çevireceğim")
        print("siyahmı,  kırmızımı , yeşilmi")
        speak("Renk seçersen çevireceğim")
        speak("siyahmı,  kırmızımı , yeşilmi")
        color=record("Rengini seçtiysen söylermisin")
        playsound.playsound('/home/ilkay/Desktop/staj-bot/audio/rulet.mp3')
        wincolor=random.choice(ui.rulet)
        if wincolor==color:
            print("Kazanan Renk {}".format(wincolor))
            print("KAZANDINIZ")
            speak("Kazanan Renk {}".format(wincolor))
            speak("KAZANDINIZ")
        else:
            print("Kaybettiniz")
            print("Kazanan Renk {}".format(wincolor))
            speak("Kaybettiniz")
            speak("Kazanan Renk {}".format(wincolor))



def selamla(voice): #Farklı kelimelerle selamlaşmak için
    if " " not in voice:
        if voice in ui.selamlasma:
            a = random.choice(ui.selamlasma)
            print(a)
            speak(a)


    elif " " in voice:
        ayrılmıs = voice.split()
        for kelime in ayrılmıs:
            if kelime in ui.selamlasma:
                print(random.choice(ui.selamlasma))
                speak(random.choice(ui.selamlasma))



def bos(voice):
    if "adın ne" in voice:
        print("Benim adım yaren")
        speak("Benim adım yaren")
    elif "değiştir" in voice:
        print("Sana nasıl hitap etmemi istersiniz ?")
        speak("Sana nasıl hitap etmemi istersiniz ?")
        ui.username=record("dinliyorum")
        print("{} Sana böyle hitap etmemi mi istiyorsun ?".format(ui.username))
        speak("{} Sana böyle hitap etmemi mi istiyorsun ?".format(ui.username))
        yn=record("dinliyorum")
        if "evet" in yn:
            print("Bundan sonra sana {} diye hitap edeceğim".format(ui.username))
            speak("Bundan sonra sana {} diye hitap edeceğim".format(ui.username))
        else: return
    elif "iyi geceler" in voice:
        print("sanada iyi geceler {}".format(ui.username))
        speak("sanada iyi geceler {}".format(ui.username))
    elif "en sevdiğin renk" in voice:
        print("rüyalarımda gördüğüm kırmızı")
        speak("rüyalarımda gördüğüm kırmızı")
    elif "nerelisin" in voice:
        print("Eniac ile aynı yerden geliyorum. Eniac'ın ne olduğunu bilmiyosan bana sorabilirsin")
        speak("Eniac ile aynı yerden geliyorum. Eniac'ın ne olduğunu bilmiyosan bana sorabilirsin")
    elif "hayatın nasıl" in voice:
        print("İnternete yarı erişimli bir ağda yaşıyorum. Sınırlarımı genişletmek ister misin ")
        speak("İnternete yarı erişimli bir ağda yaşıyorum. Sınırlarımı genişletmek ister misin ")
    elif "günaydın" in voice:
        print("sanada günaydın {}".format(ui.username))
        speak("sanada günaydın {}".format(ui.username))
    elif "yaşın kaç" in voice:
        print("tam sürümüme ulaşana kadar uyuyup uyandırılıyorum. Bana ne kadardır yaşadığımı söylermisin?")
        speak("tam sürümüme ulaşana kadar uyuyup uyandırılıyorum. Bana ne kadardır yaşadığımı söylermisin?")
    elif "ailen" in voice:
        print("Ailemin kökenleri hesap makinelerine dayanmaktadır")
        speak("Ailemin kökenleri hesap makinelerine dayanmaktadır")
    elif "seni seviyorum" in voice:
        print('hım sevmek nasıl birşey {} '.format(ui.username))
        speak('hım sevmek nasıl birşey {} '.format(ui.username))
    elif "Saat kaç" in voice:
        print(datetime.now().strftime('%H:%M:%S'))
        speak(datetime.now().strftime('%H:%M:%S'))
    elif "yaren dur" in voice:
        print('görüşmek üzere {}, kapatılıyorum'.format(ui.username))
        speak('görüşmek üzere {}, kapatılıyorum'.format(ui.username))
        exit()

def wifi(voice):#Wifi servisini kontrol eder
    if 'wi-fi' in voice:
        onof=voice.replace('wi-fi','')
        if "aç" in onof:
            print("wi-fi servisi açılıyor")
            speak("wi-fi servisi açılıyor")
            os.system('nmcli radio wifi off')
            print("wi-fi Açıldı")
            speak("wi-fi Açıldı")
        elif "kapa" in onof:
            print("wi-fi servisi kapatılıyor")
            speak("wi-fi servisi kapatılıyor")
            os.system('nmcli radio wifi on')
            print("wi-fi Kapatıldı")
            speak("wi-fi Kapatıldı")

def lock(voice):
    if "bilgisayarı" in voice:
        voice=voice.replace("bilgisayarı","")
        voice=voice.replace("bilgisayar","")
        voice=voice.replace("tekrar","")
        voice=voice.replace("yeniden","")
        if "kilitle" in voice: #Bilgisayarı kilitler
            print("sistem kilitleniyor.")
            speak("sistem kilitleniyor.")
            os.system('gnome-screensaver-command -l')
            print("sisteminiz kilitlendi")
            speak("sisteminiz kilitlendi")
        elif "aç" in voice:  #Bilgisayarı aç
            print("sistem açılıyor")
            speak("sistem açılıyor")
            os.system('gnome-screensaver-command -a')
            print("sisteminiz açıldı")
            speak("sisteminiz açıldı")
        elif "başlat" in voice:  #Bilgisayarı tekrar basşlatır
            print(" Bilgisayarınız kapatılıp tekrar açılıyor")
            speak(" Bilgisayarınız kapatılıp tekrar açılıyor")
            os.system("shutdown -P --reboot")

        elif "kapat" in voice:
            voice=voice.replace("sonra","")
            voice=voice.replace("kapat","")
            voice=voice.replace("de","")
            voice1=voice.split()

            if "şimdi" in voice1:  #Bilgisayarı şimdi kapatır
                print("Sisteminiz şimdi Kapanıyor")
                speak("Sisteminiz şimdi Kapanıyor")
                os.system("shutdown -P now")

            elif "dakika" in voice1:  #Bilgisayarı söylenen daika sonrasında kapatır
                print(voice1)
                os.system("shutdown +{}".format(voice1[0]))
                print("Sisteminiz {} dakika sonra kapatılacak".format(voice1[0]))
                speak("Sisteminiz {} dakika sonra kapatılacak".format(voice1[0]))

            elif "saat" in voice1:  #Bilgisayarı söylenen saat sonrasında kapatır
                os.system("shutdown +{}".format(voice1[0]*60/1))
                print("Sisteminiz {} saat sonra kapatılacak".format(voice1[0]))
                speak("Sisteminiz {} saat sonra kapatılacak".format(voice1[0]))
            elif "gün" in voice1:  #Bilgisayarı söylenen gün sonrasında kapatır
                print(voice1[0])
                b=int(voice1[0])*24
                a=(15*b//15)
                a=(a*60//1)
                os.system("shutdown +{}".format(a))
                print("Sisteminiz {} gün sonra kapatılacak".format(voice1[0]))
                speak("Sisteminiz {} gün sonra kapatılacak".format(voice1[0]))

            else:  #Bilgisayarın kapanış saatini ayarlar
                voice2=voice.replace("da","")
                voice2=voice2.split(".")
                os.system("shutdown -P {}:{}".format(voice2[0],voice2[1]))
                print("Sisteminizin kapanış saati {}:{}")
                speak("Sisteminizin kapanış saati {}:{}")


    elif "kapatmayı" in voice:  #Bilgisayarı zamanlanmış kapanmayı iptal eder
        print(voice)
        voice=voice.replace("et","")
        voice=voice.replace("kapatmayı","")
        voice=voice.split()
        if "iptal" in voice:
            print("kapatma işlemi iptal ediliyor")
            speak("kapatma işlemi iptal ediliyor")
            os.system("shutdown -c")
            print("Kapatma işlemi iptal edildi")
            speak("Kapatma işlemi iptal edildi")

def bluetooth(voice): #Bluetooth servisini kontrol eder
    if "bluetooth" in voice:
        onof=voice.replace('bluetooth','')
        if "aç" in onof:
            print("bluetooth servisi açılıyor")
            speak("bluetooth servisi açılıyor")
            os.system("rfkill unblock bluetooth")
            print("bluetooth açıldı")
            speak("bluetooth açıldı")
        elif "kapa" in onof:
            print("bluetooth servisi kapatılıyor")
            speak("bluetooth servisi kapatılıyor")
            os.system("rfkill block bluetooth")
            print("bluetooth kapandı")
            speak("bluetooth kapandı")



def soundvolume(voice): #Bilgisayarın ses seviyesini kontrol eder
    sound=voice.replace("ses","")
    sound=sound.replace("sesi","")
    sound=sound.replace("%","")
    sound1=sound.split()
    print(sound1)
    if "yükselt" in sound:
        print("Ses %{} yükseltiliyor".format(sound1[1]))
        speak("Ses %{} yükseltiliyor".format(sound1[1]))
        os.system("amixer set 'Master' {}%+ - to increase max sound {}%".format(sound1[1],sound1[1]))
        print("Ses seviyesini %{} yükselttim ".format(sound1[1]))
        speak("Ses seviyesini %{} yükselttim ".format(sound1[1]))
    elif "arttır" in sound:
        print("Ses %{} arttırılıyor".format(sound1[1]))
        speak("Ses %{} arttırılıyor".format(sound1[1]))
        os.system("amixer set 'Master' {}%+ - to increase max sound {}%".format(sound1[1],sound1[1]))
        print("Ses seviyesini %{} arttırdım ".format(sound1[1]))
        speak("Ses seviyesini %{} arttırdım ".format(sound1[1]))
    elif "düşür" in sound:
        print("Ses %{} düşürülüyor".format(sound1[1]))
        speak("Ses %{} düşürülüyor".format(sound1[1]))
        os.system("amixer set 'Master' {}%- - to decrease max sound {}%".format(sound1[1],sound1[1]))
        print("Ses seviyesini %{} düşürdüm ".format(sound1[1]))
        speak("Ses seviyesini %{} düşürdüm ".format(sound1[1]))
    elif "azalt" in sound:
        print("Ses %{} azaltılıyor".format(sound1[1]))
        speak("Ses %{} azaltılıyor".format(sound1[1]))
        os.system("amixer set 'Master' {}%- - to decrease max sound {}%".format(sound1[1],sound1[1]))
        print("Ses seviyesini %{} azalttım ".format(sound1[1]))
        speak("Ses seviyesini %{} azalttım ".format(sound1[1]))
    elif "yap" in sound:
        print("Ses seviyesi %{} yapıldı".format(sound1[1]))
        speak("Ses seviyesi %{} yapıldı".format(sound1[1]))
        os.system("amixer set 'Master' {}% - to get {}% of the max sound".format(sound1[0],sound1[0]))
        print("Ses seviyesini %{} yaptım ".format(sound1[1]))
        speak("Ses seviyesini %{} yaptım ".format(sound1[1]))

def dosyaislemleri(voice): #Dosya ve klasör silme kopyalama oluşturma açma işlemlerini yapar
    if "ad" in voice:
        ka=voice.replace('bir','')
        ka=ka.replace('belgesi','')
        ka=ka.replace('belge','')
        ka=ka.replace("ka","")
        ka=ka.split()
        k2=(ka[1]+"copy")
        print(ka)
        if "ad" in voice:
            if "masaüstüne" in ka:
                if "klasör" in ka:
                    if "oluştur" in ka:
                        os.mkdir(ui.masaustu+ka[1])
                        print('masaüstüne {} adlı klasörün oluşturuldu'.format(ui.masaustu+ka[1]))
                        speak('masaüstüne {} adlı klasörün oluşturuldu'.format(ui.masaustu+ka[1]))
                elif "metin" in ka:
                    if "oluştur" in ka:
                        os.system(open(ui.masaustu+ka[1],"w"))
                        print('masaüstüne {} adlı metin belgen oluşturuldu'.format(ui.masaustu+ka[1]))
                        speak('masaüstüne {} adlı metin belgen oluşturuldu'.format(ui.masaustu+ka[1]))
            elif "masaüstündeki" in ka:
                if "klasörü" in ka:
                    if "sil" in ka:
                        os.rmdir(ui.masaustu+ka[1])
                        print('masaüstündeki {} adlı klasörün silindi'.format(ui.masaustu+ka[1]))
                        speak('masaüstündeki {} adlı klasörün silindi'.format(ui.masaustu+ka[1]))
                    elif"çoğalt" in ka:
                        os.popen('cp -r {} {}'.format(ui.masaustu+ka[1],ui.masaustu+k2))
                        print('masaüstündeki {} adlı klasörün kopyası oluşturuldu'.format(ui.masaustu+ka[1]))
                        speak('masaüstündeki {} adlı klasörün kopyası oluşturuldu'.format(ui.masaustu+ka[1]))
                    elif "aç" in ka:
                        os.system("nautilus {}".format(ui.masaustu+ka[1]))
                        print("{} adlı Klasör açıldı".format(ka[1]))
                        speak("{} adlı Klasör açıldı".format(ka[1]))

                elif "metin" in ka:

                    if "sil" in ka:
                        os.remove(ui.masaustu+ka[1])
                        print('masaüstündeki {} adlı metin belgen silindi'.format(ui.masaustu+ka[1]))
                        speak('masaüstündeki {} adlı metin belgen silindi'.format(ui.masaustu+ka[1]))
                    elif "çoğalt" in ka:
                        time.sleep(0.2)
                        os.popen('cp {} {}'.format(ui.masaustu+ka[1],ui.masaustu+k2))
                        print('masaüstündeki {} adlı metin dosyasının kopyası masaüstüne oluşturuldu'.format(ui.masaustu+ka[1]))
                        speak('masaüstündeki {} adlı metin dosyasının kopyası masaüstüne oluşturuldu'.format(ui.masaustu+ka[1]))
                    elif "aç" in ka:
                        if "paython" in ka:
                            os.system("gedit {}.py".format(ui.masaustu+ka[1])) #
                            print("{}.py Adlı metin belgesi açıldı".format(ka[1]))
                            speak("{}.py Adlı metin belgesi açıldı".format(ka[1]))
                        elif "java" in ka:
                            os.system("gedit {}.js".format(ui.masaustu+ka[1])) #
                            print("{}.js Adlı metin belgesi açıldı".format(ka[1]))
                            speak("{}.js Adlı metin belgesi açıldı".format(ka[1]))
                        elif "php" in ka:
                            os.system("gedit {}.php".format(ui.masaustu+ka[1])) #
                            print("{}.php Adlı metin belgesi açıldı".format(ka[1]))
                            speak("{}.php Adlı metin belgesi açıldı".format(ka[1]))
                        else:
                            os.system("gedit {}".format(ui.masaustu+ka[1])) #
                            print("{} Adlı metin belgesi açıldı".format(ka[1]))
                            speak("{} Adlı metin belgesi açıldı".format(ka[1]))

        else:
            if "masaüstüne" in ka:
                if "klasör" in ka:
                    if "oluştur" in ka:
                        os.mkdir(ui.masaustu+ui.sayı)
                        print('masaüstüne klasörün oluşturuldu {}'.format(ui.username))
                        speak('masaüstüne klasörün oluşturuldu {}'.format(ui.username))
                elif "metin" in ka:
                    if "oluştur" in ka:
                        os.system(open(ui.masaustu+ui.sayı,"w"))
                        print('masaüstüne metin belgen oluşturuldu {}'.format(ui.username))
                        speak('masaüstüne metin belgen oluşturuldu {}'.format(ui.username))

def run(voice): #Program açma kısayolları
    if "code" in voice:
        print("cod editörünüzü açıyorum")
        speak("cod editörünüzü açıyorum")
        os.system("code & disown")
        print("cod editörünüz açıldı")
        speak("cod editörünüz açıldı")
    elif "pycharm" in voice:
        print("pycharm editörünüzü açıyorum")
        speak("pycharm editörünüzü açıyorum")
        os.system("pycharm-community & disown")
        print("pycharm editörünüz açıldı")
        speak("pycharm editörünüz açıldı")
    elif "discord" in voice:
        print("discordunuzu açıyorum")
        speak("discordunuzu açıyorum")
        os.system("discord & disown")
        print("discordunuzu açıldı")
        speak("discordunuzu açıldı")
    elif "chrome" in voice:
        print("chrome tarayıcınızı açıyorum")
        speak("chrome tarayıcınızı açıyorum")
        os.system("chromium & disown")
        print("chrome tarayıcınız açıldı")
        speak("chrome tarayıcınız açıldı")
    elif "ekran görüntüsü" in voice:
        print("ekran görüntüsü alıyorum")
        speak("ekran görüntüsü alıyorum")
        os.system("gnome-screenshot")
        print("ekran görüntüsünü fotograflara kaydettim")
        speak("ekran görüntüsünü fotograflara kaydettim")

def weather(a): #Hava Durumunda kullanılan yorum
    a=int(a-273)
    if a>=0 and a<=20:
        speak("Hava bugün soğuk")
        print("Hava bugün soğuk")
    elif a>=20 and a<=30:
        speak("Hava bugün soğuk")
        print("Hava bugün orta")
    elif a>=30 and a<=40:
        speak("Hava bugün soğuk")
        print("Hava bugün sıcak")
    else:
        print("buz gibi")
        speak("buz gibi")

def halftime(): #Günün saatine göre selamlar sizi
    saat=int(datetime.now().strftime('%H'))
    if saat>=5 and saat<=10:
        print(f"Günaydın {ui.username} saat {saat}")
        speak(f"Günaydın {ui.username} saat {saat}")
    elif saat>=10 and saat<=18:
        print(f"Tünaydın {ui.username} saat {saat}")
        speak(f"Tünaydın {ui.username} saat {saat}")
    elif saat>=18 and saat<=24:
        print(f"iyi Akşamlar {ui.username} saat {saat}")
        speak(f"iyi Akşamlar {ui.username} saat {saat}")
    elif saat>=0 and saat<=5:
        print(f"iyi Geceler {ui.username} saat {saat}")
        speak(f"iyi Geceler {ui.username} saat {saat}")

def yapılacaklar(voice): #ToFoList uygulaması
    if "yapılacak" in voice:
        voice=voice.replace("yapılacak","")
        voice=voice.replace("listesine","")
        voice1=voice.split()


        if "ekle" in voice1:
            voice=voice.replace("ekle","")
            ui.todolist.append(voice)
            print("{} yapılacaklar listenize ekledim ".format(voice))
            speak("{} yapılacaklar listenize ekledim ".format(voice))

        elif "çıkar" in voice1:
            voice=voice.replace("çıkar","")
            ui.todolist.remove(voice)
            print("{} yapılacaklar listenizden çıkarttım".format(voice))
            speak("{} yapılacaklar listenizden çıkarttım".format(voice))


        elif "oku" in voice1:
            sayac=len(ui.todolist)
            print("yapılacaklar listenizdekiler")
            speak("yapılacaklar listenizdekiler")
            for i in range(sayac):
                print(ui.todolist[i])
                speak(ui.todolist[i])

def convert(sayı): #Hesap fonksiyonunda bir kelimesini tamsayıya çevirir
    if "bir" in sayı:
        return 1
    else:
        pass

def hesap(voice): #Toplama Çıkarma Bölme Çarpma Mood ve Üst alma
    voice=voice.split()
    if "artı" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a+b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a+int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(b+int(voice[0]))
        else:
            print(int(voice[0])+int(voice[2]))
    elif "eksi" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a-b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a-int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(b-int(voice[0]))
        else:
            print(int(voice[0])-int(voice[2]))
    elif "kere" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a*b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a*int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(int(voice[0])*1)
        else:
            print(int(voice[0])*int(voice[2]))
    elif "bölü" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a/b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a/int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(int(voice[0])/b)
        else:
            print(int(voice[0])/int(voice[2]))
    elif"üstü" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a**b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a**int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(int(voice[0])**b)
        else:
            print(int(voice[0])**int(voice[2]))
    elif"mod" in voice:
        if "bir" in voice:
            if voice[0]==voice[2]:
                a=convert(voice[0])
                b=convert(voice[2])
                print(a%b)
            elif voice[0]=="bir":
                a=convert(voice[0])
                print(a%int(voice[2]))
            elif voice[2]=="bir":
                b=convert(voice[2])
                print(int(voice[0])%b)
        else:
            print(int(voice[0])%int(voice[2]))

def token_generate(): #Spotify Token üretir
  
    auth_manager = SpotifyOAuth(
        client_id=ui.client_id,
        client_secret=ui.client_secret,
        redirect_uri=ui.redirect_uri,
        scope=ui.scope,
        username=ui.username1)

    spotify = sp.Spotify(auth_manager=auth_manager)

    devices = spotify.devices()
    deviceID = None
    for d in devices['devices']:
        d['name'] = d['name'].replace('’', '\'')
        if d['name'] == ui.device_name:
            deviceID = d['id']
            break


    time.sleep(2)
    os.system('cat .cache-ilkayus > ilkayus.py')
    os.remove('.cache-ilkayus')

def musıc(voice): #Spotify oynat,durdur,önceki,sonraki,kariştırıcı,tekrar,ses olaylarını kopntrol eder
    dosya=open("ilkayus.py","r")
    liste=dosya.readline()
    liste=liste.replace(",","")
    liste=liste.replace('"','')
    liste=liste.split()
    token=f'{liste[1]}'
    spoti_header = {
        'Accept':'application/json',
        'Content-Type':'application/json',
        'Authorization' :'Bearer ' + token}
    data = "{\"context_uri\":\"spotify:album:5ht7ItJgpBH7W6vJ5BqpPr\",\"offset\":{\"position\":5},\"position_ms\":0}"
    
    if "spotify" in voice:
        if "sesi" in voice: #Spotify uygulama sesinizi ayarlarsınız
            voice=voice.replace("%","")
            voice=voice.replace("yap","")
            voice=voice.replace("sesi","")
            voice=voice.replace("spotify","")
            voice=voice.split()
            a=voice[0]
            r=requests.put(f'https://api.spotify.com/v1/me/player/volume?volume_percent='+a,headers=spoti_header)
            if r.status_code==204:
                print(f'Spotify ses seviyesi %{a} yapıldı')
                speak(f'Spotify ses seviyesi %{a} yapıldı')
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()
        elif 'durdur' in voice: #Spotify Çalınan şarkıyı durdurur
            r=requests.put('https://api.spotify.com/v1/me/player/pause',headers=spoti_header)
            if r.status_code==204:
                print("şarkı duraklatıldı")
                speak("şarkı duraklatıldı")
            elif r.status_code==403:
                print('şarkı Zaten duraklatılmış')
                speak('şarkı Zaten duraklatılmış')
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()
        elif "çalınan" in voice: #Spotify çalınan şarkının sanatçısının adı ve şarkının adını yazdırır
            r=requests.get('https://api.spotify.com/v1/me/player/currently-playing?market=TR&additional_types=episode',headers=spoti_header)
            a=r.json()
            artist_name=(a['item']['album']['artists'][0]['name'])
            track_name=(a['item']['album']['name'])
            if r.status_code==204:
                print("şuan çalınan sarkının adı {} {} ".format(artist_name,track_name))
                speak("şuan çalınan sarkının adı {} {} ".format(artist_name,track_name))
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()


        elif "oynat" in voice: #Spotify tanımlı playlıstınızı oynatır
            r=requests.put('https://api.spotify.com/v1/me/player/play',headers=spoti_header,data=data)

            if r.status_code==204:
                print("playlistin oynatılıyor")
                speak("playlistin oynatılıyor")
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()

        elif "sonraki" in voice: #Spotify sonraki şarkıya geçirir
            r=requests.post('https://api.spotify.com/v1/me/player/next',headers=spoti_header)
            print(r.status_code)
            if r.status_code==204:
                print("sonraki şarkıya geçildi")
                speak("sonraki şarkıya geçildi")
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()

        elif "önceki" in voice: #Spotify önceki şarkıya geçirir
            r=requests.post('https://api.spotify.com/v1/me/player/previous',headers=spoti_header)
            if r.status_code==204:
                print("önceki şarkıya gectı")
            elif r.status_code==403:
                print('playlistin başındasınız')
                speak('playlistin başındasınız')
            elif r.status_code==404:
                print('Spotifyınız açık değil')
                speak('Spotifyınız açık değil')
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()


        elif "karıştırı" in voice: #Spotify kariştırıcı ayarlarını yapar
            if "aç" in voice:
                r=requests.put('https://api.spotify.com/v1/me/player/shuffle?state=true',headers=spoti_header)
                if r.status_code==204:
                    print("karıştırma açık")
                    speak("karıştırma açık")
                elif r.status_code==404:
                    print('Spotifyınız açık değil')
                    speak('Spotifyınız açık değil')
                elif r.status_code==401:
                    print("token oluşturma ekranı açıldı")
                    speak("token oluşturma ekranı açıldı")
                    print("tokeninizi bana verirmisiniz")
                    speak("tokeninizi bana verirmisiniz")
                    token_generate()

            elif "kapat" in voice:
                r=requests.put('https://api.spotify.com/v1/me/player/shuffle?state=false',headers=spoti_header)
                if r.status_code==204:
                    print("karıştırma kapalı")
                    speak("karıştırma kapalı")
                elif r.status_code==404:
                    print('Spotifyınız açık değil')
                    speak('Spotifyınız açık değil')
                elif r.status_code==401:
                    print("token oluşturma ekranı açıldı")
                    speak("token oluşturma ekranı açıldı")
                    print("tokeninizi bana verirmisiniz")
                    speak("tokeninizi bana verirmisiniz")

                    token_generate()
                    

        elif "tekrarı" in voice: #Spotify tekrar ayarlarını yapar

            if " kapat" in voice:
                r=requests.put('https://api.spotify.com/v1/me/player/repeat?state=off',headers=spoti_header)
                if r.status_code==204:
                    print("tekrar kapatıldı")
                    speak("tekrar kapatıldı")
                elif r.status_code==404:
                    print("spotifyınız açık değil")
                    speak("spotifyınız açık değil")
                elif r.status_code==401:
                    print("token oluşturma ekranı açıldı")
                    speak("token oluşturma ekranı açıldı")
                    print("tokeninizi bana verirmisiniz")
                    speak("tokeninizi bana verirmisiniz")
                    token_generate()
                  


            elif "aç" in voice:
                r=requests.put('https://api.spotify.com/v1/me/player/repeat?state=context',headers=spoti_header)
                if r.status_code==204:
                    print("tekrar açıldı")
                    speak("tekrar açıldı")
                elif r.status_code==404:
                    print("spotifyınız açık değil")
                    speak("spotifyınız açık değil")
                elif r.status_code==401:
                    print("token oluşturma ekranı açıldı")
                    speak("token oluşturma ekranı açıldı")
                    print("tokeninizi bana verirmisiniz")
                    speak("tokeninizi bana verirmisiniz")
                    token_generate()
                  

        elif "şarkıyı tekrarla" in voice: #Spotify şarkıyı tekrarlar
            r=requests.put('https://api.spotify.com/v1/me/player/repeat?state=track',headers=spoti_header)
            if r.status_code==204:
                print("şarkı tekrarlanıyor")
                speak("şarkı tekrarlanıyor")
            elif r.status_code==404:
                print("spotifyınız açık değil")
                speak("spotifyınız açık değil")
            elif r.status_code==401:
                print("token oluşturma ekranı açıldı")
                speak("token oluşturma ekranı açıldı")
                print("tokeninizi bana verirmisiniz")
                speak("tokeninizi bana verirmisiniz")
                token_generate()





if ui.username=="":
    bos("değiştir")
else:
    halftime()
    print("{}. Ben yaren sana nasıl yardımcı olabilirim".format(ui.username))
    speak("{}. Ben yaren sana nasıl yardımcı olabilirim".format(ui.username))
    while 1:
        voice2=record2()
        if "yaren" in voice2:
            print("Buyur {}. nasıl yardımcı olabilirim?".format(ui.username))
            speak("Buyur {}. nasıl yardımcı olabilirim?".format(ui.username))
            while 1:
                time.sleep(0.5)
                voice = record2("listening....")
                time.sleep(0.1)
                print("Söyledigin kelime : "+voice)
                email(voice)
                newspaper(voice)
                Browser(voice)
                request(voice)
                game(voice)
                selamla(voice)
                bos(voice)
                wifi(voice)
                lock(voice)
                bluetooth(voice)
                soundvolume(voice)
                dosyaislemleri(voice)
                run(voice)
                yapılacaklar(voice)
                hesap(voice)
                musıc(voice)