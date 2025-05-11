import pygame
import math
import sys
import random
import time
import os

pygame.init()

# Ekran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Futbol Oyunu")
clock = pygame.time.Clock()

# Renkler
WHITE = (230, 230, 230)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 100)

# Görseller
oyuncu_standing = pygame.image.load('Resimler/run1.png')

top_resmi = pygame.image.load("Resimler/futboltopu.png").convert_alpha()
top_resmi = pygame.transform.scale(top_resmi, (50, 50))

arkaplan_resmi = pygame.image.load("Resimler/tribune6 (1).png").convert()
arkaplan_resmi = pygame.transform.scale(arkaplan_resmi, (WIDTH, HEIGHT))

kale_resmi = pygame.image.load("Resimler/kale.png").convert_alpha()

# Şut animasyon görselleri
sut_animasyonlari = [
    pygame.image.load("Resimler/run2.png"),
    pygame.image.load("Resimler/run3.png"),
    pygame.image.load("Resimler/run4.png")
]

# Karakter
eni, boyu = 64, 64
vel = 5

animasyon_zamanlayici = 0
frame_gecikmesi = 7

# Top
top_start = [150, HEIGHT - 50]
top_pos = list(top_start)
top_yaricap = 25
top_aci = 45
guc = 20
top_hareketli_mi = False
vektor = [0, 0]
yer_cekimi = 0.5
skor = 0
total_atislar = 0
sekme = 0
sekme_limiti = 3
sekmedeki_yukseklik_azalmasi = 0.7
top_donus_acisi = 0

# Şut animasyonu kontrol
sut_animation = False
sut_frame = 0

# Fontlar
font = pygame.font.SysFont(None, 28)
baslik_font = pygame.font.SysFont(None, 64)
skor_font = pygame.font.SysFont(None, 48)

# Menü
menu = True
oyun_bitti = False
start_time = None
zaman_siniri = 5
gecen_sure = 0

# Random kale yeri ve boyutu
def random_hoop():
    hoop_y = random.randint(100, HEIGHT - 200)
    hoop_h = random.randint(80, 140)
    return pygame.Rect(WIDTH - 120, hoop_y, 100, hoop_h)

def yuksek_skor_yukle():
    if os.path.exists("highest_score.txt"):
        with open("highest_score.txt", "r") as f:
            return int(f.read())
    return 0

def yuksek_skor_kaydet(skor):
    with open("highest_score.txt", "w") as f:
        f.write(str(skor))

yuksek_skor = yuksek_skor_yukle()
hoop = random_hoop()

def gidis_yonu_cizimi(pos, aci, guc):
    noktalar = []
    radyan = math.radians(aci)
    x_ekseni = math.cos(radyan) * guc * 0.3
    y_ekseni = -math.sin(radyan) * guc * 0.3
    for t in range(50):
        dx = pos[0] + x_ekseni * t * 0.2
        dy = pos[1] + y_ekseni * t * 0.2 + 0.5 * yer_cekimi * (t * 0.2) ** 2
        if dy > HEIGHT:
            break
        noktalar.append((int(dx), int(dy)))
    if len(noktalar) > 1:
        pygame.draw.lines(screen, WHITE, False, noktalar, 2)

        if len(noktalar) >= 2:
            p1 = noktalar[-2]
            p2 = noktalar[-1]

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            aci = math.atan2(dy, dx)

            ok_uzunluk = 10
            ok_aci = math.radians(30)

            sol = (
                p2[0] - ok_uzunluk * math.cos(aci - ok_aci), p2[1] - ok_uzunluk * math.sin(aci - ok_aci))
            sag = (
                p2[0] - ok_uzunluk * math.cos(aci + ok_aci), p2[1] - ok_uzunluk * math.sin(aci + ok_aci))

            pygame.draw.line(screen, WHITE, p1, p2, 2)
            pygame.draw.line(screen, WHITE, p2, sol, 2)
            pygame.draw.line(screen, WHITE, p2, sag, 2)

def reset_top():
    global top_pos, vektor, top_hareketli_mi, sekme, top_donus_acisi
    top_pos = list(top_start)
    vektor = [0, 0]
    sekme = 0
    top_hareketli_mi = False
    top_donus_acisi = 0

