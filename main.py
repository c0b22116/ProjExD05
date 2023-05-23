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
height = 900
goalheight = 150 #ゴールのおおきさ

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
        
class ball:
    def __init__(self):
        self._img = pg.image.load(f"ProjExD2023/ex05/fig/disc.png")
        self._rct = self._img.get_rect()
        self._rct.center = width/2, height/2
        self._vx, self._vy = +1,+1
        
    def update(self,screen: pg.Surface):
        yoko,tate = check_bound(screen.get_rect(), self._rct)
        if not yoko:
            self._vx *= -1
        if not tate:
            self._vy *= -1
        self._rct.move_ip(self._vx, self._vy)
        screen.blit(self._img,self._rct)
        
    def check_goal_in(self, scr_rect: pg.Rect, goalheight):
        """
        玉がゴールに入ったか否か、ゴールに入ったとしたらどちらのゴールかを判定する.
        引数：画面SurfaceのRect
        引数：玉のRect
        引数：ゴールの高さ
        戻り値：それぞれのゴールの衝突判定 左ゴール判定left: True or False / 右ゴール判定right: True or False
        """
        goal_in_left = False
        goal_in_right = False
        if (self._rct.left <= scr_rect.left) and (self._rct.top <= scr_rect.centery + goalheight) and (self._rct.bottom >= scr_rect.centery - goalheight):
            goal_in_left = True
        if (self._rct.right >= scr_rect.right) and (self._rct.top <= scr_rect.centery + goalheight) and (self._rct.bottom >= scr_rect.centery - goalheight):
            goal_in_right = True
        return goal_in_left, goal_in_right

def main():
    pg.display.set_caption("Air-hockey")
    screen = pg.display.set_mode((1600,900))
    pl1 = playerlect_1((width-300,height/2))
    disc = ball()
    clock = pg.time.Clock()
    bg_img = pg.image.load("ProjExD2023/ex05/fig/pg_bg.jpg")
    pk_img = pg.Surface((20,20))
    pg.draw.circle(pk_img, (255,0,0), (10,10), 10)
    pk_img.set_colorkey((0, 0, 0))
    pk_rect = pk_img.get_rect()
    pk_rect.center = random.randint(0, 1600), random.randint(0, 900)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            
        screen.blit(bg_img, [0, 0])
        screen.fill((0,0,0))
        pg.draw.line(screen, blue,(0,0), (screen.get_width()/2 - 5,0) ,20)
        pg.draw.line(screen, blue,(0,screen.get_height()), (screen.get_width()/2 - 5,screen.get_height()) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2+5,0), (screen.get_width() ,0) ,20)
        pg.draw.line(screen, red, (screen.get_width()/2 + 5,screen.get_height()) , (screen.get_width(),screen.get_height()) ,20)
        pg.draw.line(screen,white,(width/2,0),(width/2,height),5)
        pg.draw.line(screen, (0, 0, 255), (0,0), (0,screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, (0, 0, 255), (0,screen.get_height()/2 + goalheight), (0,screen.get_height()) ,5)
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),0), (screen.get_width(),screen.get_height()/2-goalheight) ,5)
        pg.draw.line(screen, (255, 0, 0), (screen.get_width(),screen.get_height()/2 + goalheight), (screen.get_width(),screen.get_height()) ,5)

            
        #ゴール判定 左ゴールに入った場合、g_leftがTrueに,右ゴールに入った場合、g_rightがTrueにそれぞれなる
        g_left, g_right = disc.check_goal_in(screen.get_rect(), goalheight)
        if g_left == True:
            break
        if g_right == True:
            break
        
        key_lst = pg.key.get_pressed()
        pl1.update(key_lst,screen)
        disc.update(screen)
        pg.display.update()
        clock.tick(1000)
        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()