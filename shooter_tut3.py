"""
Part3
・プレイヤーがジャンプできる
・ジャンプすると重力が働き下に落ちる
・地面を作成。プレイヤーは地面より下に落ちない。
"""
# pygameを読み込む
import pygame
# OSの機能を利用した処理をするosを読み込む。ディレクトリの操作などが行える。
import os

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

"""
Q1.重力を弱めてください
"""
#重力の大きさ。ジャンプした時に落ちる力。
GRAVITY = 0.75

# プレイヤーの進行方向のフラグ
moving_left = False
moving_right = False


# 背景色のRGB値。Red,Blue,Green
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
	"""
	背景色を描画
	"""
	# 背景色でスクリーンを塗りつぶす
	screen.fill(BG)
	# 地面の赤い線を描画する
	pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


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
		# 生死フラグ
		self.alive = True
		# 兵士の種類を代入
		self.char_type = char_type
		# 兵士の移動スピードを代入
		self.speed = speed
		# 兵士の進行方向 右が1、左が-1
		self.direction = 1
		# Y軸方向の速度
		self.vel_y = 0
		# ジャンプのフラグ
		self.jump = False
		# 空中にいるかどうかのフラグ
		self.in_air = True
		# 水平反転フラグ
		self.flip = False
		# アニメーション画像を入れるリスト
		self.animation_list = []
		# フレーム画像のインデックス（何番目の画像か）
		self.frame_index = 0
		# アクション番号
		self.action = 0
		# 更新時刻
		self.update_time = pygame.time.get_ticks()
		
		# プレイヤーのアニメーションの種類 停止、走る、ジャンプ
		animation_types = ['Idle', 'Run', 'Jump']

		# 各アニメーションに必要な画像をリストに追加していく
		for animation in animation_types:
			# 一時的に使う画像を入れるリストを初期化
			temp_list = []
			# フォルダの中にある画像の枚数を数える
			num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
			# 各フレーム画像に対して処理を行う
			for i in range(num_of_frames):
				# 画像を読み込む（ロード） 画像名がフレームの番号と対応している
				img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
				# 画像のスケールに合わせて画像サイズを変形
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				# 一時的に使うリストに追加
				temp_list.append(img)
			# アニメーション画像のリストにリストを追加。リストの中にリストを入れています。
			self.animation_list.append(temp_list)

		# アクションとフレームインデックスに対応した画像を取得
		self.image = self.animation_list[self.action][self.frame_index]
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


		"""
		Q2.兵士のジャンプ力を上げてください
		"""
		#ジャンプ
		# ジャンプ中かつ空中フラグはまだFalse
		if self.jump == True and self.in_air == False:
			# Y軸方向の速度
			self.vel_y = -11
			# ジャンプのフラグを更新
			self.jump = False
			# 空中フラグを更新
			self.in_air = True

		# 重力を適用。Y軸方向の速度に重力を加える。この重力は重力速度である。単位時間あたりの速度と考えるので力をそのまま速度に足して良い。
		"""
		時間:t
		単位時間あたりの移動距離（Y軸方向）: a
		単位時間あたりの移動距離（重力）: b
		としたら
		vel_y: a/t
		GRAVITY: b/t

		単位時間なのでt=1としてよい。
		なので
		速度を足すと
		a + b
		になる
		"""
		self.vel_y += GRAVITY
		# Y軸方向の速度が一定以上なら
		if self.vel_y > 10:
			# 速さはゼロになる
			self.vel_y
		# Y軸方向の微小な移動距離を更新.単位時間なので距離に速度を足すことができる
		dy += self.vel_y

		"""
		Q3.兵士が床の下に行けるようにしてください	
		"""
		# 床との衝突判定
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			# 空中フラグを更新
			self.in_air = False

		# 画像を囲む四角形の位置を移動量に合わせて更新
		self.rect.x += dx
		self.rect.y += dy


	def update_animation(self):
		"""
		アニメーションを更新
		"""
		ANIMATION_COOLDOWN = 100
		# 現在のフレームに合わせて画像を取得
		self.image = self.animation_list[self.action][self.frame_index]
		# 最後の更新タイミングからANIMATION_COOLDOWNの時間だけが経っていたら
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			# 更新時刻を更新
			self.update_time = pygame.time.get_ticks()
			# フレームインデックスを1増やす
			self.frame_index += 1
		# フレームインデックスがアニメーションのリストの長さよりも大きくなったら
		if self.frame_index >= len(self.animation_list[self.action]):
			# フレームインデックスを0に戻す
			self.frame_index = 0



	def update_action(self, new_action):
		"""
		アクションを更新
		"""
		# 新しいアクションが前回のアクションと異なる場合
		if new_action != self.action:
			# アクションを新しいアクションに更新
			self.action = new_action
			# アニメーションの設定を更新。フレームインデックスを0、更新時刻を更新
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()


	def draw(self):
		"""
		描画関数
		"""
		# ゲーム画面に兵士の画像を描画。水平反転フラグに合わせて向きを変えて描画。
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



# 兵士クラスからインスタンスを生成。プレイヤーとする。
player = Soldier('player', 200, 200, 3, 5)
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

	# プレイヤーのアニメーションを更新
	player.update_animation()
	# プレイヤーを描画
	player.draw()
	# 敵を描画
	enemy.draw()


	"""
	プレイヤーのアクションを更新
	"""
	# プレイヤーが生きている場合
	if player.alive:
		# プレイヤーが空中にいる場合
		if player.in_air:
			# ジャンプアクションを実行
			player.update_action(2)
		# 左右どちらかに移動している場合
		elif moving_left or moving_right:
			# 走るアクションを実行
			player.update_action(1)
		else:
			# そのほかの場合、停止アクションを実行
			player.update_action(0)
		# プレイヤーを移動
		player.move(moving_left, moving_right)


	# イベント処理
	for event in pygame.event.get():
		#終了イベント
		if event.type == pygame.QUIT:
			# ゲームが終了するとゲーム実行フラグがFalseになる
			run = False
		# あるキーを押す
		if event.type == pygame.KEYDOWN:
			# aキーを押す
			if event.key == pygame.K_a:
				# 左移動フラグをTrue
				moving_left = True
			# dキーを押す
			if event.key == pygame.K_d:
				# 右移動フラグをTrue
				moving_right = True
			# wキーを押す、かつ、プレイヤーが生きている
			if event.key == pygame.K_w and player.alive:
				# ジャンプフラグをTrue
				player.jump = True
			#ESCキーを押すとゲームが終了する
			if event.key == pygame.K_ESCAPE:
				# ゲームが終了するとゲーム実行フラグがFalseになる
				run = False


		# キーを離した
		if event.type == pygame.KEYUP:
			# aキーを離した
			if event.key == pygame.K_a:
				# 左移動フラグをFalse
				moving_left = False
			# dキーを離した
			if event.key == pygame.K_d:
				# 右移動フラグをFalse
				moving_right = False


	# ゲーム画面（スクリーン）全体を更新
	pygame.display.update()

# ゲームを終了する。quitは「やめる」の意味
pygame.quit()