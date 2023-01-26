# Import libs
import os
import cv2
import numpy as np
import argparse
from pathlib import Path

from utils import edge_detector
from utils import to_degree, to_rad
from utils import draw_center, draw_line, draw_main_axis, draw_text, draw_process
from utils import get_theta, get_angle


def process_image(image_path, save_dir):
    image_name = image_path.split(os.path.sep)[-1]
    print("=== Processing image {} ===".format(image_name))

    process = []

    # 1. Read image and convert to gray image
    print('[1] Read image and convert to gray...')
    origin_image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
    process.extend([origin_image, gray_image])

    # 2. Convert image to binary
    print('[2] Convert to binarty...')
    binary_threshold = 176
    binary_image = cv2.threshold(
        gray_image, binary_threshold, 255, cv2.THRESH_BINARY)[1]
    process.append(binary_image)

    # 3. Open to remove noise, then close to join components
    print('[3] Open then close...')
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    process.append(opening)

    kernel = np.ones((25, 25), np.uint8)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    process.append(closing)

    # 4. Find and split connected components
    print('[4] Find connected components...')
    num_labels, labels_im = cv2.connectedComponents(closing)
    process.append(labels_im)

    # 5. Sort and filter labels
    print('[5] Sort and filter connected components...')

    def area(label):
        return np.sum(labels_im == label)

    sorted_labels = sorted(list(range(1, num_labels)), key=area, reverse=True)
    filtered_labels = sorted_labels[:3]  # Get top 3 labels with largest area
    filtered_label_im = labels_im.copy()
    for l in range(1, num_labels):
        if l not in filtered_labels:
            filtered_label_im = filtered_label_im - \
                (labels_im == l) * filtered_label_im
    process.append(filtered_label_im)

    # 6. Extract components
    print('[6] Extract connected components from origin image...')

    def extract_component(binary_im, label_im, label):
        return (label_im == label) * binary_im

    main_comp = extract_component(closing, labels_im, filtered_labels[0])
    side_comp_1 = extract_component(closing, labels_im, filtered_labels[1])
    side_comp_2 = extract_component(closing, labels_im, filtered_labels[2])

    # 7. Side components edge detection
    print('[7] Edge detection for side component...')
    hough_threshold = 30
    lines = edge_detector(side_comp_1, hough_threshold)
    rho_1, theta_1 = lines[0][0]
    process.append(draw_line(side_comp_1, rho_1, theta_1, (255, 255, 255), 2))

    lines = edge_detector(side_comp_2, hough_threshold)
    rho_2, theta_2 = lines[0][0]
    process.append(draw_line(side_comp_2, rho_2, theta_2, (255, 255, 255), 2))

    # 8. Smooth main component edge
    print('[8] Smoothen main component edge...')
    kernel = np.ones((15, 15), np.int8)
    main_comp = cv2.morphologyEx(main_comp, cv2.MORPH_OPEN, kernel)
    process.append(main_comp.copy())

    # 9. Main component orientation estimation
    print('[9] Estimate main component orientation...')
    _, center, theta_0 = get_theta(main_comp)
    process.append(draw_main_axis(main_comp, center, theta_0, (0, 0, 0)))

    # 10. Calculate angle
    print('[10] Calculate angle between components...')
    angle_1 = get_angle(theta_0, theta_1)
    angle_2 = get_angle(theta_0, theta_2)

    # 11. Draw results
    print('[11] Draw result...')
    image = origin_image.copy()
    image = draw_line(image, rho_1, theta_1, (0, 255, 0))
    image = draw_text(image, "Comp1: {:.2f}deg".format(
        to_degree(angle_1)), (20, 60), (0, 255, 0))
    image = draw_line(image, rho_2, theta_2, (255, 0, 0))
    image = draw_text(image, "Comp2: {:.2f}deg".format(
        to_degree(angle_2)), (20, 120), (255, 0, 0))
    image = draw_main_axis(image, center, theta_0, (0, 0, 255))
    image = draw_center(image, center, 15, (114, 66, 20))
    process.append(image.copy())

    # 12. Save result
    print('[12] Save result...')
    save_path = os.path.join(save_dir, image_name, 'result.jpg')
    Path(os.path.join(save_dir, image_name)).mkdir(parents=True, exist_ok=True)
    cv2.imwrite(save_path, image)
    print('==> Save result to {}!'.format(save_path))
    save_path = os.path.join(save_dir, image_name, 'process.jpg')
    draw_process(process, save_path)
    print()


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_dir', type=str,
                        default='./data', help='Path to image directory')
    parser.add_argument('--save_dir', type=str,
                        default='./save/results', help='Path to save dir')

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    for image_name in os.listdir(args.image_dir):
        image_path = os.path.join(args.image_dir, image_name)
        process_image(image_path, args.save_dir)


if __name__ == '__main__':
    main()
