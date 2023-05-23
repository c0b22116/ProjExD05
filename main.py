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

def check_goal_in(scr_rect: pg.Rect, obj_rect: pg.Rect):
    """
    玉がゴールに入ったか否か、ゴールに入ったとしたらどちらのゴールかを判定する.
    引数：画面SurfaceのRect
    引数：玉のRect
    戻り値：それぞれのゴールの衝突判定 right: True or False / left: True or False
    """
    
    goal_in_left = False
    goal_in_right = False
    if (obj_rect.left <= scr_rect.left) and (obj_rect.top <= scr_rect.centery + 100) and (obj_rect.bottom >= scr_rect.centery - 100):
        goal_in_left = True
    if (obj_rect.right >= scr_rect.right) and (obj_rect.top <= scr_rect.centery + 100) and (obj_rect.bottom >= scr_rect.centery - 100):
        goal_in_right = True
    return goal_in_left, goal_in_right
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ProjExD2023/ex05/fig/pg_bg.jpg")
    bp_img = pg.image.load("ProjExD2023/ex05/fig/bluepad.png")
    bp_img = pg.transform.rotozoom(bp_img, 0, 2.0)
    bp_rect = bp_img.get_rect()
    bp_rect.center = 400, 400
    
    pk_img = pg.Surface((20,20))
    pg.draw.circle(pk_img, (255,0,0), (10,10), 10)
    pk_img.set_colorkey((0, 0, 0))
    pk_rect = pk_img.get_rect()
    pk_rect.center = random.randint(0, 1600), random.randint(0, 900)
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
                bp_rect.move_ip(mv)
        if check_bound(screen.get_rect(), bp_rect) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    bp_rect.move_ip(-mv[0], -mv[1])
        screen.blit(bp_img, bp_rect) 
        
        yoko, tate = check_bound(screen.get_rect(), pk_rect)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pk_rect.move_ip(vx, vy)
        
        
        g_left, g_right = check_goal_in(screen.get_rect(), pk_rect)
        if g_left == True:
            print("a")
            break
        if g_right == True:
            print("b")
            break
        
        screen.blit(pk_img, pk_rect)
        pg.display.update()
        clock.tick(500)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()