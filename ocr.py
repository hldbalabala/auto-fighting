from paddleocr import PaddleOCR
import pyautogui
import time


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


def find_text_and_click(boxes, txts, target, dx, dy):
    for idx, txt in enumerate(txts):
        if target in txt:
            center_x = (boxes[idx][0][0] + boxes[idx][1][0]) / 2 + dx
            center_y = (boxes[idx][1][1] + boxes[idx][2][1]) / 2 + dy
            pyautogui.click(x=center_x + x1, y=center_y + y1)
            print("目标", target, "已检测到，并在位置 ({}, {}) 处进行了点击操作。".format(center_x, center_y))
            break


def find_text(boxes, txts, target):
    for idx, txt in enumerate(txts):
        if target in txt:
            center_x = (boxes[idx][0][0] + boxes[idx][1][0]) / 2
            center_y = (boxes[idx][1][1] + boxes[idx][2][1]) / 2
            print("have found", target)
            return center_x + x1, center_y + y1
    print("not find", target)
    return -1, -1


def click(x, y):
    pyautogui.click(x, y)


x1 = y1 = x2 = y2 = 0
while 1:
    desktop_image = pyautogui.screenshot()
    desktop_image.save('screenshot.jpg', 'JPEG')
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr('screenshot.jpg', cls=True)
    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    start_x, start_y = find_text(boxes, txts, "开始游戏")
    normal_x, normal_y = find_text(boxes, txts, "普通")
    time.sleep(1)
    if start_x > 0 and start_y > 0 and normal_x > 0 and normal_y > 0:
        break
x1 = int(start_x - (start_x - normal_x) * 4.1)
x2 = int(start_x + (start_x - normal_x) * 4.1)
y1 = int(start_y - (start_y - normal_y) * 18.5 / 11.5)
y2 = int(start_y + (start_y - normal_y) * 4.5 / 11.5)
print("窗口位置：(", x1, ",", y1, "),(", x2, ",", y2, ")")
boxes, txts = ocr_detection()
MARKET_X = int(x1 + (x2 - x1) / 12)
CHARACTER_X = int(x1 + 3 * (x2 - x1) / 12)
FIGHT_X = int(x1 + 5 * (x2 - x1) / 12)
CORE_X = int(x1 + 7 * (x2 - x1) / 12)
BASE_X = int(x1 + 9 * (x2 - x1) / 12)
LEGION_X = int(x1 + 11 * (x2 - x1) / 12)
MAIN_PAGE_Y = int(y2 - (x2 - x1) / 12)
time.sleep(2)

MARKET = 1
CHARACTER = 2
FIGHT = 3
FIGHTING = 30
PATROL_CAR = 31
CORE = 4
BASE = 5
LEGION = 6
ADVERTISE = 7
REWARD = 8

main_state = -1
car_state = 0
chest_state = 0
energy_state = 0
auto_mode = 0

task_free_chest = 1
task_patrol_car = 1
task_gain_strength = 0

