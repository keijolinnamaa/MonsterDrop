# Move with left and right arrow keys
# Shoot with space
# Catch coins
# Dont hit monsters with robo

# Pelissä liikut vasemmalle ja oikealle nuolinäppäimillä.
# Välilyönnillä ammut monstereita.
# Nappaa robolla kiinni kolikoita, joista saa isot pisteet.
# Älä osu robolla monsteriin.
# Aloittaaksesi paina hiirellä pelaa nappia.

import pygame
from random import randint
from pygame.sprite import Sprite

class MonsterDrop:

    def __init__ (self):
        pygame.init()
        self.naytto =pygame.display.set_mode((1200,800))
        self.naytto_rect = self.naytto.get_rect()
        pygame.display.set_caption("Monster Drop")
        self.tausta = (0,128,255)
        self.pelaa = False
        self.pisteet = 0
        self.ennatys = 0
        self.fontti = pygame.font.SysFont("Arial", 35)
        self.tekstin_vari = (0, 255, 0)
        self.teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, self.tekstin_vari)
        self.ennatys_teksti = self.fontti.render(f"Ennätys: {self.ennatys}", True, self.tekstin_vari)
        self.robo = Robo(self)
        
        self.ammukset = pygame.sprite.Group()
        self.monsterit = pygame.sprite.Group()
        self.kolikot = pygame.sprite.Group()

        self.monsterimaara = 3

        self.muodosta_monsterit()        
        self.muodosta_kolikot()

        self.peli_nappi = Nappi(self, "Pelaa")
            

    def run(self):
        while True:
            
            self.tarkista()
            if self.pelaa:
                self.robo.paivita()
                self.ammukset.update()
                monsteri_osuma = pygame.sprite.groupcollide(self.ammukset, self.monsterit, True, True)            
                if monsteri_osuma:
                    self.pisteet += 200            
                    self.teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, self.tekstin_vari)
                    if self.pisteet >= self.ennatys:
                        self.ennatys = self.pisteet
                        self.ennatys_teksti = self.fontti.render(f"Ennätys: {self.ennatys}", True, self.tekstin_vari)
                for ammus in self.ammukset.copy():
                    if ammus.rect.bottom <= 0:
                        self.ammukset.remove(ammus)

                self.monsterit.update()
                monsteri_robo_osuma = pygame.sprite.spritecollideany(self.robo, self.monsterit)
                if monsteri_robo_osuma:
                    self.pelaa = False
                    pygame.mouse.set_visible(True)
                if len(self.monsterit) == 0:
                    self.monsterimaara += 3
                    self.muodosta_monsterit()
                    self.muodosta_kolikot()
                for monsteri in self.monsterit.copy():                            
                    if monsteri.rect.top >= 800:
                        self.monsterit.remove(monsteri)

                self.kolikot.update() 
                kolikko_robo_osuma = pygame.sprite.spritecollideany(self.robo, self.kolikot)                           
                for kolikko in self.kolikot:                    
                    if kolikko_robo_osuma:
                        self.kolikot.remove(kolikko)
                        self.pisteet += 300
                        self.teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, self.tekstin_vari)
                        if self.pisteet >= self.ennatys:
                            self.ennatys = self.pisteet
                            self.ennatys_teksti = self.fontti.render(f"Ennätys: {self.pisteet}", True, self.tekstin_vari)                
                    elif kolikko.rect.top >= 800:
                        self.kolikot.remove(kolikko)
                    
            self.paivita()

    def tarkista(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            elif tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = True
                elif tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = True
                elif tapahtuma.key == pygame.K_SPACE:
                    self.ammutaan()

            elif tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_RIGHT:
                    self.robo.oikealle = False
                elif tapahtuma.key == pygame.K_LEFT:
                    self.robo.vasemmalle = False

            elif tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                hiiren_paikka = pygame.mouse.get_pos()
                painettu = self.peli_nappi.rect.collidepoint(hiiren_paikka)
                if painettu and not self.pelaa:
                    self.pisteet = 0
                    self.teksti = self.fontti.render(f"Pisteet: {self.pisteet}", True, self.tekstin_vari)
                    self.pelaa = True
                    self.ammukset.empty()
                    self.monsterit.empty()
                    self.kolikot.empty()
                    self.muodosta_monsterit()        
                    self.muodosta_kolikot()
                    self.robo.rect.midbottom = self.naytto_rect.midbottom
                    pygame.mouse.set_visible(False)


    def ammutaan(self):
        if len(self.ammukset) < 3:
            uusi_ammus = Ammukset(self)
            self.ammukset.add(uusi_ammus)

    def muodosta_monsterit(self):           
        for _ in range(self.monsterimaara):
            monsteri = Monsterit(self)
            monsteri.x = monsteri.rect.x
            monsteri.y = monsteri.rect.y
            self.monsterit.add(monsteri)

    def muodosta_kolikot(self):        
        for _ in range(1):
            kolikko = Kolikot(self)
            kolikko.x = kolikko.rect.x
            kolikko.y = kolikko.rect.y
            self.kolikot.add(kolikko)
                    
    def paivita(self):   
            self.naytto.fill(self.tausta)
            self.robo.blitme()
            self.naytto.blit(self.teksti, (900, 30))
            self.naytto.blit(self.ennatys_teksti, (30, 30))
            for ammus in self.ammukset.sprites():
                ammus.piirra_ammus()
            self.monsterit.draw(self.naytto)
            self.kolikot.draw(self.naytto)
            if not self.pelaa:
                self.peli_nappi.piirra_nappi()
            pygame.display.flip()


class Robo:
    def __init__(self, mdpeli):
        self.naytto = mdpeli.naytto
        self.naytto_rect = mdpeli.naytto.get_rect()
        self.kuva = pygame.image.load("pictures/robo.png")
        self.rect = self.kuva.get_rect()
        self.rect.midbottom = self.naytto_rect.midbottom
        
        self.oikealle = False
        self.vasemmalle = False

    def paivita(self):
        if self.oikealle and self.rect.right < self.naytto_rect.right:
            self.rect.x += 1
        if self.vasemmalle and self.rect.left > 0:
            self.rect.x -= 1

    def blitme(self):
        self.naytto.blit(self.kuva, self.rect)


class Ammukset(Sprite):
    def __init__(self, mdpeli):
        super().__init__()
        self.naytto = mdpeli.naytto
        self.rect = pygame.Rect(0,0,4,15)
        self.rect.midtop = mdpeli.robo.rect.midtop

    def update(self):
        self.rect.y -= 1

    def piirra_ammus(self):
        pygame.draw.rect(self.naytto, (255,0,127), self.rect)


class Monsterit(Sprite):
    def __init__(self, mdpeli):
        super().__init__()
        self.naytto = mdpeli.naytto
        self.naytto_rect = mdpeli.naytto.get_rect()
        self.image = pygame.image.load("pictures/hirvio.png")
        self.rect = self.image.get_rect()   

        self.rect.x = randint(0, self.naytto_rect.right - self.rect.width)
        self.rect.y = randint(-6500, -1500)

    def update(self):
        self.rect.y += 1
    


class Kolikot(Sprite):
    def __init__(self, mdpeli):
        super().__init__()
        self.naytto = mdpeli.naytto
        self.naytto_rect = mdpeli.naytto.get_rect()
        self.image = pygame.image.load("pictures/kolikko.png")
        self.rect = self.image.get_rect()             

        self.rect.x = randint(0, self.naytto_rect.right - self.rect.width)
        self.rect.y = randint(-6500, -1500)

    def update(self):            
        self.rect.y += 1

class Nappi:
    def __init__(self, mdpeli, txt):
        self.naytto = mdpeli.naytto
        self.naytto_rect = self.naytto.get_rect()
        self.leveys, self.korkeus = 200, 50
        self.nappi_vari = (0,255,0)
        self.txt_vari = (0,128,255)
        self.font = pygame.font.SysFont("Arial", 35)
        self.rect = pygame.Rect(0,0, self.leveys, self.korkeus)
        self.rect.center = self.naytto_rect.center

        self.valmista_txt(txt)

    def valmista_txt(self, txt):
        self.txt_kuva = self.font.render(txt, True, self.txt_vari, self.nappi_vari)
        self.txt_kuva_rect =self.txt_kuva.get_rect()
        self.txt_kuva_rect.center = self.rect.center

    def piirra_nappi(self):
        self.naytto.fill(self.nappi_vari, self.rect)
        self.naytto.blit(self.txt_kuva, self.txt_kuva_rect)

md = MonsterDrop()
md.run()