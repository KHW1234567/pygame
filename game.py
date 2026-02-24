import pygame
import random
import os

# =====================================================
# TUNING / BALANCE (수치 조절)
# =====================================================
# - 화면/프레임
BASE_WIDTH = 700
BASE_HEIGHT = 900
FPS = 60

# - UI/레이아웃(비율/위치)
TITLE_NAME_Y_RATIO = 0.22
TITLE_STARTBTN_Y_RATIO = 0.85 

# 플로팅 텍스트 및 적 체력바 관련 수치
FLOAT_TEXT_LIFETIME_MS = 800
FLOAT_TEXT_RISE_SPEED = 0.05
MINI_HP_BAR_W = 30
MINI_HP_BAR_H = 6
BOSS_HP_BAR_W = 200
BOSS_HP_BAR_H = 15
ICON_SIZE = 32  

# - 스케일(이미지 크기)
SCALE_ALVEOLUS = 0.35
SCALE_BULLET = 0.3

SCALE_DUST = 0.3
SCALE_FOOD = 0.5
SCALE_CIGARETTE = 0.7
SCALE_BOSS = 1.2

SCALE_BROCCOLI = 0.3
SCALE_WATER = 0.3

NEBULIZER_SCALE = 0.15
# [수정됨: 1. 네블라이저 팝업(이펙트) 이미지 크기 조절 변수 추가]
NEBULIZER_EFFECT_SCALE = 0.5

# - 이동/속도
PLAYER_BASE_SPEED = 3
BULLET_SPEED = 8

DUST_SPEED = 2.0
FOOD_SPEED = 1.5
CIGARETTE_SPEED = 1.0
BOSS_SPEED = 1.2

BROCCOLI_SPEED = 2.5
WATER_SPEED = 2.5
NEBULIZER_SPEED = 2.0

# - 스폰(초 단위)
DUST_SPAWN_INTERVAL = 0.15

FOOD_SPAWN_START = 10
FOOD_SPAWN_INTERVAL = 1

CIGARETTE_SPAWN_START = 15
CIGARETTE_SPAWN_INTERVAL = 2

BROCCOLI_SPAWN_INTERVAL = 2
WATER_SPAWN_INTERVAL = 5

NEBULIZER_SPAWN_TIMES = [18, 33, 48]

# - HP/점수/조건
SPO2_START = 100
SPO2_DECAY_PER_SEC = 3.0
SPO2_WIN_THRESHOLD = 90
TIME_LIMIT = 60

DUST_HP = 1
FOOD_HP = 3
CIGARETTE_HP = 5
BOSS_HP = 70

SCORE_DUST = 1
SCORE_FOOD = 3
SCORE_CIGARETTE = 5
SCORE_BOSS = 10

SPO2_GAIN_DUST = 1
SPO2_GAIN_FOOD = 3
SPO2_GAIN_CIGARETTE = 5
SPO2_GAIN_BOSS = 10

BROCCOLI_MAX_STACK = 30
ROW_CAPACITY = 10
BROCCOLI_INSERT_OFFSET_RATIO = 0.33
WATER_SPEED_GAIN = 1

# - 보스(초 단위)
BOSS_FIRST_DELAY = 20
BOSS_INTERVAL = 15
BOSS_MAX_SPAWN = 3
BOSS_WARNING_SEC = 3

# - 네블라이저(필살기)
NEBULIZER_ALL_ENEMY_HP_DEC = 5
NEBULIZER_EFFECT_DURATION_MS = 1000

POPUP_LIFETIME_MS = 1000
POPUP_RISE_PER_MS = 0.06
POPUP_ALPHA_DEC_PER_MS = 0.28

# =====================================================
# PATH
# =====================================================
IMG_PATH = "D:\\MHH\\python\\MedicalDA05_pygame-ver2-\\image\\"
SOUND_PATH = "D:\\MHH\\python\\MedicalDA05_pygame-ver2-\\sound\\"
FONT_PATH = "D:\\MHH\\python\\MedicalDA05_pygame-ver2-\\font\\"

# =====================================================
# INIT / DISPLAY
# =====================================================
pygame.init()
pygame.mixer.init()

background = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

info = pygame.display.Info()
monitor_w = info.current_w
monitor_h = info.current_h

# - 화면 스케일(모니터 대응)
scale_ratio = min(monitor_w / BASE_WIDTH, monitor_h / BASE_HEIGHT) * 0.8
display_w = int(BASE_WIDTH * scale_ratio)
display_h = int(BASE_HEIGHT * scale_ratio)

screen = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("강철폐포부대")
clock = pygame.time.Clock()

# =====================================================
# STATE (화면 전환)
# =====================================================
STATE_TITLE = 0
STATE_INTRO = 1
STATE_READY = 2
STATE_GAME = 3
game_state = STATE_TITLE

# =====================================================
# LOAD / UI (시작/결과 화면)
# =====================================================
# - 시작 화면
image_game_start_bg = pygame.image.load(IMG_PATH + "game_start.png")
image_game_start_bg = pygame.transform.scale(image_game_start_bg, (BASE_WIDTH, BASE_HEIGHT))

image_game_name = pygame.image.load(IMG_PATH + "game_name.png")
image_game_name = pygame.transform.rotozoom(image_game_name, 0, 0.85)

image_start_button = pygame.image.load(IMG_PATH + "start_button.png")
image_start_button = pygame.transform.rotozoom(image_start_button, 0, 0.35)

