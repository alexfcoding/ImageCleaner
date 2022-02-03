# Example: python image_hash.py -i images/input_images -o images/similar_images -s 16 -t 33

import cv2
import os
from pathlib import Path
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input_folder", type=str, required=True,
                help="folder to clean similar images")
ap.add_argument("-o", "--similar_images", type=str, required=True,
                help="folder to move similar images")
ap.add_argument("-s", "--hash_size", type=int, default=16,
                help="hash size")
ap.add_argument("-t", "--threshold", type=int, required=True,
                help="threshold for detecting similar images")

args = vars(ap.parse_args())


def calculate_mean(pixels_list):
    mean = 0
    total_pixels = len(pixels_list)
    for i in range(total_pixels):
        mean += pixels_list[i] / total_pixels
    return mean


def grab_pixels(squeezed_frame):
    pixels_list = []
    for x in range(0, squeezed_frame.shape[1], 1):
        for y in range(0, squeezed_frame.shape[0], 1):
            pixel_color = squeezed_frame[x, y]
            pixels_list.append(pixel_color)
    return pixels_list


def make_bits_list(mean, pixels_list):
    bits_list = []
    for i in range(len(pixels_list)):
        if pixels_list[i] >= mean:
            bits_list.append(255)
        else:
            bits_list.append(0)
    return bits_list


def hashify(squeezed_frame, bits_list):
    bit_index = 0
    hashed_frame = squeezed_frame
    for x in range(0, squeezed_frame.shape[1], 1):
        for y in range(0, squeezed_frame.shape[0], 1):
            hashed_frame[x, y] = bits_list[bit_index]
            bit_index += 1
    return hashed_frame


def hash_generator_animation(frame, hash_size, iterations):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(f"static/test.avi", fourcc, 25, (frame.shape[1] * 2, frame.shape[0]), True)

    for i in range(iterations):
        if hash_size >= 16:
            frame_squeezed = cv2.resize(frame, (hash_size, hash_size))
            frame_squeezed = cv2.cvtColor(frame_squeezed, cv2.COLOR_BGR2GRAY)
            pixels_list = grab_pixels(frame_squeezed)
            mean_color = calculate_mean(pixels_list)
            bits_list = make_bits_list(mean_color, pixels_list)
            hashed_frame = hashify(frame_squeezed, bits_list)
            hashed_frame = cv2.cvtColor(hashed_frame, cv2.COLOR_GRAY2BGR)
            cv2.putText(hashed_frame, f"hash_size: {hash_size}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4,
                        lineType=cv2.LINE_AA)
            im_v = cv2.hconcat([frame, hashed_frame])
            cv2.imshow("Hash", im_v)
            cv2.waitKey(1)
            writer.write(im_v)
            hash_size -= 1


def generate_hash(frame, hash_size):
    frame_squeezed = cv2.resize(frame, (hash_size, hash_size))
    frame_squeezed = cv2.cvtColor(frame_squeezed, cv2.COLOR_BGR2GRAY)
    pixels_list = grab_pixels(frame_squeezed)
    mean_color = calculate_mean(pixels_list)
    bits_list = make_bits_list(mean_color, pixels_list)
    hashed_frame = hashify(frame_squeezed, bits_list)
    hashed_frame = cv2.cvtColor(hashed_frame, cv2.COLOR_GRAY2BGR)
    return bits_list, hashed_frame


def clean_folder(input_folder, similar_images, hash_size, threshold):
    files = (os.listdir(input_folder))
    list_length = len(files)
    i = 0
    k = 1
    frame = None
    hashed_frame = None
    duplicate_count = 0
    bits_list = []

    while i < len(files):
        sum_diff = 0

        if files[i] is not None:
            frame = cv2.imread(f"{input_folder}/{files[i]}")
            bits_list, hashed_frame = generate_hash(frame, hash_size)

        while k < len(files):
            if (i != k) and (files[k] is not None):
                new_frame = cv2.imread(f"{input_folder}/{files[k]}")
                new_bits_list, hashed_second_frame = generate_hash(new_frame, hash_size)

                for j in range(len(bits_list)):
                    if bits_list[j] != new_bits_list[j]:
                        sum_diff += 1

                print(f"{files[i]} -> {files[k]} sum_diff = {sum_diff}")

                im_h = cv2.hconcat([cv2.resize(frame, (450, 450)), cv2.resize(new_frame, (450, 450))])
                im_h2 = cv2.hconcat([cv2.resize(hashed_frame, (450, 450)), cv2.resize(hashed_second_frame, (450, 450))])
                im_v = cv2.vconcat([im_h, im_h2])

                if sum_diff <= hash_size * hash_size * threshold / 100:
                    Path(f"{input_folder}/{files[k]}").rename(f"{similar_images}/{files[k]}")
                    print(f"Deleted {k} element ({files[k]}) of {list_length}")
                    del files[k]
                    duplicate_count += 1
                else:
                    k += 1

                cv2.putText(im_v, f"SIMILAR: {duplicate_count}", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            lineType=cv2.LINE_AA)
                cv2.imshow("Seeking for similar images...", im_v)
                cv2.waitKey(1)
                sum_diff = 0
        i += 1
        k = i + 1


clean_folder(args['input_folder'], args['similar_images'], args['hash_size'], args['threshold'])
