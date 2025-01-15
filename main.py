import pygame
import sys
import os


# Pygameの初期化
pygame.init()

# ウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tamagotchi modoki")

# 背景の色設定 (RGB)
BACKGROUND_COLOR = (255, 249, 172)
BACKGROUND_COLOR2 = (0, 0, 0)

# 画像を読み込むパスを設定
assets_dir = "assets"
hunger_icon_path = os.path.join(assets_dir, "food.png")
happiness_icon_path = os.path.join(assets_dir, "happy.png")
energy_icon_path = os.path.join(assets_dir, "heart.png")
normal_character_path = os.path.join(assets_dir, "toya.png")
sad_character_path = os.path.join(assets_dir, "toya_bad.png")
happy_character_path = os.path.join(assets_dir, "toyaluv.png")
tombstone_path = os.path.join(assets_dir, "tombstone.png")

# フォントファイルのパスを指定
FONT_PATH = os.path.join("assets.gitignore", "YokohamaDotsJPN.otf")
FONT_SIZE = 30  # フォントサイズ
FONT_COLOR = (0, 0, 0)

# フォントの設定
font = pygame.font.Font(FONT_PATH, FONT_SIZE)  # カスタムフォントを指定

# アイコンの読み込み
hunger_icon = pygame.image.load(hunger_icon_path)
happiness_icon = pygame.image.load(happiness_icon_path)
energy_icon = pygame.image.load(energy_icon_path)

# アイコンを20x20にリサイズ
icon_size = (30, 30)  # 新しいアイコンのサイズ
hunger_icon = pygame.transform.scale(hunger_icon, icon_size)
happiness_icon = pygame.transform.scale(happiness_icon, icon_size)
energy_icon = pygame.transform.scale(energy_icon, icon_size)

# キャラクター画像の読み込み
normal_character = pygame.image.load(normal_character_path)
sad_character = pygame.image.load(sad_character_path)
happy_character = pygame.image.load(happy_character_path)
tombstone_image = pygame.image.load(tombstone_path)
normal_character = pygame.transform.scale(
    normal_character, (200, 200))  # キャラクター画像をリサイズ
sad_character = pygame.transform.scale(
    sad_character, (200, 200))  # キャラクター画像をリサイズ
happy_character = pygame.transform.scale(
    happy_character, (200, 200))  # キャラクター画像をリサイズ
tombstone_image = pygame.transform.scale(
    tombstone_image, (200, 200))

# デバウンスに必要な変数を追加
last_click_time = 0  # 最後のクリック時間
debounce_time = 500  # デバウンス時間（ミリ秒）

# ボタンの設定
button_font = font
button_width, button_height = 150, 50
button_color = (255, 175, 175)
button_hover_color = (230, 125, 130)

# ステータスの初期値
hunger = 50
happiness = 50
energy = 50

# ボタンの位置
hunger_x = screen_width // 4 - button_width // 2
happiness_x = screen_width // 2 - button_width // 2
energy_x = screen_width // 2 + screen_width // 4 - button_width // 2
button_y = screen_height // 2 - button_height + 200
hunger_button_rect = pygame.Rect(
    hunger_x, button_y, button_width, button_height)
happiness_button_rect = pygame.Rect(
    happiness_x, button_y, button_width, button_height)
energy_button_rect = pygame.Rect(
    energy_x, button_y, button_width, button_height)

# メインループ
game_over = False
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  if not game_over:
    # 背景を描画
    screen.fill(BACKGROUND_COLOR)

    # ステータスを徐々に減少 (0.002ずつ減少)
    happiness = max(happiness - 0.002, 0)  # 幸福度
    hunger = max(hunger - 0.002, 0)        # 空腹度
    energy = max(energy - 0.002, 0)        # エネルギー

# ゲームオーバーのチェック
    if happiness == 0 and hunger == 0 and energy == 0:
      game_over = True

  # キャラクターのグラフィックを決定
    if happiness < 20 or hunger < 20 or energy < 20:
      character_image = sad_character  # 状態が悪いときの画像
    elif happiness > 80 and hunger > 80 and energy > 80:
      character_image = happy_character  # 幸せなキャラクターの画像
    else:
      character_image = normal_character  # 通常の画像
    screen.fill(BACKGROUND_COLOR)
    character_x = screen_width // 2 - character_image.get_width() // 2
    character_y = screen_height // 2 - character_image.get_height() // 2
    screen.blit(character_image, (character_x, character_y))

  # 各ステータスに応じてアイコンを描画
    def draw_icons(value, icon, position):
      if value > 80:
        count = 5
      elif value > 60:
        count = 4
      elif value > 40:
        count = 3
      elif value > 20:
        count = 2
      elif value > 0:
        count = 1
      else:
        count = 0

      for i in range(count):
        screen.blit(icon, (position[0] + i * 40, position[1]))

    draw_icons(hunger, hunger_icon, (160, 48))
    draw_icons(happiness, happiness_icon, (160, 98))
    draw_icons(energy, energy_icon, (160, 148))

  # アイコン下にステータス値を表示
    hunger_text = font.render(f"おなか", True, (0, 0, 0))
    happiness_text = font.render(f"しあわせ", True, (0, 0, 0))
    energy_text = font.render(f"げんき", True, (0, 0, 0))
    screen.blit(hunger_text, (50, 48))
    screen.blit(happiness_text, (50, 98))
    screen.blit(energy_text, (50, 148))

    # マウスボタンが押された時の処理
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  # 左クリック
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()  # 現在のミリ秒を取得
        if current_time - last_click_time > debounce_time:  # デバウンス条件
          last_click_time = current_time  # クリック時間を更新
          if hunger_button_rect.collidepoint(mouse_pos):
            hunger += 10  # おなかを増加
          elif happiness_button_rect.collidepoint(mouse_pos):
            happiness += 10  # しあわせを増加
          elif energy_button_rect.collidepoint(mouse_pos):
            energy += 10  # げんきを増加

    # ボタンの描画
    for button_rect, label in [(hunger_button_rect, "ごはん"),
                               (happiness_button_rect, "あそぶ"),
                               (energy_button_rect, "おふろ")]:
        # マウス位置でボタンの色を変更
      if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, button_hover_color, button_rect)
      else:
        pygame.draw.rect(screen, button_color, button_rect)

      # ボタンのラベルを描画
      button_text = button_font.render(label, True, (255, 255, 255))
      text_rect = button_text.get_rect(center=button_rect.center)
      screen.blit(button_text, text_rect)

  else:
    screen.fill(BACKGROUND_COLOR2)
    character_image = tombstone_image  # 墓の画像
    character_x = screen_width // 2 - character_image.get_width() // 2
    character_y = screen_height // 2 - character_image.get_height() // 2
    screen.blit(character_image, (character_x, character_y))
    game_over_text = font.render("あなたの育てていたいきものはしんでしまいました", True, (255, 0, 0))
    restart_text = font.render("もう一度遊びますか？(Y/N)", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 2 -
                                 game_over_text.get_width() // 2, screen_height // 2 + 100))
    screen.blit(restart_text, (screen_width // 2 -
                               restart_text.get_width() // 2, screen_height // 2 + 130))

    # ゲームオーバー時の入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:  # 'Y'キーで再スタート
      happiness = 50
      hunger = 50
      energy = 50
      game_over = False
    elif keys[pygame.K_n]:  # 'N'キーで終了
      pygame.quit()
      sys.exit()

  # 画面を更新
  pygame.display.flip()
