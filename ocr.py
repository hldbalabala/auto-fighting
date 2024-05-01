from paddleocr import PaddleOCR
import pyautogui
import time

x1, y1 = 0, 0
x2, y2 = 450, 870


def ocr_detection():
    desktop_image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    desktop_image.save('screenshot.jpg', 'JPEG')
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr('screenshot.jpg', cls=True)
    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    return boxes, txts


def screenshot_and_click(boxes, txts, target, dx, dy):
    for idx, txt in enumerate(txts):
        if target in txt:
            center_x = (boxes[idx][0][0] + boxes[idx][1][0]) / 2 + dx
            center_y = (boxes[idx][1][1] + boxes[idx][2][1]) / 2 + dy
            pyautogui.click(x=center_x, y=center_y)
            print("目标",target,"已检测到，并在位置 ({}, {}) 处进行了点击操作。".format(center_x, center_y))
            break


def find_text(boxes, txts, target):
    for idx, txt in enumerate(txts):
        if target in txt:
            print("have found",target)
            return 1
    print("not find", target)
    return 0


def click(x,y):
    pyautogui.click(x, y)


main_state = 0
car_state = 1
chest_state = 1
energy_state = 0
auto_mode = 0
while 1:
    boxes, txts = ocr_detection()
    # print(txts)
    # avoid broken
    if find_text(boxes, txts, "恭喜获得") == 1:
        click((x1 + x2) / 2, (y1 + y2) / 4)
    if find_text(boxes, txts, "广告") == 1:
        screenshot_and_click(boxes, txts, "关闭", 0, 0)
    if find_text(boxes, txts, "选择技能") == 1:
        main_state = 1
    # if find_text(boxes, txts, "X1.5") == 1:
    #    screenshot_and_click(boxes, txts, "X1.5", 0, 0)
    # start menu
    if main_state == 0:
        # 领取巡逻车收益
        if find_text(boxes, txts, "章节越高，收益越大") == 1:
            if find_text(boxes, txts, "暂无奖励") == 0:
                screenshot_and_click(boxes, txts, "领取", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            elif find_text(boxes, txts, "快速巡逻") == 1 and find_text(boxes, txts, "0/3") == 0:
                screenshot_and_click(boxes, txts, "快速巡逻", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            elif find_text(boxes, txts, "观看广告") == 1 and find_text(boxes, txts, "0/3") == 0:
                screenshot_and_click(boxes, txts, "观看广告", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                screenshot_and_click(boxes, txts, "关闭", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            else:
                screenshot_and_click(boxes, txts, "快速巡逻", 0, 60)
                car_state = 1
        if car_state == 0:
            screenshot_and_click(boxes, txts, "巡逻车", 0, 0)
        # 领取宝箱
        if car_state == 1 and chest_state == 0:
            while find_text(boxes, txts, "普通宝箱") == 0:
                click(47,800)
                print("点击商城")
                time.sleep(1)
                boxes, txts = ocr_detection()
            while find_text(boxes, txts, "免费") == 1:
                screenshot_and_click(boxes, txts, "免费", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "广告") == 1:
                    screenshot_and_click(boxes, txts, "关闭", 0, 0)
                    boxes, txts = ocr_detection()
                time.sleep(2)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            chest_state = 1
            boxes, txts = ocr_detection()
            screenshot_and_click(boxes, txts, "战斗", 0, 0)
        #start fighting
        if car_state == 1 and chest_state == 1:
            # 确认体力充足
            boxes, txts = ocr_detection()
            screenshot_and_click(boxes, txts, "开始游戏", 0, 0)
            time.sleep(1)
            boxes, txts = ocr_detection()
            if find_text(boxes, txts, "体力购买") == 1:
                time.sleep(1)
                click((x1 + x2) / 2, y2-50)
                time.sleep(1)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "食堂") == 0:
                    click((x1 + x2) * 3 / 4, 800)
                    print("点击基地")
                    boxes, txts = ocr_detection()
                screenshot_and_click(boxes, txts, "食堂", 0, -50)
                time.sleep(1)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "领取") == 0:
                    print(txts)
                    screenshot_and_click(boxes, txts, "食堂", 0, -50)
                    boxes, txts = ocr_detection()
                screenshot_and_click(boxes, txts, "领取", 0, 0)
                time.sleep(1)
                click((x1 + x2) / 2, y2 - 50)
                print("点击空白退出")
                time.sleep(1)
                click(47, 800)
                print("返回")
                time.sleep(1)
                boxes, txts = ocr_detection()
                screenshot_and_click(boxes, txts, "战斗", 0, 0)
            else:
                main_state = 1
    # fighting
    elif main_state == 1:
        time.sleep(1)
        if auto_mode == 0:
            screenshot_and_click(boxes, txts, "开始游戏", 0, 0)
            if find_text(boxes, txts, "选择技能") == 1:
                screenshot_and_click(boxes, txts, "子弹爆炸", 0, 0)
                screenshot_and_click(boxes, txts, "连发", 0, 0)
                screenshot_and_click(boxes, txts, "齐射", 0, 0)
                screenshot_and_click(boxes, txts, "子弹穿透", 0, 0)
                screenshot_and_click(boxes, txts, "聚焦", 0, 0)
                screenshot_and_click(boxes, txts, "焦点引爆", 0, 0)
                screenshot_and_click(boxes, txts, "功率增幅", 0, 0)
                screenshot_and_click(boxes, txts, "军备强化", 0, 0)
                screenshot_and_click(boxes, txts, "闪击射线", 0, 0)
                screenshot_and_click(boxes, txts, "连续出击", 0, 0)
                screenshot_and_click(boxes, txts, "爆炸扩散", 0, 0)
                screenshot_and_click(boxes, txts, "选择技能", 0, 150)
            screenshot_and_click(boxes, txts, "精英掉落", 0, 0)
            if find_text(boxes, txts, "双倍奖励") == 1:
                screenshot_and_click(boxes, txts, "双倍奖励", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                screenshot_and_click(boxes, txts, "关闭", 0, 0)
            screenshot_and_click(boxes, txts, "返回", 0, 0)
        elif auto_mode == 1:
            screenshot_and_click(boxes, txts, "选择技能", 0, 150)
            screenshot_and_click(boxes, txts, "返回", 0, 0)
        elif auto_mode == 2:
            screenshot_and_click(boxes, txts, "选择技能", 0, 150)
            screenshot_and_click(boxes, txts, "返回", 0, 0)
        else:
            print("error")

    #time.sleep(1)
