

'''
Help taken from ChatGpt and internet for writing this code.
'''

'''
The code itself converts image to grayscale image. So any image can be used as input.
Place the image in the same directory as the code. The image format should be jpg and it should be named as 'image.jpg'.
The density file should should also be present in the same directory.
'''

import cv2
import csv

def convert_to_grayscale(input_image_path, output_image_path):
    try:
        image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
        if image is None:
            print("Error: Unable to load the image.")
            return
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(output_image_path, grayscale_image)
        print("Grayscale image saved successfully.")
    except Exception as e:
        print(f"Error: {e}")

def read_ascii_mapping(csv_file):
    ascii_mapping = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            density_of_dots, ascii_no, ascii_char = row
            ascii_mapping.append((int(density_of_dots), int(ascii_no), ascii_char))
    return ascii_mapping


def map_gray_to_ascii(gray_value, ascii_mapping):
    for density, ascii_no, ascii_char in ascii_mapping:
        if gray_value%200 <= density:
            return ascii_char
    return " "

def resize_image(input_image_path, new_width):
    try:
        image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
        if image is None:
            print("Error: Unable to load the image.")
            return
        original_height, original_width, _ = image.shape
        resize_ratio = new_width / original_width
        new_height = int(original_height * resize_ratio)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        return grayscale_image

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    input_image_path = "image.jpg"
    output_image_path = "grayscale_image.jpg"
    convert_to_grayscale(input_image_path, output_image_path)
    input_image_path = "grayscale_image.jpg"
    new_width = 100
    ascii_mapping = read_ascii_mapping("density.csv")
    resized_image = resize_image(input_image_path, new_width)
    if resized_image is not None:
        ascii_art = ""
        for row in resized_image:
            for gray_value in row:
                ascii_char = map_gray_to_ascii(gray_value, ascii_mapping)
                ascii_art += ascii_char
            ascii_art += "\n"
        print(ascii_art)