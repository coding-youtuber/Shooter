"""
Part1
・ゲームの初期設定
・ゲームの画面をつくる
・プレイヤーを表示するだけ
"""


"""
Q1.画面の横幅を1500にしてください
"""
# pygameを読み込む
import pygame

# pygameを初期化
pygame.init()

# ゲーム画面の横幅
SCREEN_WIDTH = 800
# ゲーム画面の縦幅、横幅の80%にする
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# ゲーム画面を作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# ゲーム画面の上部にキャプション（ゲームタイトル）を設定
pygame.display.set_caption('Shooter')


class Soldier(pygame.sprite.Sprite):
	"""
	兵士クラス pygameのSpriteクラスを継承
	"""
	def __init__(self, x, y, scale):
		"""
		x: 兵士のx座標
		y: 兵士のy座標
		scale: 画像のスケール
		"""
		"""
		Q2.プレイヤー兵士の画像を敵の画像に変えてください
		"""
		# 親クラスの初期化
		pygame.sprite.Sprite.__init__(self)
		# 兵士の画像をロード
		img = pygame.image.load('img/player/Idle/0.png')
		# 画像のスケールに合わせて画像サイズを変形
		self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		# 画像を囲む四角形を取得
		self.rect = self.image.get_rect()
		# 画像を囲む四角形の中央座標に引数x,yを設定
		self.rect.center = (x, y)

	def draw(self):
		"""
		描画関数
		"""
		# ゲーム画面に兵士の画像を描画
		screen.blit(self.image, self.rect)


"""
Q3.三人目の兵士を作成し表示してください
"""

# 兵士クラスからインスタンスを生成。一人目の兵士。
player = Soldier(200, 200, 3)
# 兵士クラスからインスタンスを生成。二人目の兵士。
player2 = Soldier(400, 200, 3)



# ゲームの実行フラグ
run = True

# ゲームの実行フラグがTrueである限り、while文の中を実行する
while run:
	# 一人目の兵士を描画
	player.draw()
	# 二人目の兵士を描画
	player2.draw()

	# イベント処理
	for event in pygame.event.get():
		#終了イベント、画面を閉じる
		if event.type == pygame.QUIT:
			# ゲームが終了するとゲーム実行フラグがFalseになる
			run = False


	# ゲーム画面（スクリーン）全体を更新
	pygame.display.update()

# ゲームを終了する。quitは「やめる」の意味
pygame.quit()