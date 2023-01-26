import cv2
import numpy as np
import matplotlib.pyplot as plt


def draw_center(image, center, radius=20, color=(0, 0, 255)):
    image = cv2.circle(
        image, (int(center[0]), int(center[1])), radius, color, -1)
    image = cv2.putText(image, 'Center ({}, {})'.format(center[0], center[1]), (
        center[0] + 20, center[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
    return image


def draw_line(image, rho, theta, color=(0, 0, 255), width=4):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 10000 * (-b))
    y1 = int(y0 + 10000 * (a))
    x2 = int(x0 - 10000 * (-b))
    y2 = int(y0 - 10000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), color, width)
    return image


def draw_main_axis(image, center, theta, color=(0, 0, 255)):
    rho = center[1] * np.cos(theta) - center[0] * \
        np.sin(theta)  # main axis goes through center
    new_theta = theta + np.pi / 2
    image = draw_line(image, rho, new_theta, color)
    return image


def draw_text(image, content, pos, color=(0, 255, 255)):
    image = cv2.putText(image, content, pos,
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
    return image


def show_image(title, image, gray=True):
    if gray:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.axis('off')
    plt.title(title)


def draw_process(process, save_path):
    plt.figure(figsize=(32, 16))

    # 1. Origin image
    plt.subplot(3, 4, 1)
    show_image("1. Original image", process[0], False)

    # 2. Gray image
    plt.subplot(3, 4, 2)
    show_image("2. To gray", process[1], True)

    # 3. Binary image
    plt.subplot(3, 4, 3)
    show_image("3. To binary", process[2], True)

    # 4. Opening
    plt.subplot(3, 4, 4)
    show_image("4. Opening", process[3], True)

    # 5. Closing
    plt.subplot(3, 4, 5)
    show_image("5. Closing", process[4], True)

    # 6. Label connected components
    plt.subplot(3, 4, 6)
    show_image("6. Labelling", process[5], False)

    # 7. Filter labelled components
    plt.subplot(3, 4, 7)
    show_image("7. Filter labels", process[6], False)

    # 8. Detect edge side 1
    plt.subplot(3, 4, 8)
    show_image("8. Edge side 1", process[7], True)

    # 9. Detect edge side 2
    plt.subplot(3, 4, 9)
    show_image("9. Edge side 2", process[8], True)

    # 10. Smooth main
    plt.subplot(3, 4, 10)
    show_image("10. Smooth main", process[9], True)

    # 11. Main axis
    plt.subplot(3, 4, 11)
    show_image("11. Main axis", process[10], True)

    # 12. Final result
    plt.subplot(3, 4, 12)
    show_image("12. Final result", process[11], False)

    # Save result
    plt.tight_layout()
    plt.savefig(save_path)
    print('==> Save process to {}!'.format(save_path))
