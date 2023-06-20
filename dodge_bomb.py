import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = (900, 400)

    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10,10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rect = bomb_img.get_rect()
    bomb_rect.center = (
        random.randint(0 + bomb_rect.width // 2, WIDTH - bomb_rect.width // 2),
        random.randint(0 + bomb_rect.height // 2, HEIGHT - bomb_rect.height // 2)
    )

    # こうかとんの移動
    kk_move = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }

    clock = pg.time.Clock()
    tmr = 0
    vx = 5; vy = 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])

        # こうかとんの移動
        key_list = pg.key.get_pressed() # 押下状態押下状態リスト
        合計移動量 = [0, 0]
        for key in kk_move: # 押下キーと移動量辞書から合計移動量を求める
            if key_list[key]:
                合計移動量[0] += kk_move[key][0]
                合計移動量[1] += kk_move[key][1]
        kk_rect.move_ip(合計移動量)
        screen.blit(kk_img, kk_rect)

        # 爆弾の移動
        bomb_rect.move_ip(vx, vy)
        screen.blit(bomb_img, bomb_rect)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()