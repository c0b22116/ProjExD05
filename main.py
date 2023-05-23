import pygame as pg
import sys
import time
import random

white = (255,255,255)
black = (0,0,0)
green = (0,150,0)
red = (255,0,0)
blue = (0,0,255)
light_blue = (147,251,253)
width = 1600
hight = 900
goalheight = 50 #ゴールのおおきさ

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

class playerlect_1:

    _delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }
    

    def __init__(self, xy: tuple[int,int]): 
        self._img = pg.transform.rotozoom(pg.image.load(f"ProjExD2023/ex05/fig/redpad.png"),0, 2.0)
        self._rct = self._img.get_rect()
        self._rct.center = xy


    def update(self,key_lst: list[bool], screen: pg.Surface):
        for k,mv in __class__._delta.items():
            if key_lst[k]:
                self._rct.move_ip(mv)

        screen.blit(self._img,self._rct)
        

def main():
    pg.display.set_caption("Air-hockey")
    screen = pg.display.set_mode((1600,900))
    pl1 = playerlect_1((width-300,hight/2))
    clock = pg.time.Clock()
    
    bg_img = pg.image.load("ProjExD2023/ex05/fig/pg_bg.jpg")
    pk_img = pg.Surface((20,20))
    pg.draw.circle(pk_img, (255,0,0), (10,10), 10)
    pk_img.set_colorkey((0, 0, 0))
    pk_rect = pk_img.get_rect()
    pk_rect.center = random.randint(0, 1600), random.randint(0, 900)
    vx, vy = +1, +1
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            
        screen.blit(bg_img, [0, 0])

        screen.fill((0,0,0))
        pg.draw.line(screen, blue,(0,0), (screen.get_width()/2 - 5,0) ,20)
        pg.draw.line(screen, blue,(0,screen.get_height()), (screen.get_width()/2 - 5,screen.get_height()) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2+5,0), (screen.get_width() ,0) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2 + 5,screen.get_height()) , (screen.get_width(),screen.get_height()) ,20)
        pg.draw.line(screen,white,(width/2,0),(width/2,hight),5)
        pg.draw.line(screen, (0, 0, 255), (0,0), (0,screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, (0, 0, 255), (0,screen.get_height()/2 + goalheight), (0,screen.get_height()) ,5)
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),0), (screen.get_width(),screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),screen.get_height()/2 + goalheight), (screen.get_width(),screen.get_height()) ,5)

        yoko, tate = check_bound(screen.get_rect(), pk_rect)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
            
        
        pk_rect.move_ip(vx, vy)
        screen.blit(pk_img, pk_rect)
        
        key_lst = pg.key.get_pressed()
        pl1.update(key_lst,screen)

        pg.display.update()
        clock.tick(1000)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()