start_button_rect_img = image_start_button.get_rect(
    center=(BASE_WIDTH // 2, int(BASE_HEIGHT * TITLE_STARTBTN_Y_RATIO))
)

game_name_rect = image_game_name.get_rect(
    center=(BASE_WIDTH // 2, int(BASE_HEIGHT * TITLE_NAME_Y_RATIO)+50)
)

image_ready_start_button = pygame.image.load(IMG_PATH + "버튼_START.png")
image_ready_start_button = pygame.transform.rotozoom(image_ready_start_button, 0, 0.8)
ready_start_rect_img = image_ready_start_button.get_rect(
    center=(BASE_WIDTH / 2, BASE_HEIGHT / 2 + 300) 
)

# - 결과 화면
image_success_bg = pygame.image.load(IMG_PATH + "success.png")
image_success_bg = pygame.transform.scale(image_success_bg, (BASE_WIDTH, BASE_HEIGHT))

image_fail_bg = pygame.image.load(IMG_PATH + "fail.png")
image_fail_bg = pygame.transform.scale(image_fail_bg, (BASE_WIDTH, BASE_HEIGHT))

try:
    image_gameover_title = pygame.image.load(IMG_PATH + "button_fail.png")
    image_gameover_title = pygame.transform.rotozoom(image_gameover_title, 0, 0.8)
except:
    image_gameover_title = None

try:
    image_success_title = pygame.image.load(IMG_PATH + "button_success.png") 
    image_success_title = pygame.transform.rotozoom(image_success_title, 0, 0.8)
except:
    image_success_title = None

image_retry_button = pygame.image.load(IMG_PATH + "버튼_RETRY.png")
image_retry_button = pygame.transform.rotozoom(image_retry_button, 0, 0.85) 
retry_rect_img = image_retry_button.get_rect()

image_quit_button = pygame.image.load(IMG_PATH + "버튼_QUIT.png")
image_quit_button = pygame.transform.rotozoom(image_quit_button, 0, 0.85)
quit_rect_img = image_quit_button.get_rect()

try:
    image_boss_warning = pygame.image.load(IMG_PATH + "warn_boss.png")
    image_boss_warning = pygame.transform.rotozoom(image_boss_warning, 0, 0.7) 
except:
    image_boss_warning = None

# [수정됨: 2. 스케일 변수(NEBULIZER_EFFECT_SCALE)를 적용하여 이미지 로드]
try:
    image_nebulizer_effect = pygame.image.load(IMG_PATH + "effect_네불라이저.png")
    image_nebulizer_effect = pygame.transform.rotozoom(image_nebulizer_effect, 0, NEBULIZER_EFFECT_SCALE) 
except:
    image_nebulizer_effect = None

# =====================================================
# LOAD / GAME (배경 + 오브젝트 + UI 아이콘)
# =====================================================
# - 게임 배경
image_bg = pygame.image.load(IMG_PATH + "background_highR.png")
image_bg = pygame.transform.scale(image_bg, (BASE_WIDTH, BASE_HEIGHT))

image_icon_star = pygame.image.load(IMG_PATH + "star.png")
image_icon_clock = pygame.image.load(IMG_PATH + "time.png")
image_icon_spo2 = pygame.image.load(IMG_PATH + "o2.png")

image_icon_star = pygame.transform.scale(image_icon_star, (ICON_SIZE, ICON_SIZE))
image_icon_clock = pygame.transform.scale(image_icon_clock, (ICON_SIZE, ICON_SIZE))
image_icon_spo2 = pygame.transform.scale(image_icon_spo2, (ICON_SIZE, ICON_SIZE))

# 폐포(플레이어), 총알
image_alveolus = pygame.image.load(IMG_PATH + "alveolus.png")
image_bullet = pygame.image.load(IMG_PATH + "bullet.png")

# 적군
image_dust = pygame.image.load(IMG_PATH + "dust.png")
image_food = pygame.image.load(IMG_PATH + "food.png")
image_cigarette = pygame.image.load(IMG_PATH + "cigarette.png")

image_boss_list = [
    pygame.image.load(IMG_PATH + "boss1.png"),
    pygame.image.load(IMG_PATH + "boss2.png"),
    pygame.image.load(IMG_PATH + "boss3.png")
]

# 아이템
image_broccoli = pygame.image.load(IMG_PATH + "broccoli.png")
image_water = pygame.image.load(IMG_PATH + "water.png")

# 필살기
image_nebulizer = pygame.image.load(IMG_PATH + "nebulizer.png")

# =====================================================
# SCALE (오브젝트 크기 조절)
# =====================================================
image_alveolus = pygame.transform.rotozoom(image_alveolus, 0, SCALE_ALVEOLUS)
image_bullet = pygame.transform.rotozoom(image_bullet, 0, SCALE_BULLET)

image_dust = pygame.transform.rotozoom(image_dust, 0, SCALE_DUST)
image_food = pygame.transform.rotozoom(image_food, 0, SCALE_FOOD)
image_cigarette = pygame.transform.rotozoom(image_cigarette, 0, SCALE_CIGARETTE)
for i in range(len(image_boss_list)):
    image_boss_list[i] = pygame.transform.rotozoom(image_boss_list[i], 0, SCALE_BOSS)

image_broccoli = pygame.transform.rotozoom(image_broccoli, 0, SCALE_BROCCOLI)
image_water = pygame.transform.rotozoom(image_water, 0, SCALE_WATER)

image_nebulizer = pygame.transform.rotozoom(image_nebulizer, 0, NEBULIZER_SCALE)

RIGHT_ZONE_W = BASE_WIDTH // 2
MAX_NEB_W = RIGHT_ZONE_W - 20
neb_w, neb_h = image_nebulizer.get_rect().size
if neb_w > MAX_NEB_W:
    extra_scale = MAX_NEB_W / neb_w
    image_nebulizer = pygame.transform.rotozoom(image_nebulizer, 0, extra_scale)

# =====================================================
# SIZE CACHE (충돌/배치 계산용)
# =====================================================
size_alveolus_width, size_alveolus_height = image_alveolus.get_rect().size
size_bullet_width, size_bullet_height = image_bullet.get_rect().size
size_dust_width, size_dust_height = image_dust.get_rect().size
size_food_width, size_food_height = image_food.get_rect().size
size_cigarette_width, size_cigarette_height = image_cigarette.get_rect().size
size_boss_width, size_boss_height = image_boss_list[0].get_rect().size
size_broccoli_width, size_broccoli_height = image_broccoli.get_rect().size
size_water_width, size_water_height = image_water.get_rect().size
size_nebulizer_width, size_nebulizer_height = image_nebulizer.get_rect().size

# =====================================================
# LOAD / INTRO (story1~7)
# =====================================================
intro_images = []
for i in range(1, 8):
    img = pygame.image.load(IMG_PATH + f"story{i}.png")
    img = pygame.transform.scale(img, (BASE_WIDTH, BASE_HEIGHT))
    intro_images.append(img)

# =====================================================
# AUDIO (BGM/SFX)
# =====================================================
music_intro_file = SOUND_PATH + "배경음1.mp3"
music_game_file = SOUND_PATH + "배경음2.mp3"

sfx_item = pygame.mixer.Sound(SOUND_PATH + "아이템획득.mp3")
sfx_start = pygame.mixer.Sound(SOUND_PATH + "게임시작.mp3")
sfx_fail = pygame.mixer.Sound(SOUND_PATH + "게임실패2.mp3")
sfx_success = pygame.mixer.Sound(SOUND_PATH + "게임성공2.mp3")
sfx_shoot = pygame.mixer.Sound(SOUND_PATH + "발사소리.mp3")
sfx_button = pygame.mixer.Sound(SOUND_PATH + "버튼클릭음.mp3")
sfx_boss = pygame.mixer.Sound(SOUND_PATH + "경고음.mp3")
sfx_nebulizer = pygame.mixer.Sound(SOUND_PATH + "네볼라이저효과음.mp3")

try:
    sfx_player_die = pygame.mixer.Sound(SOUND_PATH + "sound_hit.mp3")
except:
    sfx_player_die = None 

sfx_shoot.set_volume(0.5)

pygame.mixer.music.load(music_intro_file)
pygame.mixer.music.play(-1)

# =====================================================
# FONT
# =====================================================
my_custom_font_file = "Bazzi.ttf" 
font_full_path = os.path.join(FONT_PATH, my_custom_font_file)

try:
    font_small = pygame.font.Font(font_full_path, 28)
    font_big = pygame.font.Font(font_full_path, 50)
    font_ui = pygame.font.Font(font_full_path, 34)
except:
    print("커스텀 폰트를 찾을 수 없습니다. 기본 폰트로 실행합니다.")
    font_small = pygame.font.SysFont("arial", 28, bold=True)
    font_big = pygame.font.SysFont("arial", 50, bold=True)
    font_ui = pygame.font.SysFont("arial", 34, bold=True)

font_title = pygame.font.SysFont("impact", 90, bold=True) 

# =====================================================
# UTIL 
# =====================================================
def get_non_overlap_x(existing_list, width, start_x=0, end_x=None, min_gap=10):
    if end_x is None:
        end_x = BASE_WIDTH // 2 - width  
    
    if start_x >= end_x:
        end_x = start_x + 1
        
    attempts = 0
    while attempts < 100:
        x = random.randrange(start_x, end_x)
        overlap = any(abs(x - obj[0]) < width + min_gap for obj in existing_list)
        if not overlap:
            return x
        attempts += 1
    return random.randrange(start_x, end_x)

def draw_text_with_outline(surface, text, font, text_color, outline_color, x, y):
    for dx, dy in [(-2,-2), (-2,2), (2,-2), (2,2), (0,-2), (-2,0), (2,0), (0,2)]:
        outline = font.render(text, True, outline_color)
        surface.blit(outline, (x + dx, y + dy))
    label = font.render(text, True, text_color)
    surface.blit(label, (x, y))

def draw_capsule_bar(surface, x, y, w, h, ratio, color, bg_color=(40, 40, 40)):
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=h//2)
    fill_w = int(w * ratio)
    if fill_w > 0:
        pygame.draw.rect(surface, color, (x, y, fill_w, h), border_radius=h//2)
    pygame.draw.rect(surface, (0, 0, 0), (x, y, w, h), width=2, border_radius=h//2)

def draw_mini_hp_bar(surface, x, y, current_hp, max_hp, is_boss=False):
    if current_hp <= 0: return
    ratio = current_hp / max_hp
    bar_w = BOSS_HP_BAR_W if is_boss else MINI_HP_BAR_W
    bar_h = BOSS_HP_BAR_H if is_boss else MINI_HP_BAR_H

    pygame.draw.rect(surface, (80, 0, 0), (x, y, bar_w, bar_h))
    pygame.draw.rect(surface, (255, 50, 50), (x, y, int(bar_w * ratio), bar_h))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_w, bar_h), width=1)


# =====================================================
# GAME RESET
# =====================================================
def reset_game():
    global players, bullets, to_x, move_speed, SpO2

    global dusts, cigarettes, foods
    global boss_hp, boss_alive, x_pos_boss, y_pos_boss, boss_warning, boss_warning_start
    global last_boss_spawn, remaining_boss_images, boss_spawn_count, current_boss_image

    global broccolis, waters
    global floating_texts

    global nebulizers, nebulizer_spawned_times
    global nebulizer_effect, nebulizer_effect_start, damage_popups

    global game_over, success, point
    global start_ticks, seconds
    global last_spawn_second, last_spawn_food, last_spawn_cigarette
    global last_spawn_broccoli, last_spawn_water
    global end_sound_played

    players = [[BASE_WIDTH / 2 - size_alveolus_width / 2, BASE_HEIGHT - size_alveolus_height - 20]]
    to_x = 0
    move_speed = PLAYER_BASE_SPEED
    SpO2 = SPO2_START

    bullets = []
    dusts = []
    foods = []
    cigarettes = []
    broccolis = []
    waters = []
    floating_texts = []

    nebulizers = []
    nebulizer_spawned_times = set()
    nebulizer_effect = False
    nebulizer_effect_start = 0
    damage_popups = []

    boss_hp = BOSS_HP
    boss_alive = False
    x_pos_boss = 0
    y_pos_boss = 0
    boss_warning = False
    boss_warning_start = 0
    last_boss_spawn = 0
    remaining_boss_images = image_boss_list.copy()
    boss_spawn_count = 0
    current_boss_image = image_boss_list[0]

    point = 0
    game_over = False
    success = False

    start_ticks = pygame.time.get_ticks()
    seconds = 0

    last_spawn_second = -1
    last_spawn_food = -3
    last_spawn_cigarette = -6
    last_spawn_broccoli = -5
    last_spawn_water = -7

    end_sound_played = False

reset_game()

# =====================================================
# INTRO
# =====================================================
intro_index = 0

# =====================================================
# MAIN LOOP
# =====================================================
game_started = False
play = True

while play:
    clock.tick(FPS)
    shake_x = 0
    shake_y = 0

    if game_state == STATE_TITLE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                mx /= scale_ratio
                my /= scale_ratio
                if start_button_rect_img.collidepoint(mx, my):
                    sfx_button.play()
                    intro_index = 0
                    game_state = STATE_INTRO

        background.blit(image_game_start_bg, (0, 0))
        background.blit(image_game_name, game_name_rect)
        background.blit(image_start_button, start_button_rect_img)

    elif game_state == STATE_INTRO:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sfx_button.play() 
                intro_index += 1
                if intro_index >= len(intro_images):
                    game_state = STATE_READY

        if intro_index < len(intro_images):
            background.blit(intro_images[intro_index], (0, 0))

    elif game_state == STATE_READY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                mx /= scale_ratio
                my /= scale_ratio
                if ready_start_rect_img.collidepoint(mx, my):
                    sfx_button.play()
                    sfx_start.play()
                    game_started = True
                    start_ticks = pygame.time.get_ticks()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(music_game_file)
                    pygame.mixer.music.play(-1)
                    game_state = STATE_GAME

        background.blit(image_game_start_bg, (0, 0))
        background.blit(image_ready_start_button, ready_start_rect_img)

    elif game_state == STATE_GAME:
        if game_started and not game_over and not success:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(TIME_LIMIT - seconds))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if (game_over or success) and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx /= scale_ratio
                my /= scale_ratio
                if retry_rect_img.collidepoint(mx, my):
                    sfx_button.play()
                    reset_game()
                    game_started = True
                    start_ticks = pygame.time.get_ticks()
                    pygame.mixer.music.load(music_game_file)
                    pygame.mixer.music.play(-1)
                if quit_rect_img.collidepoint(mx, my):
                    sfx_button.play()
                    play = False
            if game_started and not game_over and not success:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        to_x = move_speed
                    if event.key == pygame.K_LEFT:
                        to_x = -move_speed
                    if event.key == pygame.K_SPACE:
                        sfx_shoot.play()
                        for p in players:
                            bullets.append([p[0] + size_alveolus_width / 2 - size_bullet_width / 2, p[1]])
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        to_x = 0

        background.blit(image_bg, (0, 0))

        # =================================================
        # GAME LOGIC
        # =================================================
        if game_started and not game_over and not success:
            SpO2 -= SPO2_DECAY_PER_SEC * (clock.get_time() / 1000)
            if SpO2 < 0:
                SpO2 = 0
            if SpO2 <= 0:
                game_over = True

            if seconds - last_spawn_second >= DUST_SPAWN_INTERVAL:
                last_spawn_second = seconds
                x_dust = get_non_overlap_x(dusts + cigarettes, size_dust_width)
                dusts.append([x_dust, 0, DUST_HP])

            if seconds >= FOOD_SPAWN_START and int(seconds) - last_spawn_food >= FOOD_SPAWN_INTERVAL:
                last_spawn_food = int(seconds)
                x_food = get_non_overlap_x(dusts + cigarettes + foods, size_food_width)
                foods.append([x_food, 0, FOOD_HP])

            if seconds >= CIGARETTE_SPAWN_START and int(seconds) - last_spawn_cigarette >= CIGARETTE_SPAWN_INTERVAL:
                last_spawn_cigarette = int(seconds)
                x_cig = get_non_overlap_x(dusts + cigarettes, size_cigarette_width)
                cigarettes.append([x_cig, 0, CIGARETTE_HP])

            if (not boss_alive and remaining_boss_images and boss_spawn_count < BOSS_MAX_SPAWN
                and int(seconds) - last_boss_spawn >= BOSS_INTERVAL and seconds >= BOSS_FIRST_DELAY):
                sfx_boss.play()
                boss_alive = True
                boss_warning = True
                boss_warning_start = pygame.time.get_ticks()
                last_boss_spawn = int(seconds)
                x_pos_boss = random.randrange(0, BASE_WIDTH // 2 - size_boss_width)
                y_pos_boss = 0
                current_boss_image = random.choice(remaining_boss_images)
                remaining_boss_images.remove(current_boss_image)
                boss_hp = BOSS_HP
                boss_spawn_count += 1

            if int(seconds) - last_spawn_broccoli >= BROCCOLI_SPAWN_INTERVAL:
                last_spawn_broccoli = int(seconds)
                x_bro = get_non_overlap_x(broccolis + waters, size_broccoli_width, start_x=BASE_WIDTH // 2, end_x=BASE_WIDTH - size_broccoli_width, min_gap=40)
                broccolis.append([x_bro, 0])

            if int(seconds) - last_spawn_water >= WATER_SPAWN_INTERVAL:
                last_spawn_water = int(seconds)
                x_water = get_non_overlap_x(broccolis + waters, size_water_width, start_x=BASE_WIDTH // 2, end_x=BASE_WIDTH - size_water_width, min_gap=40)
                waters.append([x_water, 0])

            for t in NEBULIZER_SPAWN_TIMES:
                if seconds >= t and t not in nebulizer_spawned_times:
                    nebulizer_spawned_times.add(t)
                    min_x = BASE_WIDTH // 2
                    max_x = BASE_WIDTH - size_nebulizer_width
                    if max_x <= min_x:
                        x_neb = min_x
                    else:
                        x_neb = random.randrange(min_x, max_x)
                    nebulizers.append([x_neb, 0])

            for p in players:
                p[0] += to_x

            if len(players) > 0:
                min_x = min(p[0] for p in players)
                if min_x < 0:
                    diff = -min_x
                    for p in players:
                        p[0] += diff

                max_x = max(p[0] for p in players)
                if max_x > BASE_WIDTH - size_alveolus_width:
                    diff = max_x - (BASE_WIDTH - size_alveolus_width)
                    for p in players:
                        p[0] -= diff

            # -----------------------------
            # 적군 이동/렌더 및 플레이어-적 충돌 검사
            # -----------------------------
            for dust in dusts[:]:
                dust[1] += DUST_SPEED
                background.blit(image_dust, (dust[0], dust[1]))
                draw_mini_hp_bar(background, dust[0] + size_dust_width/2 - MINI_HP_BAR_W/2, dust[1] - 12, dust[2], DUST_HP)
                
                dust_rect = pygame.Rect(dust[0], dust[1], size_dust_width, size_dust_height)
                hit_player = False
                for p in players[:]:
                    p_rect = pygame.Rect(p[0], p[1], size_alveolus_width, size_alveolus_height)
                    if dust_rect.colliderect(p_rect):
                        players.remove(p)
                        if sfx_player_die: sfx_player_die.play() 
                        if dust in dusts: dusts.remove(dust)
                        hit_player = True
                        break 
                
                if hit_player: 
                    if len(players) <= 0: game_over = True
                    continue

                if dust[1] >= BASE_HEIGHT - size_dust_height:
                    game_over = True

            for food in foods[:]:
                food[1] += FOOD_SPEED
                background.blit(image_food, (food[0], food[1]))
                draw_mini_hp_bar(background, food[0] + size_food_width/2 - MINI_HP_BAR_W/2, food[1] - 12, food[2], FOOD_HP)
                
                food_rect = pygame.Rect(food[0], food[1], size_food_width, size_food_height)
                hit_player = False
                for p in players[:]:
                    p_rect = pygame.Rect(p[0], p[1], size_alveolus_width, size_alveolus_height)
                    if food_rect.colliderect(p_rect):
                        players.remove(p)
                        if sfx_player_die: sfx_player_die.play() 
                        if food in foods: foods.remove(food)
                        hit_player = True
                        break
                if hit_player:
                    if len(players) <= 0: game_over = True
                    continue

                if food[1] >= BASE_HEIGHT - size_food_height:
                    game_over = True

            for cigarette in cigarettes[:]:
                cigarette[1] += CIGARETTE_SPEED
                background.blit(image_cigarette, (cigarette[0], cigarette[1]))
                draw_mini_hp_bar(background, cigarette[0] + size_cigarette_width/2 - MINI_HP_BAR_W/2, cigarette[1] - 12, cigarette[2], CIGARETTE_HP)
                
                cig_rect = pygame.Rect(cigarette[0], cigarette[1], size_cigarette_width, size_cigarette_height)
                hit_player = False
                for p in players[:]:
                    p_rect = pygame.Rect(p[0], p[1], size_alveolus_width, size_alveolus_height)
                    if cig_rect.colliderect(p_rect):
                        players.remove(p)
                        if sfx_player_die: sfx_player_die.play() 
                        if cigarette in cigarettes: cigarettes.remove(cigarette)
                        hit_player = True
                        break
                if hit_player:
                    if len(players) <= 0: game_over = True
                    continue

                if cigarette[1] >= BASE_HEIGHT - size_cigarette_height:
                    game_over = True

            if boss_alive:
                y_pos_boss += BOSS_SPEED
                background.blit(current_boss_image, (x_pos_boss, y_pos_boss))
                draw_mini_hp_bar(background, x_pos_boss + size_boss_width/2 - BOSS_HP_BAR_W/2, y_pos_boss - 25, boss_hp, BOSS_HP, is_boss=True)
                
                boss_rect = pygame.Rect(x_pos_boss, y_pos_boss, size_boss_width, size_boss_height)
                for p in players[:]:
                    p_rect = pygame.Rect(p[0], p[1], size_alveolus_width, size_alveolus_height)
                    if boss_rect.colliderect(p_rect):
                        players.remove(p)
                        if sfx_player_die: sfx_player_die.play() 
                        boss_hp -= 5  
                        if boss_hp <= 0:
                            boss_alive = False
                            point += SCORE_BOSS
                            SpO2 = min(100, SpO2 + SPO2_GAIN_BOSS)
                        break 
                
                if len(players) <= 0: 
                    game_over = True

                if y_pos_boss >= BASE_HEIGHT - size_boss_height:
                    game_over = True

            # -----------------------------
            # 아이템 렌더 및 충돌 
            # -----------------------------
            for bro in broccolis[:]:
                bro[1] += BROCCOLI_SPEED
                background.blit(image_broccoli, (bro[0], bro[1]))

                if bro[1] >= BASE_HEIGHT - size_broccoli_height:
                    broccolis.remove(bro)
                    continue

                for p in players:
                    if (p[0] < bro[0] < p[0] + size_alveolus_width and
                        p[1] < bro[1] + size_broccoli_height < p[1] + size_alveolus_height):
                        sfx_item.play()
                        floating_texts.append([p[0], p[1], "Squad +1", (0, 255, 50), pygame.time.get_ticks()])
                        broccolis.remove(bro)
                        
                        if len(players) < BROCCOLI_MAX_STACK:
                            offset_x = size_alveolus_width * BROCCOLI_INSERT_OFFSET_RATIO
                            offset_y = size_alveolus_height * 0.6  
                            
                            if len(players) % ROW_CAPACITY == 0:
                                rightmost_x = max(pl[0] for pl in players)
                                top_y = min(pl[1] for pl in players)
                                players.insert(0, [rightmost_x, top_y - offset_y])
                            else:
                                players.insert(0, [players[0][0] - offset_x, players[0][1]])
                        break

            for water in waters[:]:
                water[1] += WATER_SPEED
                background.blit(image_water, (water[0], water[1]))

                if water[1] >= BASE_HEIGHT - size_water_height:
                    waters.remove(water)
                    continue

                for p in players:
                    if (p[0] < water[0] < p[0] + size_alveolus_width and
                        p[1] < water[1] + size_water_height < p[1] + size_alveolus_height):
                        sfx_item.play()
                        floating_texts.append([p[0], p[1], "Speed UP!", (0, 200, 255), pygame.time.get_ticks()])
                        waters.remove(water)
                        move_speed += WATER_SPEED_GAIN
                        break

            for neb in nebulizers[:]:
                neb[1] += NEBULIZER_SPEED
                background.blit(image_nebulizer, (neb[0], neb[1]))

                if neb[1] >= BASE_HEIGHT - size_nebulizer_height:
                    nebulizers.remove(neb)
                    continue

                neb_collected = False
                neb_rect = pygame.Rect(neb[0], neb[1], size_nebulizer_width, size_nebulizer_height)

                for p in players:
                    player_rect = pygame.Rect(p[0], p[1], size_alveolus_width, size_alveolus_height)
                    if neb_rect.colliderect(player_rect):
                        neb_collected = True
                        break

                if neb_collected:
                    sfx_nebulizer.play()
                    
                    floating_texts.append([players[0][0], players[0][1], "DAMAGE ALL -5", (0, 220, 255), pygame.time.get_ticks()])
                    
                    nebulizers.remove(neb)
                    nebulizer_effect = True
                    nebulizer_effect_start = pygame.time.get_ticks()

                    for dust in dusts[:]:
                        dust[2] -= NEBULIZER_ALL_ENEMY_HP_DEC
                        damage_popups.append((dust[0] + size_dust_width // 2, dust[1], pygame.time.get_ticks()))
                        if dust[2] <= 0:
                            dusts.remove(dust)
                            point += SCORE_DUST
                            SpO2 = min(100, SpO2 + SPO2_GAIN_DUST)

                    for food in foods[:]:
                        food[2] -= NEBULIZER_ALL_ENEMY_HP_DEC
                        damage_popups.append((food[0] + size_food_width // 2, food[1], pygame.time.get_ticks()))
                        if food[2] <= 0:
                            foods.remove(food)
                            point += SCORE_FOOD
                            SpO2 = min(100, SpO2 + SPO2_GAIN_FOOD)

                    for cigarette in cigarettes[:]:
                        cigarette[2] -= NEBULIZER_ALL_ENEMY_HP_DEC
                        damage_popups.append((cigarette[0] + size_cigarette_width // 2, cigarette[1], pygame.time.get_ticks()))
                        if cigarette[2] <= 0:
                            cigarettes.remove(cigarette)
                            point += SCORE_CIGARETTE
                            SpO2 = min(100, SpO2 + SPO2_GAIN_CIGARETTE)

                    if boss_alive:
                        boss_hp -= NEBULIZER_ALL_ENEMY_HP_DEC
                        damage_popups.append((x_pos_boss + size_boss_width // 2, y_pos_boss, pygame.time.get_ticks()))
                        if boss_hp <= 0:
                            boss_alive = False
                            point += SCORE_BOSS
                            SpO2 = min(100, SpO2 + SPO2_GAIN_BOSS)
                    break

            for bullet in bullets[:]:
                bullet[1] -= BULLET_SPEED
                background.blit(image_bullet, (bullet[0], bullet[1]))

                if bullet[1] <= 0:
                    if bullet in bullets: bullets.remove(bullet)
                    continue

                hit = False
                for dust in dusts[:]:
                    if (dust[0] < bullet[0] < dust[0] + size_dust_width and dust[1] < bullet[1] < dust[1] + size_dust_height):
                        dust[2] -= 1
                        if bullet in bullets: bullets.remove(bullet)
                        hit = True
                        if dust[2] <= 0:
                            dusts.remove(dust)
                            point += SCORE_DUST
                            SpO2 = min(100, SpO2 + SPO2_GAIN_DUST)
                        break
                if hit: continue

                for food in foods[:]:
                    if (food[0] < bullet[0] < food[0] + size_food_width and food[1] < bullet[1] < food[1] + size_food_height):
                        food[2] -= 1
                        if bullet in bullets: bullets.remove(bullet)
                        hit = True
                        if food[2] <= 0:
                            foods.remove(food)
                            point += SCORE_FOOD
                            SpO2 = min(100, SpO2 + SPO2_GAIN_FOOD)
                        break
                if hit: continue

                for cigarette in cigarettes[:]:
                    if (cigarette[0] < bullet[0] < cigarette[0] + size_cigarette_width and cigarette[1] < bullet[1] < cigarette[1] + size_cigarette_height):
                        cigarette[2] -= 1
                        if bullet in bullets: bullets.remove(bullet)
                        hit = True
                        if cigarette[2] <= 0:
                            cigarettes.remove(cigarette)
                            point += SCORE_CIGARETTE
                            SpO2 = min(100, SpO2 + SPO2_GAIN_CIGARETTE)
                        break
                if hit: continue

                if boss_alive:
                    if (x_pos_boss < bullet[0] < x_pos_boss + size_boss_width and y_pos_boss < bullet[1] < y_pos_boss + size_boss_height):
                        boss_hp -= 1
                        if bullet in bullets: bullets.remove(bullet)
                        if boss_hp <= 0:
                            boss_alive = False
                            point += SCORE_BOSS
                            SpO2 = min(100, SpO2 + SPO2_GAIN_BOSS)

            if seconds >= TIME_LIMIT:
                if SpO2 >= SPO2_WIN_THRESHOLD:
                    success = True
                else:
                    game_over = True

        # =================================================
        # DRAW: 플레이어 / HUD
        # =================================================
        
        for p in sorted(players, key=lambda val: val[1]):
            background.blit(image_alveolus, (p[0], p[1]))

        icon_x_point = 20
        icon_y_point = 20
        background.blit(image_icon_star, (icon_x_point, icon_y_point))
        draw_text_with_outline(background, f"{point}", font_ui, (255, 215, 0), (80, 50, 0), icon_x_point + ICON_SIZE + 10, icon_y_point)

        icon_x_time = BASE_WIDTH // 2 - 50
        icon_y_time = 20
        background.blit(image_icon_clock, (icon_x_time, icon_y_time))
        draw_text_with_outline(background, f"{time_left}", font_ui, (255, 255, 255), (50, 50, 50), icon_x_time + ICON_SIZE + 10, icon_y_time)

        bar_w = 400
        bar_h = 24
        bar_x = BASE_WIDTH // 2 - bar_w // 2
        bar_y = 65
        ratio = SpO2 / 100.0

        gauge_color = (0, 200, 100) if SpO2 >= SPO2_WIN_THRESHOLD else (255, 80, 80)
        draw_capsule_bar(background, bar_x, bar_y, bar_w, bar_h, ratio, gauge_color)

        icon_x_spo2 = bar_x
        icon_y_spo2 = bar_y - ICON_SIZE - 5
        background.blit(image_icon_spo2, (icon_x_spo2, icon_y_spo2))
        spo2_text = f"{int(SpO2)}%"
        draw_text_with_outline(background, spo2_text, font_ui, gauge_color, (0, 0, 0), icon_x_spo2 + ICON_SIZE + 10, icon_y_spo2)

        current_time = pygame.time.get_ticks()
        for f_text in floating_texts[:]:
            f_x, f_y, text, color, start_time = f_text
            dt = current_time - start_time
            if dt > FLOAT_TEXT_LIFETIME_MS:
                floating_texts.remove(f_text)
                continue
            f_text[1] -= FLOAT_TEXT_RISE_SPEED * clock.get_time()
            alpha = max(0, 255 - int((dt / FLOAT_TEXT_LIFETIME_MS) * 255))
            text_surf = font_ui.render(text, True, color)
            alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.blit(text_surf, (0, 0))
            alpha_surf.set_alpha(alpha)
            background.blit(alpha_surf, (f_x + size_alveolus_width/2 - text_surf.get_width()/2, f_y - 40))

        if boss_warning:
            elapsed = (pygame.time.get_ticks() - boss_warning_start) / 1000
            if elapsed > BOSS_WARNING_SEC:
                boss_warning = False
            else:
                shake_x = random.randint(-2, 2)
                shake_y = random.randint(-2, 2)
                if int(elapsed * 6) % 2 == 0:
                    flash = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
                    flash.set_alpha(100)
                    flash.fill((255, 0, 0))
                    background.blit(flash, (0, 0))
                
                if image_boss_warning:
                    bw_rect = image_boss_warning.get_rect(center=(BASE_WIDTH / 2, BASE_HEIGHT / 2 - 200))
                    background.blit(image_boss_warning, bw_rect)
                else:
                    txt = font_big.render("BOSS WARNING !!!", True, (255, 255, 0))
                    background.blit(txt, (BASE_WIDTH / 2 - txt.get_width() / 2, BASE_HEIGHT / 2 - 200))

        if nebulizer_effect:
            elapsed_ms = pygame.time.get_ticks() - nebulizer_effect_start
            if elapsed_ms > NEBULIZER_EFFECT_DURATION_MS:
                nebulizer_effect = False
            else:
                flash = pygame.Surface((BASE_WIDTH // 2, BASE_HEIGHT))
                flash.set_alpha(90)
                flash.fill((0, 220, 255))
                background.blit(flash, (0, 0))
                
                if image_nebulizer_effect:
                    neb_eff_rect = image_nebulizer_effect.get_rect(center=(BASE_WIDTH / 2, BASE_HEIGHT / 2 - 200)) 
                    background.blit(image_nebulizer_effect, neb_eff_rect)
                else:
                    neb_txt = font_big.render("NEBULIZER!", True, (0, 0, 0))
                    background.blit(neb_txt, (BASE_WIDTH / 2 - neb_txt.get_width() / 2, 500))

        for popup in damage_popups[:]:
            x, y, st = popup
            dt = pygame.time.get_ticks() - st
            if dt > POPUP_LIFETIME_MS:
                damage_popups.remove(popup)
                continue
            dy = dt * POPUP_RISE_PER_MS
            alpha = max(0, 255 - int(dt * POPUP_ALPHA_DEC_PER_MS))
            pop_surf = font_small.render(f"-{NEBULIZER_ALL_ENEMY_HP_DEC}", True, (0, 220, 255))
            pop_surf.set_alpha(alpha)
            background.blit(pop_surf, (x - pop_surf.get_width() / 2, (y - 30) - dy))

        # =================================================
        # END SCREEN (성공/실패) 
        # =================================================
        if game_over or success:
            if not end_sound_played:
                pygame.mixer.music.stop()
                if success:
                    sfx_success.play()
                else:
                    sfx_fail.play()
                end_sound_played = True

            if success:
                background.blit(image_success_bg, (0, 0))
            else:
                background.blit(image_fail_bg, (0, 0))

            board_w = 600
            board_h = 460 
            board_x = BASE_WIDTH // 2 - board_w // 2
            board_y = BASE_HEIGHT // 2 - 280 
            
            board_surface = pygame.Surface((board_w, board_h), pygame.SRCALPHA)
            board_surface.fill((0, 0, 0, 180)) 
            pygame.draw.rect(board_surface, (255, 255, 255, 100), (0, 0, board_w, board_h), width=4, border_radius=20)
            
            background.blit(board_surface, (board_x, board_y))

            if game_over:
                if image_gameover_title:
                    title_rect = image_gameover_title.get_rect(center=(BASE_WIDTH // 2, board_y + 80))
                    background.blit(image_gameover_title, title_rect)
                else:
                    draw_text_with_outline(background, "GAME OVER", font_title, (255, 80, 80), (0, 0, 0), 
                                           BASE_WIDTH // 2 - font_title.size("GAME OVER")[0] // 2, board_y + 20)
            else:
                if image_success_title:
                    title_rect = image_success_title.get_rect(center=(BASE_WIDTH // 2, board_y + 80))
                    background.blit(image_success_title, title_rect)
                else:
                    draw_text_with_outline(background, "SUCCESS!", font_title, (100, 255, 100), (0, 0, 0), 
                                           BASE_WIDTH // 2 - font_title.size("SUCCESS!")[0] // 2, board_y + 20)

            score_y = board_y + 250
            score_label = f"FINAL SCORE :  {point}"
            draw_text_with_outline(background, score_label, font_big, (255, 215, 0), (0, 0, 0), 
                                   BASE_WIDTH // 2 - font_big.size(score_label)[0] // 2, score_y)

            spo2_y = board_y + 330
            spo2_ratio = SpO2 / 100.0
            spo2_color = (0, 200, 100) if SpO2 >= SPO2_WIN_THRESHOLD else (255, 80, 80)
            
            spo2_status_txt = f"SpO2 Danger! ({int(SpO2)}%)" if SpO2 < SPO2_WIN_THRESHOLD else f"SpO2 Normal ({int(SpO2)}%)"
            
            text_width = font_ui.size(spo2_status_txt)[0]
            total_width = ICON_SIZE + 10 + text_width
            start_x = BASE_WIDTH // 2 - total_width // 2

            background.blit(image_icon_spo2, (start_x, spo2_y))
            draw_text_with_outline(background, spo2_status_txt, font_ui, spo2_color, (0, 0, 0), 
                                   start_x + ICON_SIZE + 10, spo2_y)
            
            draw_capsule_bar(background, BASE_WIDTH // 2 - 150, spo2_y + 50, 300, 24, spo2_ratio, spo2_color)

            retry_rect_img.center = (BASE_WIDTH / 2 - 140, board_y + board_h + 90)
            quit_rect_img.center = (BASE_WIDTH / 2 + 140, board_y + board_h + 90)
            
            background.blit(image_retry_button, retry_rect_img)
            background.blit(image_quit_button, quit_rect_img)

    # =====================================================
    # PRESENT (스케일링 출력)
    # =====================================================
    scaled = pygame.transform.scale(background, (display_w, display_h))
    screen.fill((0, 0, 0))
    screen.blit(scaled, (shake_x, shake_y))
    pygame.display.update()

pygame.quit()