def giris_menusu():
    screen.blit(arkaplan_resmi, (0, 0))
    baslik = baslik_font.render("Futbol Oyunu", True, WHITE)
    giris_text = font.render("ENTER - Başlat", True, GREEN)
    cikis_text = font.render("ESC - Çıkış", True, RED)
    screen.blit(baslik, (WIDTH // 2 - baslik.get_width() // 2, 270))
    screen.blit(giris_text, (WIDTH // 2 - giris_text.get_width() // 2, 350))
    screen.blit(cikis_text, (WIDTH // 2 - cikis_text.get_width() // 2, 375))
    pygame.display.flip()

def oyun_bitti_menusu():
    screen.blit(arkaplan_resmi, (0, 0))
    oyun_bitti_text = baslik_font.render("Oyun Bitti!", True, RED)
    skor_text = skor_font.render(f"Skor: {skor}", True, BLACK)
    yuksek_skor_text = skor_font.render(f"En Yüksek Skor: {yuksek_skor}", True, GREEN)
    yeniden_baslat_text = font.render("ENTER - Yeniden Başlat", True, WHITE)
    cikis_text = font.render("ESC - Çıkış", True, WHITE)

    screen.blit(oyun_bitti_text, (WIDTH // 2 - oyun_bitti_text.get_width() // 2, 180))
    screen.blit(skor_text, (WIDTH // 2 - skor_text.get_width() // 2, 255))
    screen.blit(yuksek_skor_text, (WIDTH // 2 - yuksek_skor_text.get_width() // 2, 290))
    screen.blit(yeniden_baslat_text, (WIDTH // 2 - yeniden_baslat_text.get_width() // 2, 350))
    screen.blit(cikis_text, (WIDTH // 2 - cikis_text.get_width() // 2, 380))
    pygame.display.flip()

# Ana Oyun Döngüsü
while True:
    if menu:
        giris_menusu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            menu = False
            start_time = time.time()
            score = 0
            total_atislar = 0
            gecen_sure = 0
            reset_top()
            hoop = random_hoop()
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        continue

    if oyun_bitti:
        oyun_bitti_menusu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            menu = True
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        continue

    clock.tick(60)
    screen.blit(arkaplan_resmi, (0, 0))
    gecen_sure = int(time.time() - start_time)

    if gecen_sure >= zaman_siniri:
        oyun_bitti = True
        if skor > yuksek_skor:
            yuksek_skor = skor
            yuksek_skor_kaydet(yuksek_skor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if not top_hareketli_mi and not sut_animation:
        if keys[pygame.K_UP]:
            top_aci = min(80, top_aci + 1)
        if keys[pygame.K_DOWN]:
            top_aci = max(10, top_aci - 1)
        if keys[pygame.K_RIGHT]:
            guc = min(50, guc + 1)
        if keys[pygame.K_LEFT]:
            guc = max(10, guc - 1)
        if keys[pygame.K_SPACE]:
            sut_animation = True
            sut_frame = 0
            radyan = math.radians(top_aci)
            vektor = [math.cos(radyan) * guc * 0.5, -math.sin(radyan) * guc * 0.5]
            total_atislar += 1
        if keys[pygame.K_ESCAPE]:
            menu = True
            continue

    if sut_animation:
        if sut_frame < len(sut_animasyonlari):
            if animasyon_zamanlayici % frame_gecikmesi == 0:
                screen.blit(sut_animasyonlari[sut_frame], (top_pos[0] - 150, HEIGHT - 250))
                sut_frame += 1
            else:
                screen.blit(sut_animasyonlari[sut_frame - 1], (top_pos[0] - 150, HEIGHT - 250))
            animasyon_zamanlayici += 1
        else:
            sut_animation = False
            sut_frame = 0
            animasyon_zamanlayici = 0
            top_hareketli_mi = True
    else:
        screen.blit(oyuncu_standing, (WIDTH - 780, HEIGHT - 250))

    if top_hareketli_mi:
        vektor[1] += yer_cekimi
        top_pos[0] += vektor[0]
        top_pos[1] += vektor[1]
        top_donus_acisi = (top_donus_acisi + 10) % 360

        #Gol olması
        top_rect = pygame.Rect(top_pos[0] - top_yaricap-10,top_pos[1] - top_yaricap-10, top_yaricap, top_yaricap * 2)
        if top_rect.colliderect(hoop):
            skor += 1
            hoop = random_hoop()
            reset_top()
        elif top_pos[1] + top_yaricap >= HEIGHT:
            if sekme < sekme_limiti:
                top_pos[1] = HEIGHT - top_yaricap
                vektor[1] = -vektor[1] * sekmedeki_yukseklik_azalmasi
                vektor[0] *= 0.8
                sekme += 1
            else:
                reset_top()
        elif top_pos[0] > WIDTH:
            reset_top()

    # Topun döndürerek çizimi
    dondurulmus_top = pygame.transform.rotate(top_resmi, -top_donus_acisi)
    dondurulmus_rect = dondurulmus_top.get_rect(center=(int(top_pos[0]), int(top_pos[1])))
    screen.blit(dondurulmus_top, dondurulmus_rect.topleft)

    screen.blit(pygame.transform.scale(kale_resmi, (hoop.width, hoop.height)), (hoop.x, hoop.y))

    if not top_hareketli_mi and not sut_animation:
        gidis_yonu_cizimi(top_pos, top_aci, guc)

    isabet_orani = round((skor / total_atislar) * 100, 1) if total_atislar > 0 else 0
    screen.blit(font.render(f"Açı: {top_aci}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Güç: {guc}", True, WHITE), (10, 30))
    screen.blit(font.render(f"Skor: {skor}", True, WHITE), (10, 50))
    screen.blit(font.render(f"Atış: {total_atislar}", True, WHITE), (10, 70))
    screen.blit(font.render(f"İsabet Oranı: %{isabet_orani}", True, GREEN), (10, 105))
    screen.blit(font.render(f"Süre: {zaman_siniri - gecen_sure}s", True, RED), (10, 125))
    screen.blit(skor_font.render(f"En Yüksek Skor: {yuksek_skor}", True, WHITE), (WIDTH - 330, 15))

    pygame.display.flip()
