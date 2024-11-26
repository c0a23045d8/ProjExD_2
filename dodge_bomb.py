import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 押下キーと移動量の対応関係を表す辞書DELTAを定義する
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5), 
         pg.K_RIGHT: (5, 0), pg.K_LEFT: (-5, 0)}



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果））
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False

    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    # 画面の幅ト高さの中心を計算
    text_x = WIDTH // 2 - 200
    text_y = HEIGHT // 2 - 50
    #画面をブラックアウトさせる
    bo = pg.Surface((WIDTH, HEIGHT))
    bo.fill((0,0,0)) # 黒く塗りつぶす
    bo.set_alpha(200) # 透過
    screen.blit(bo, (0,0)) # 描画

    # gameoverを表示
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255,255,255))
    screen.blit(text, (text_x, text_y))

    #泣いてるこうかとん
    kk_img8 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(kk_img8, (text_x - 50, text_y)) # 左
    screen.blit(kk_img8, (text_x + 390, text_y)) # 右
    pg.display.update()
    time.sleep(5)
    return

def init_bb_imags() -> tuple[list[pg.Surface], list[int]]:
    # 加速度リスト（サイズの増加率）
    accs = [a for a in range(1, 11)]  # 1から10までのサイズ変化
    bb_imgs = []  # 爆弾画像のリスト

    # 10段階で膨張する爆弾の画像を生成
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))  # 爆弾のサイズを段階的に変更
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 爆弾を描画
        bb_img.set_colorkey((0, 0, 0))  # 透明色に設定
        bb_imgs.append(bb_img)

    return bb_imgs, accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    引数:押下キーに対する移動量の合計値タプル
    戻り値:rotozoomしたSurface
    """
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    if sum_mv == (0, 0):
        return kk_img
    if sum_mv == (0, -5):
        return pg.transform.rotozoom(kk_img, 0, 0.9)
    if sum_mv == (0, 5):
        return pg.transform.rotozoom(kk_img, 180, 0.9)
    if sum_mv == (-5, 0):
        return pg.transform.rotozoom(kk_img, 90, 0.9)
    if sum_mv == (5, 0):
        return pg.transform.rotozoom(kk_img, 270, 0.9)
    if sum_mv == (-5, -5):
        return pg.transform.rotozoom(kk_img, 45, 0.9)
    if sum_mv == (5, -5):
        return pg.transform.rotozoom(kk_img, 315, 0.9)
    if sum_mv == (-5, 5):
        return pg.transform.rotozoom(kk_img, 135, 0.9)
    if sum_mv == (5, 5):
        return pg.transform.rotozoom(kk_img, 225, 0.9)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imags()  # 爆弾の画像リストと加速度リスト
    bb_rct = bb_imgs[0].get_rect()  # 初期爆弾画像のRect
    bb_rct.centerx = random.randint(0, WIDTH) 
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, -5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        # 爆弾に当たった時の処理
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return  # ゲームオーバー

        screen.blit(bg_img, [0, 0])  # 背景を描画

        # キー入力の処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        # 画面外に出ないようにする
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)  # こうかとんを描画

        # 爆弾の加速度に基づいて速度を調整
        avx = vx * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]  # サイズを変更した爆弾画像を取得
        bb_rct.width, bb_rct.height = bb_img.get_size()  # 爆弾のRectを更新
        bb_rct.move_ip(avx, vy)  # 爆弾を動かす

        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        # 爆弾が画面外に出ないように反転
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ている
            vx *= -1
        if not tate:  # 縦方向にはみ出ている
            vy *= -1

        screen.blit(bb_img, bb_rct)  # 爆弾を描画
        pg.display.update()  # 画面を更新

        tmr += 1
        clock.tick(50)  # FPS制御


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