while 1:
    while 1:
        boxes, txts = ocr_detection()
        x, y = find_text(boxes, txts, "开始游戏")
        if x > 0 and y > 0:
            page = FIGHT
            break
        x, y = find_text(boxes, txts, "普通宝箱")
        if x > 0 and y > 0:
            page = MARKET
            break
        x, y = find_text(boxes, txts, "研究所")
        if x > 0 and y > 0:
            page = BASE
            break
        x, y = find_text(boxes, txts, "章节越高，收益越大")
        if x > 0 and y > 0:
            page = PATROL_CAR
            break
        x, y = find_text(boxes, txts, "广告")
        if x > 0 and y > 0:
            x, y = find_text(boxes, txts, "获得奖励")
            if x > 0 and y > 0:
                page = ADVERTISE
                break
        x, y = find_text(boxes, txts, "恭喜获得")
        if x > 0 and y > 0:
            page = REWARD
            break
        x, y = find_text(boxes, txts, "选择技能")
        if x > 0 and y > 0:
            page = FIGHTING
            break
        x, y = find_text(boxes, txts, "精英掉落")
        if x > 0 and y > 0:
            page = FIGHTING
            break
        x, y = find_text(boxes, txts, "总伤害")
        if x > 0 and y > 0:
            page = FIGHTING
            break
        print("无法识别页面")
        time.sleep(1)
    print("当前页面代号为：", page)

    if page == FIGHT:
        if task_free_chest == 1:
            click(MARKET_X, MAIN_PAGE_Y)
        elif task_patrol_car == 1:
            find_text_and_click(boxes, txts, "巡逻车", 0, 0)
        elif task_gain_strength == 1:
            click(BASE_X, MAIN_PAGE_Y)
        else:
            find_text_and_click(boxes, txts, "开始游戏", 0, 0)
    elif page == FIGHTING:
        find_text_and_click(boxes, txts, "子弹爆炸", 0, 0)
        find_text_and_click(boxes, txts, "连发", 0, 0)
        find_text_and_click(boxes, txts, "齐射", 0, 0)
        find_text_and_click(boxes, txts, "子弹穿透", 0, 0)
        find_text_and_click(boxes, txts, "聚焦", 0, 0)
        find_text_and_click(boxes, txts, "焦点引爆", 0, 0)
        find_text_and_click(boxes, txts, "功率增幅", 0, 0)
        find_text_and_click(boxes, txts, "军备强化", 0, 0)
        find_text_and_click(boxes, txts, "闪击射线", 0, 0)
        find_text_and_click(boxes, txts, "连续出击", 0, 0)
        find_text_and_click(boxes, txts, "爆炸扩散", 0, 0)
        find_text_and_click(boxes, txts, "选择技能", 0, 200)
        # other
        find_text_and_click(boxes, txts, "精英掉落", 0, 0)
        find_text_and_click(boxes, txts, "双倍奖励", 0, 0)
        find_text_and_click(boxes, txts, "返回", 0, 0)
    elif page == MARKET:
        if task_free_chest == 1:
            x, y = find_text(boxes, txts, "免费")
            if x > 0 and y > 0:
                click(x, y)
            else:
                task_free_chest = 0
                click(FIGHT_X, MAIN_PAGE_Y)
        else:
            click(FIGHT_X, MAIN_PAGE_Y)
    elif page == PATROL_CAR:
        if task_patrol_car == 1:
            x, y = find_text(boxes, txts, "暂无奖励")
            if x == -1 and y == -1:
                find_text_and_click(boxes, txts, "领取", 0, 0)
            else:
                x, y = find_text(boxes, txts, "0/3")
                if x > 0 and y > 0:
                    x, y = find_text(boxes, txts, "0/30")
                    if x == -1 and y == -1:
                        task_patrol_car = 0
                        click(int((x1 + x2) / 2), MAIN_PAGE_Y)
                else:
                    find_text_and_click(boxes, txts, "快速巡逻", 0, 0)
                    find_text_and_click(boxes, txts, "观看广告", 0, 0)
        else:
            click(int((x1 + x2) / 2), MAIN_PAGE_Y)
    elif page == ADVERTISE:
        x, y = find_text(boxes, txts, "已获得奖励")
        if x > 0 and y > 0:
            find_text_and_click(boxes, txts, "关闭", 0, 0)
        else:
            time.sleep(3)
    elif page == REWARD:
        click(int((x1 + x2) / 2), MAIN_PAGE_Y)
    else:
        print("未定义本页面操作")
        break

    # print(txts)
    # avoid broken
    # if find_text(boxes, txts, "恭喜获得") == 1:
    #    click((x1 + x2) / 2, (y1 + y2) / 4)
    # if find_text(boxes, txts, "广告") == 1:
    #    find_text_and_click(boxes, txts, "关闭", 0, 0)
    # if find_text(boxes, txts, "选择技能") == 1:
    #    main_state = 1
    # if find_text(boxes, txts, "X1.5") == 1:
    #    screenshot_and_click(boxes, txts, "X1.5", 0, 0)
    # start menu
    if main_state == 0:
        # 领取巡逻车收益
        if find_text(boxes, txts, "章节越高，收益越大") == 1:
            if find_text(boxes, txts, "暂无奖励") == 0:
                find_text_and_click(boxes, txts, "领取", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            elif find_text(boxes, txts, "快速巡逻") == 1 and find_text(boxes, txts, "0/3") == 0:
                find_text_and_click(boxes, txts, "快速巡逻", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            elif find_text(boxes, txts, "观看广告") == 1 and find_text(boxes, txts, "0/3") == 0:
                find_text_and_click(boxes, txts, "观看广告", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                find_text_and_click(boxes, txts, "关闭", 0, 0)
                time.sleep(3)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            else:
                find_text_and_click(boxes, txts, "快速巡逻", 0, 60)
                car_state = 1
        if car_state == 0:
            find_text_and_click(boxes, txts, "巡逻车", 0, 0)
        # 领取宝箱
        if car_state == 1 and chest_state == 0:
            while find_text(boxes, txts, "普通宝箱") == 0:
                click(47, 800)
                print("点击商城")
                time.sleep(1)
                boxes, txts = ocr_detection()
            while find_text(boxes, txts, "免费") == 1:
                find_text_and_click(boxes, txts, "免费", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "广告") == 1:
                    find_text_and_click(boxes, txts, "关闭", 0, 0)
                    boxes, txts = ocr_detection()
                time.sleep(2)
                click((x1 + x2) / 2, (y1 + y2) / 4)
            chest_state = 1
            boxes, txts = ocr_detection()
            find_text_and_click(boxes, txts, "战斗", 0, 0)
        # start fighting
        if car_state == 1 and chest_state == 1:
            # 确认体力充足
            boxes, txts = ocr_detection()
            find_text_and_click(boxes, txts, "开始游戏", 0, 0)
            time.sleep(1)
            boxes, txts = ocr_detection()
            if find_text(boxes, txts, "体力购买") == 1:
                time.sleep(1)
                click((x1 + x2) / 2, y2 - 50)
                time.sleep(1)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "食堂") == 0:
                    click((x1 + x2) * 3 / 4, 800)
                    print("点击基地")
                    boxes, txts = ocr_detection()
                find_text_and_click(boxes, txts, "食堂", 0, -50)
                time.sleep(1)
                boxes, txts = ocr_detection()
                while find_text(boxes, txts, "领取") == 0:
                    print(txts)
                    find_text_and_click(boxes, txts, "食堂", 0, -50)
                    boxes, txts = ocr_detection()
                find_text_and_click(boxes, txts, "领取", 0, 0)
                time.sleep(1)
                click((x1 + x2) / 2, y2 - 50)
                print("点击空白退出")
                time.sleep(1)
                click(47, 800)
                print("返回")
                time.sleep(1)
                boxes, txts = ocr_detection()
                find_text_and_click(boxes, txts, "战斗", 0, 0)
            else:
                main_state = 1
    # fighting
    elif main_state == 1:
        time.sleep(1)
        if auto_mode == 0:
            find_text_and_click(boxes, txts, "开始游戏", 0, 0)
            if find_text(boxes, txts, "选择技能") == 1:
                find_text_and_click(boxes, txts, "子弹爆炸", 0, 0)
                find_text_and_click(boxes, txts, "连发", 0, 0)
                find_text_and_click(boxes, txts, "齐射", 0, 0)
                find_text_and_click(boxes, txts, "子弹穿透", 0, 0)
                find_text_and_click(boxes, txts, "聚焦", 0, 0)
                find_text_and_click(boxes, txts, "焦点引爆", 0, 0)
                find_text_and_click(boxes, txts, "功率增幅", 0, 0)
                find_text_and_click(boxes, txts, "军备强化", 0, 0)
                find_text_and_click(boxes, txts, "闪击射线", 0, 0)
                find_text_and_click(boxes, txts, "连续出击", 0, 0)
                find_text_and_click(boxes, txts, "爆炸扩散", 0, 0)
                find_text_and_click(boxes, txts, "选择技能", 0, 150)
            find_text_and_click(boxes, txts, "精英掉落", 0, 0)
            if find_text(boxes, txts, "双倍奖励") == 1:
                find_text_and_click(boxes, txts, "双倍奖励", 0, 0)
                time.sleep(35)
                boxes, txts = ocr_detection()
                find_text_and_click(boxes, txts, "关闭", 0, 0)
            find_text_and_click(boxes, txts, "返回", 0, 0)
        elif auto_mode == 1:
            find_text_and_click(boxes, txts, "选择技能", 0, 150)
            find_text_and_click(boxes, txts, "返回", 0, 0)
        elif auto_mode == 2:
            find_text_and_click(boxes, txts, "选择技能", 0, 150)
            find_text_and_click(boxes, txts, "返回", 0, 0)
        else:
            print("error")

    # time.sleep(1)
