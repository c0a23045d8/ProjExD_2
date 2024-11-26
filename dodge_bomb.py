import os
import random
import sys
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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20)) # 爆弾用の空Surface
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    pg.draw.circle(bb_img, (255, 0, 0),(10, 10), 10) # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0)) # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect() # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH) 
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, -5 # 爆弾ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        # 爆弾にあたった時の処理
        if kk_rct.colliderect(bb_rct):
            return #ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # 効果トンが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横にはみ出てる
            vx *= -1
        if not tate: # 盾にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
