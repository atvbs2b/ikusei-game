import pygame
import sys
import os


# Pygameの初期化
pygame.init()

# ウィンドウの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tamagotchi Game with Icons")

# 背景の色設定 (RGB)
BACKGROUND_COLOR = (255, 249, 172)

# 画像を読み込むパスを設定
assets_dir = "assets"
hunger_icon_path = os.path.join(assets_dir, "food.png")
happiness_icon_path = os.path.join(assets_dir, "happy.png")
energy_icon_path = os.path.join(assets_dir, "heart.png")
normal_character_path = os.path.join(assets_dir, "toya.png")
sad_character_path = os.path.join(assets_dir, "toya_bad.png")


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
normal_character = pygame.transform.scale(
    normal_character, (200, 200))  # キャラクター画像をリサイズ
sad_character = pygame.transform.scale(
    sad_character, (200, 200))  # キャラクター画像をリサイズ

# ステータスの初期値
hunger = 100
happiness = 50
energy = 50

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

  # キャラクターのグラフィックを決定
  if happiness < 20 or hunger < 20 or energy < 20:
    character_image = sad_character   # 状態が悪いときの画像
  else:
    character_image = normal_character  # 通常の画像

  # キャラクターの描画 (中央に配置)
  character_x = screen_width // 2 - character_image.get_width() // 2
  character_y = screen_height // 2 - character_image.get_height() // 2
  screen.blit(character_image, (character_x, character_y))

  # ステータスを徐々に減少 (0.002ずつ減少)
  happiness = max(happiness - 0.002, 0)  # 幸福度
  hunger = max(hunger - 0.002, 0)        # 空腹度
  energy = max(energy - 0.002, 0)        # エネルギー

  # ゲームオーバーのチェック
  if happiness == 0 and hunger == 0 and energy == 0:
    game_over = True

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

  # ゲームオーバーの状態をチェック
  if game_over:
    game_over_text = font.render("あなたの育てていたいきものはしんでしまいました", True, (255, 0, 0))
    restart_text = font.render("もう一度遊びますか？(Y/N)", True, (0, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 -
                                 game_over_text.get_width() // 2, screen_height // 2 - 20))
    screen.blit(restart_text, (screen_width // 2 -
                               restart_text.get_width() // 2, screen_height // 2 + 20))

    # ゲームオーバー時の入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:  # 'Y'キーで再スタート
      happiness = 100
      hunger = 100
      energy = 100
      game_over = False
    elif keys[pygame.K_n]:  # 'N'キーで終了
      pygame.quit()
      sys.exit()

  # 画面を更新
  pygame.display.flip()
