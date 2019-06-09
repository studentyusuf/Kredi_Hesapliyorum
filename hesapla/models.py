from django.db import models


# Create your models here.

class Service:

    #Merkez Bankası tarafından belirlenen en düşük faiz oranı
    sabitFaizOranı = 1.00

    @staticmethod
    def foundService(service, typeOfProduct, values):
        bank = ""
        if service == "Türkiye İş Bankası":
            bank = IsBankasi(service, typeOfProduct, values)
        elif service == "Akbank":
            bank = Akbank(service, typeOfProduct, values)
        elif service == "Garanti":
            bank = Garanti(service, typeOfProduct, values)
        else:
            print("FATALERROR: Bilinmeyen servis !!!")
        return bank

    def __init__(self, service, typeOfProduct, values):
        self.faizOranı = self.faizHesapla(typeOfProduct, self.sabitFaizOranı)
        self.vade = self.taksitMiktarı(typeOfProduct)
        self.dokumCetveli = self.tabloOlustur(values)

    
    def taksitMiktarı(self, typeOfProduct):
        vade = 0
        if typeOfProduct == "ihtiyac":
            vade = 12, 24 
        elif typeOfProduct == "arac":
            vade = 36, 48
        elif typeOfProduct == "ev":
            vade = 48, 72
        else:
            vade = 72
        return vade
     
    def faizHesapla(self, typeOfProduct, faiz):
        faizOranı = 0
        if typeOfProduct == "ihtiyac":
            faizOranı = faiz + 0.08, faiz + 0.08
        elif typeOfProduct == "arac":
            faizOranı = faiz + 0.13, faiz + 0.13
        elif typeOfProduct == "ev":
            faizOranı = faiz + 0.25, faiz + 0.45
        else:
            faizOranı = faiz + 0.45
        return faizOranı

    def tabloOlustur(self, values):
        dokumCetveli = []
        krediDokumu = []
        krediMiktarlari = range(values[0], values[1], 500)

        for miktar in krediMiktarlari:
            for index in range(2):
                vade = self.vade[index]
                faiz = self.faizOranı[index]

                faizliTutar = miktar * faiz
                aylikTutar = faizliTutar / vade

                toplamFaizMiktari =  faizliTutar - miktar
                toplamOdenecekBorc = aylikTutar * vade
                
                #Format strings
                faiz = "%s" % str(format(faiz, "-.2f"))
                aylikTutar = "₺ %s" % str(format(aylikTutar, ",.2f"))
                toplamFaizMiktari = "₺ %s" % str(format(toplamFaizMiktari, ",.2f"))
                toplamOdenecekBorc = "₺ %s" % str(format(toplamOdenecekBorc, ",.2f"))

                krediDokumu.append((vade, faiz, aylikTutar, toplamFaizMiktari, toplamOdenecekBorc))

            miktar = "₺ %s" % str(format(miktar, ",.2f"))

            # (1500₺ için (12 ay, faiz, aylık tutar, faiz toplamı, toplam ödenecek tutar), (24 ay, faiz, aylık tutar, faiz toplamı, toplam ödenecek tutar))
            dokumCetveli.append(
                (miktar, krediDokumu)
            )
            #Hesaplanmış değerler, bir sonraki miktar için temizlenir.
            krediDokumu = []
        
        #Hesaplanan kredi dökümü geri döndürülür. 
        return dokumCetveli


class IsBankasi(Service):
    
    #Bankanın sabit faiz oranı
    sabitFaizOranı = 1.55

class Garanti(Service):

    #Bankanın sabit faiz oranı
    sabitFaizOranı = 1.85

class Akbank(Service):

    #Bankanın sabit faiz oranı
    sabitFaizOranı = 1.75