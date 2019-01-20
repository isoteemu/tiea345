#!/usr/bin/env python

import RPi.GPIO as GPIO
import time


class Demo2:
    """Demo 2 luokka.
    """

    PIN_LED = 16
    PIN_PAINIKE = 19
    PIN_PIR = 24

    PIN_JALAKNKULKIJA_VIHREÄ = 12
    PIN_AUTO_PUNAINEN = 16
    PIN_AUTO_KELTAINEN = 20
    PIN_AUTO_VIHREÄ = 21

    def __init__(self):
        GPIO.setmode(GPIO.BCM)


    """Tehtävä 1: Vilkuta lediä
    """
    def vilkuta(self):
        GPIO.setup(self.PIN_LED, GPIO.OUT)

        while(True):
            GPIO.output(self.PIN_LED, 1)
            time.sleep(0.5)
            GPIO.output(self.PIN_LED, 0)
            time.sleep(0.5)


    """Tehtävä 2 osa 1: Lue painiketta ja käynnistä ledi"""
    def painike(self):
        return self.kuuntele(self.PIN_PAINIKE)


    """Tehtävä 2 osa 2: Lue PIR painikkeen tilaa"""
    def pir(self):
        return self.kuuntele(self.PIN_PIR)

    def kuuntele(self, in_pin):
        GPIO.setup(self.PIN_LED, GPIO.OUT)
        GPIO.setup(in_pin, GPIO.IN)
        tila = GPIO.input(in_pin)
        while(True):
            if tila != GPIO.input(in_pin):
                tila = not tila
                print("Uusi painikkeen tila: %s" % tila)

            GPIO.output(self.PIN_LED, tila)
            time.sleep(0.1)

    def liikennevalot():
        GPIO.setup(self.PIN_JALANKULKIJA_VIHREÄ, GPIO.OUT)
        GPIO.setup(self.PIN_AUTO_PUNAINEN, GPIO.OUT)
        GPIO.setup(self.PIN_AUTO_KELTAINEN, GPIO.OUT)
        GPIO.setup(self.PIN_AUTO_VIHREÄ, GPIO.OUT)
        GPIO.setup(self.PIN_PAINIKE, GPIO.IN)

        GPIO.output(self.PIN_JALAKNKULKIJA_VIHREÄ, 0)
        GPIO.output(self.PIN_AUTO_PUNAINEN, 0)
        GPIO.output(self.PIN_AUTO_KELTAINE, 0)
        GPIO.output(self.PIN_AUTO_VIHREÄ, 1)

        while(true):

            # Kun valot ovat vihreät autoilijoille ja painiketta on painettu, 
            # sytytetään signaalivalo (keltainen), joka kertoo jalankulkijalle, 
            # että painallus on rekisteröity. Valon tulee palaa napin
            # painamisesta siihen asti, kunnes jalankulkijoille vaihtuu vihreä valo.
            if GPIO.input(self.PIN_PAINIKE):

                GPIO.output(PIN_AUTO_KELTAINEN, 1)

                if GPIO.input(self.PIN_PIR):
                    # Kun nappia painetaan, tarkistetaan, näkyykö liikettä.
                    # Jos ei näy liikettä, ei ole autoja, joten valot voi vaihtaa
                    # jalankulkijoille suotuisiksi. Jos liikettä, odota hetki, jos
                    # jono loppuisi. 
                    time.sleep(2)

                GPIO.output(PIN_AUTO_KELTAINEN, 0)
                GPIO.output(PIN_AUTO_PUNAINEN, 1)
                GPIO.output(PIN_AUTO_VIHREÄ, 0)

                time.sleep(3)

                GPIO.output(PIN_AUTO_KELTAINEN, 0)
                GPIO.output(PIN_AUTO_PUNAINEN, 0)
                GPIO.output(PIN_AUTO_VIHREÄ, 1)

            time.sleep(0.1)
            


    def __del__(self):
        GPIO.output(self.PIN_LED, 0)
        GPIO.cleanup()


if __name__ == "__main__":

    toiminnot = ["vilkuta", "painike", "pir", "liikennevalot"]

    import argparse
    cmdline = argparse.ArgumentParser(description="TIEA345 Demo 2")
    cmdline.add_argument("toiminto", help="Suoritettava toiminto.",
                         choices=toiminnot)

    args = cmdline.parse_args()

    if args.toiminto in toiminnot:
        demo = Demo2()
        getattr(demo, args.toiminto)()
    else:
        cmdline.error("Ei toimintoa")
