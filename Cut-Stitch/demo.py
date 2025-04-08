from PIL import Image
import random


def cut_stitch_unidirectional(image, direction='horizontal', ratio=0.05):
    """
    对图像进行单向(水平/竖直)Cut-Stitch操作，使用PIL处理。

    :param image: 输入图像(PIL.Image)
    :param ratio: 裁切比例(0～1之间)
    :param direction: 'horizontal' 或 'vertical'
    :return: 返回拼接后的图像
    """
    width, height = image.size
    if direction == 'horizontal':
        # 按照裁切率 ratio 计算裁剪宽度
        cut_size = int(ratio * width)
        if cut_size < 1:
            raise ValueError("裁切宽度过小，请增大 ratio 或使用更大图像。")

        strips = [image.crop((i * cut_size, 0, (i + 1) * cut_size, height)) for i in range(width // cut_size)]

        # 跳过拼接
        img1 = Image.new('RGB', (width, height))
        img2 = Image.new('RGB', (width, height))

        # 拼接 strips[::2] 和 strips[1::2]
        x_offset = 0
        for strip in strips[::2]:
            img1.paste(strip, (x_offset, 0))
            x_offset += strip.width

        x_offset = 0
        for strip in strips[1::2]:
            img2.paste(strip, (x_offset, 0))
            x_offset += strip.width

    elif direction == 'vertical':
        # 按照裁切率 ratio 计算裁剪高度
        cut_size = int(ratio * height)
        if cut_size < 1:
            raise ValueError("裁切高度过小，请增大 ratio 或使用更大图像。")

        strips = [image.crop((0, i * cut_size, width, (i + 1) * cut_size)) for i in range(height // cut_size)]

        img1 = Image.new('RGB', (width, height))
        img2 = Image.new('RGB', (width, height))

        # 拼接 strips[::2] 和 strips[1::2]
        y_offset = 0
        for strip in strips[::2]:
            img1.paste(strip, (0, y_offset))
            y_offset += strip.height

        y_offset = 0
        for strip in strips[1::2]:
            img2.paste(strip, (0, y_offset))
            y_offset += strip.height

    else:
        raise ValueError("direction 必须是 'horizontal' 或 'vertical'.")

    # 调整大小，使拼接后的图像和原图大小一致
    img1 = img1.resize((width, height), Image.LANCZOS)
    img2 = img2.resize((width, height), Image.LANCZOS)

    return random.choice([img1, img2])


def cut_stitch_bidirectional(image, ratio=0.05):
    """
    对图像进行双向(H+V 或 V+H)Cut-Stitch操作，使用PIL处理。

    :param image: 输入图像(PIL.Image)
    :param ratio: 裁切比例(0～1之间)
    :return: 返回拼接后的图像
    """
    # 先进行水平裁切
    horizontals_img = cut_stitch_unidirectional(image, ratio=ratio, direction='horizontal')
    final_img = cut_stitch_unidirectional(horizontals_img, ratio=ratio, direction='vertical')

    return final_img



# import random
#
# import cv2
# import numpy as np
# import os
#
#
# def cut_stitch_unidirectional(image, direction='horizontal', ratio=0.05):
#     """
#     对图像进行单向(水平/竖直)Cut-Stitch操作，
#     并返回2张分别使用“跳过拼接”得到的图像。
#
#     :param image: 输入图像(numpy数组, H×W×C)
#     :param ratio: 裁切比例(0～1之间)
#     :param direction: 'horizontal' 或 'vertical'
#     :return: [image1, image2], 共2张图像
#     """
#     h, w, c = image.shape
#     if direction == 'horizontal':
#         # 按照裁切率 ratio 计算裁剪宽度
#         cut_size = int(ratio * w)
#         if cut_size < 1:
#             raise ValueError("裁切宽度过小，请增大 ratio 或使用更大图像。")
#         # 计算可切出多少条
#         num_slices = w // cut_size
#
#         # 分割图像
#         strips = [image[:, i * cut_size:(i + 1) * cut_size]
#                   for i in range(num_slices)]
#
#         # 跳过拼接
#         # 例如 strips[::2] + strips[1::2]
#         # 生成两张图
#
#         img1 = np.hstack(strips[::2])
#         img2 = np.hstack(strips[1::2])
#
#     elif direction == 'vertical':
#         # 按照裁切率 ratio 计算裁剪高度
#         cut_size = int(ratio * h)
#         if cut_size < 1:
#             raise ValueError("裁切高度过小，请增大 ratio 或使用更大图像。")
#         num_slices = h // cut_size
#
#         strips = [image[i * cut_size:(i + 1) * cut_size, :]
#                   for i in range(num_slices)]
#
#         img1 = np.vstack(strips[::2])
#         img2 = np.vstack(strips[1::2])
#     else:
#         raise ValueError("direction 必须是 'horizontal' 或 'vertical'.")
#     img1 = cv2.resize(img1, (w, h), interpolation=cv2.INTER_LINEAR)
#     img2 = cv2.resize(img2, (w, h), interpolation=cv2.INTER_LINEAR)
#     return random.choice([img1, img2])
#
#
# def cut_stitch_bidirectional(image, ratio=0.05):
#     """
#     对图像进行双向(H+V 或 V+H)Cut-Stitch操作，
#     返回4张图像。
#     - 先在水平或竖直方向切割得到2张图
#     - 再对这2张图进行垂直或水平切割，各得到2张，共4张
#
#     注：本例中默认先水平再竖直，
#        也可按需求反过来先竖直再水平。
#     """
#     # 先进行水平裁切
#     horizontals_img = cut_stitch_unidirectional(image, ratio=ratio, direction='horizontal')
#     final_img = cut_stitch_unidirectional(horizontals_img, ratio=ratio, direction='vertical')
#
#     return final_img
