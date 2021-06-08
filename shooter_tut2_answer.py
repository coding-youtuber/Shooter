"""
Part2
・敵プレイヤーを表示
・プレイヤーを動かす
・キー操作
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

# 時間管理を行うClockオブジェクトを作成。フレームレートの設定に使います
clock = pygame.time.Clock()
#FPS=frame per second。1秒間に何回フレームを描画するのか。60だと滑らか。
FPS = 60

# プレイヤーの進行方向のフラグ
moving_left = False
moving_right = False


"""
Q1. 背景色を青色に変えてください
"""
# 背景色のRGB値。Red,Green,Blue
# BG = (144, 201, 120)
# Q1の解答
BG = (0, 0, 255)

def draw_bg():
	"""
	背景色を描画
	"""
	# 背景色でスクリーンを塗りつぶす
	screen.fill(BG)



class Soldier(pygame.sprite.Sprite):
	"""
	兵士クラス pygameのSpriteクラスを継承
	"""
	def __init__(self, char_type, x, y, scale, speed):
		"""
		char_type: 兵士の種類（文字列）
		x: 兵士のx座標
		y: 兵士のy座標
		scale: 画像のスケール
		speed: 移動スピード
		"""
		# 親クラスの初期化
		pygame.sprite.Sprite.__init__(self)
		# 兵士の種類を代入
		self.char_type = char_type
		# 兵士の移動スピードを代入
		self.speed = speed
		# 兵士の進行方向 右が1、左が-1
		self.direction = 1
		# 水平反転フラグ
		self.flip = False
		# 兵士の種類に合わせて兵士の画像をロード
		img = pygame.image.load(f'img/{self.char_type}/Idle/0.png')
		# 画像のスケールに合わせて画像サイズを変形
		self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
		# 画像を囲む四角形を取得
		self.rect = self.image.get_rect()
		# 画像を囲む四角形の中央座標に引数x,yを設定
		self.rect.center = (x, y)


	def move(self, moving_left, moving_right):
		"""
		兵士の移動
		moving_left: 左移動フラグ
		moving_right: 右移動フラグ

		"""
		# 移動量をリセット。dx,dyと表記しているのは微小な移動量を表すため。微分、積分で使うdx,dy。
		dx = 0
		dy = 0

		# 左に移動
		if moving_left:
			# スピードの分だけ移動。座標系において左は負の方向
			dx = -self.speed
			# 画像を水平反転するのでTrue
			self.flip = True
			# 進行方向フラグは左なので-1
			self.direction = -1
		# 右に移動
		if moving_right:
			# スピードの分だけ移動。座標系において左は負の方向
			dx = self.speed
			# 画像を水平反転する必要はないのでFalse
			self.flip = False
			# 進行方向フラグは右なので1
			self.direction = 1


		# 画像を囲む四角形の位置を移動量に合わせて更新
		self.rect.x += dx
		self.rect.y += dy


	def draw(self):
		"""
		描画関数
		"""
		# ゲーム画面に兵士の画像を描画。水平反転フラグに合わせて向きを変えて描画。
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



"""
Q2. 兵士の移動スピードを速くしてください
"""
# 兵士クラスからインスタンスを生成。プレイヤーとする。
# player = Soldier('player', 200, 200, 3, 5)
# Q2の解答。引数speedの値を5より大きくする
player = Soldier('player', 200, 200, 3, 20)
# 兵士クラスからインスタンスを生成。敵とする。
enemy = Soldier('enemy', 400, 200, 3, 5)



# ゲームの実行フラグ
run = True
# ゲームの実行フラグがTrueである限り、while文の中を実行する
while run:

	# clockオブジェクトを更新。この命令はフレームごとに実行される必要がある
	clock.tick(FPS)

	# 背景色を描画
	draw_bg()

	# プレイヤーを描画
	player.draw()
	# 敵を描画
	enemy.draw()

	# プレイヤーを移動
	player.move(moving_left, moving_right)


	"""
	Q3.左右キーでも左右の移動ができるようにしてください
	左キーは「K_LEFT」
	右キーは「K_RIGHT」とします

	https://www.pygame.org/docs/ref/key.html
	"""
	# イベント処理
	for event in pygame.event.get():
		#終了イベント
		if event.type == pygame.QUIT:
			# ゲームが終了するとゲーム実行フラグがFalseになる
			run = False
		# あるキーを押す
		if event.type == pygame.KEYDOWN:
			# Q3の解答。aキーを押す or 左キーを押す
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				# 左移動フラグをTrue
				moving_left = True
			# Q3の解答。dキーを押す or 右キーを押す
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				# 右移動フラグをTrue
				moving_right = True
			#ESCキーを押すとゲームが終了する
			if event.key == pygame.K_ESCAPE:
				# ゲームが終了するとゲーム実行フラグがFalseになる
				run = False


		# キーを離した
		if event.type == pygame.KEYUP:
			# Q3の解答。aキーを離した or 左キーを離した
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				# 左移動フラグをFalse
				moving_left = False
			# Q3の解答。dキーを離した or 右キーを離した
			if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				# 右移動フラグをFalse
				moving_right = False




	# ゲーム画面（スクリーン）全体を更新
	pygame.display.update()

# ゲームを終了する。quitは「やめる」の意味
pygame.quit()