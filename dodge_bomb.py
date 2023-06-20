import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def chek_bound(area: pg.Rect, obj: pg.rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真偽値タプルを返す
    引数1 area: 画面SurfaceのRect
    引数2 obj: オブジェクト（爆弾、こうかとん）SurfaceのRectオブジェクト
    戻り値: 横方向, 縦方向のはみ出し判定結果（画面内:True/画面外:False）
    """
    width, height = True, True
    if obj.left < area.left or area.right < obj.right: #  横方向のはみ出し判定
        width = False
    if obj.top < area.top or area.bottom < obj.bottom: #  縦方向のはみ出し判定
        height = False
    return width, height

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # 背景
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    bg_rect = bg_img.get_rect()

    # こうかとん
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = (900, 400)

    # 爆弾
    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10,10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rect = bomb_img.get_rect()
    bomb_rect.center = (
        random.randint(0 + bomb_rect.width // 2, WIDTH - bomb_rect.width // 2),
        random.randint(0 + bomb_rect.height // 2, HEIGHT - bomb_rect.height // 2)
    )

    kk_move = {  # 押下キーと移動量の対応辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }

    clock = pg.time.Clock()
    tmr = 0
    vx = 5; vy = 5  # 移動量
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])  # 背景の描画

        # こうかとんの移動
        pos = kk_rect.center
        key_list = pg.key.get_pressed() # 押下状態押下状態リスト
        合計移動量 = [0, 0]
        # 押下キーと移動量辞書から合計移動量を求める
        for key in kk_move: 
            if key_list[key]:
                合計移動量[0] += kk_move[key][0]
                合計移動量[1] += kk_move[key][1]
        kk_rect.move_ip(合計移動量)
        # 更新後の位置が画面外になった場合、更新前の座標に戻す
        if (not chek_bound(bg_rect, kk_rect)[0]) or (not chek_bound(bg_rect, kk_rect)[1]):
            kk_rect.center = pos
        
        screen.blit(kk_img, kk_rect)  # こうかとんの描画

        # 更新後の位置が画面外になった場合、移動量を反転する
        if not chek_bound(bg_rect, bomb_rect)[0]:
            vx *= -1
        if not chek_bound(bg_rect, bomb_rect)[1]:
            vy *= -1
        bomb_rect.move_ip(vx, vy)  # 爆弾の移動
        screen.blit(bomb_img, bomb_rect)  # 爆弾の描画

        # こうかとんと爆弾の衝突判定
        if kk_rect.colliderect(bomb_rect):
            return 

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()