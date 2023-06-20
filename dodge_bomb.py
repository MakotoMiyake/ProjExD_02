import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta: dict = {  # 押下キーと移動量の対応辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

accs = [a for a in range(1, 11)] #  加速度リスト

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し、真偽値タプルを返す
    引数 obj: オブジェクト（爆弾、こうかとん）SurfaceのRectオブジェクト
    戻り値: 横方向, 縦方向のはみ出し判定結果（画面内:True/画面外:False）
    """
    width, height = True, True
    if obj.left < 0 or WIDTH < obj.right: #  横方向のはみ出し判定
        width = False
    if obj.top < 0 or HEIGHT < obj.bottom: #  縦方向のはみ出し判定
        height = False
    return width, height

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # 背景
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    # こうかとん
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = (900, 400)  # 初期位置
    kk_img_r = pg.transform.flip(kk_img, True, False)  # 反転こうかとん
    kk_img_go = pg.image.load("ex02/fig/6.png")  # ゲームオーバーこうかとん
    kk_img_go = pg.transform.rotozoom(kk_img_go, 0, 2.0)

    # 押下キーとrotozoomした画像の対応辞書
    kk_imgs: dict = {
    (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
    (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),
    (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
    (0, -5): pg.transform.rotozoom(kk_img_r, 90, 1.0),
    (+5, -5): pg.transform.rotozoom(kk_img_r, 45, 1.0),
    (+5, 0): pg.transform.rotozoom(kk_img_r, 0, 1.0),
    (+5, +5): pg.transform.rotozoom(kk_img_r, -45, 1.0),
    (0, +5): pg.transform.rotozoom(kk_img_r, -90, 1.0),
    }

    # 爆弾
    bomb_img = pg.Surface((20, 20))
    pg.draw.circle(bomb_img, (255, 0, 0), (10,10), 10)
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rect = bomb_img.get_rect()
    bomb_rect.center = (
        random.randint(0 + bomb_rect.width // 2, WIDTH - bomb_rect.width // 2),
        random.randint(0 + bomb_rect.height // 2, HEIGHT - bomb_rect.height // 2)
    )


    clock = pg.time.Clock()
    tmr = 0
    vx = 5; vy = 5  # 移動量
    goflag = False  # ゲームオーバーフラグ
    time = 0  # 経過時間
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        screen.blit(bg_img, [0, 0])  # 背景の描画

        # こうかとんの移動
        key_list = pg.key.get_pressed() # 押下状態押下状態リスト
        # 押下キーと移動量辞書から合計移動量を求める
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_list[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rect.move_ip(sum_mv)
        # 更新後の位置が画面外になった場合、更新前の座標に戻す
        if check_bound(kk_rect) != (True, True):
            kk_rect.move_ip([-sum_mv[0], -sum_mv[1]])
        
        # 更新後の位置が画面外になった場合、移動量を反転する
        width, height = check_bound(bomb_rect)
        if not width:  # 横方向に画面外だったら
            vx *= -1
        if not height:  # 縦方向に画面外だったら
            vy *= -1
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # 加速度
        bomb_rect.move_ip(avx, avy)  # 爆弾の移動
        screen.blit(bomb_img, bomb_rect)  # 爆弾の描画

        # こうかとんと爆弾の衝突判定
        if kk_rect.colliderect(bomb_rect):
            screen.blit(kk_img_go, kk_rect)  # ゲームオーバーこうかとんの描画
            goflag = True
        else:
            screen.blit(kk_imgs[tuple(sum_mv)], kk_rect)  # こうかとんの描画
        
        # ゲームオーバー処理
        if goflag:
            print("GAME OVER")
            screen.blit(kk_img_go, kk_rect)  # ゲームオーバーこうかとんの描画
            screen.blit(font.render("Time: " + str(time), True, (0, 0, 255)), [0, 0])
            screen.blit(font_go.render("GAME OVER", True, (255, 0, 0)), [430, 390])
            pg.display.update()
            clock.tick(0.5)
            return
        
        if tmr % 50 == 0:
            time += 1

        # 経過時間の表示
        font = pg.font.Font(None, 80) # 経過時間表示用のフォント
        font_go = pg.font.Font(None, 160)  # ゲームオーバー時のフォント
        screen.blit(font.render("Time: " + str(time), True, (0, 0, 255)), [0, 0])

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()