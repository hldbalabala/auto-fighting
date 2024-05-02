import numpy as np
from skimage.metrics import structural_similarity
import cv2
import os


def resize(img_path):
    image = cv2.imread(img_path)

    # 获取图像的高度和宽度
    height, width = image.shape[:2]

    # 计算剪裁区域的左上角坐标
    start_x = (width - 120) // 2
    start_y = (height - 90) // 2

    # 剪裁图像
    cropped_image = image[start_y:start_y + 90, start_x:start_x + 120]
    return cropped_image


def init_compare():
    paths = []
    name_map = {}
    data_dir = "data"
    for idx, file_name in enumerate(os.listdir(data_dir)):
        if file_name.endswith('.png'):
            file_path = os.path.join(data_dir, file_name)
            paths.append(file_path)
            name_map[idx] = file_name[:-4]
    return paths, name_map


def compare_img(paths, name_map, img_path):
    results = []
    img1 = resize(img_path)
    for path in paths:
        img2 = resize(path)
        results.append(structural_similarity(img1, img2, multichannel=True))
    return name_map[np.argmax(results)]


if __name__ == '__main__':
    paths, name_map = init_compare()
    results = compare_img(paths, name_map, "data/ice.png")
    print(results)
