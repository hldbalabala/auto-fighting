from paddleocr import PaddleOCR
import pyautogui
import time


def ocr_detection(img_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="ch")
    result = ocr.ocr(img_path, cls=False)
    result = result[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # scores = [line[1][1] for line in result]
    return boxes, txts


def screenshot_and_click(boxes, txts, target, mode):
    for idx, txt in enumerate(txts):
        if txt == target:
            center_x = (boxes[idx][0][0] + boxes[idx][1][0]) / 2
            center_y = (boxes[idx][1][1] + boxes[idx][2][1]) / 2 + 150 * (mode == 1)
            pyautogui.click(x=center_x, y=center_y)
            print("目标{}已检测到，并在位置 ({}, {}) 处进行了点击操作。".format(target, center_x, center_y))
            break


x1, y1 = 0, 0
x2, y2 = 450, 850
while 1:
    desktop_image = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    desktop_image.save('screenshot.jpg', 'JPEG')
    boxes, txts = ocr_detection('screenshot.jpg')
    # print(txts)
    screenshot_and_click(boxes, txts, "开始游戏", 0)
    screenshot_and_click(boxes, txts, "选择技能", 1)
    screenshot_and_click(boxes, txts, "返回", 0)
    screenshot_and_click(boxes, txts, "点击空白处关闭", 0)
    #time.sleep(1)
