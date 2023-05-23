import random
import sys
import time

import pygame as pg



delta = {
    pg.K_UP: (0, -2),
    pg.K_DOWN: (0, +2),
    pg.K_LEFT: (-2, 0),
    pg.K_RIGHT: (+2, 0),
    }

accs = [a for a in range(1, 11)] 

def check_bound(scr_rect: pg.Rect, obj_rect: pg.Rect):
    """
    オブジェクトが画面内or画面外を判定する
    引数：画面SurfaceのRect
    引数：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    
    yoko, tate = True, True
    if obj_rect.left < scr_rect.left or scr_rect.right < obj_rect.right:
        yoko = False
    if obj_rect.top < scr_rect.top or scr_rect.bottom < obj_rect.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ProjExD2023/ex05/fig/pg_bg.jpg")
    kk_img = pg.image.load("ProjExD2023/ex05/fig/bluepad.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = 900, 400
    
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rect = bb_img.get_rect()
    bb_rect.center = random.randint(0, 1600), random.randint(0, 900)
    vx, vy = +1, +1
    fonto  = pg.font.Font(None, 80)
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
        tmr += 1
        screen.blit(bg_img, [0, 0])
        
        
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rect.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rect) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rect.move_ip(-mv[0], -mv[1])
        screen.blit(kk_img, kk_rect) 
        
        yoko, tate = check_bound(screen.get_rect(), bb_rect)
        if not yoko:
            vx *= -1
            print("yoko")
        if not tate:
            vy *= -1
            print("tate")
            
        bb_rect.move_ip(vx, vy)
        screen.blit(bb_img, bb_rect)
                
        pg.display.update()
        clock.tick(500)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()