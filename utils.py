import cv2
import numpy as np

def split_number(n):
    return {
        'units': n % 10,
        'tens': (n // 10) % 10,
        'hundreds': (n // 100) % 10,
        'thousands': (n // 1000) % 10
    }

def is_valid_number(n):
    return isinstance(n, int) and 1 <= n <= 9999

def draw_line(img, pt1, pt2, color=0, thickness=2):
    cv2.line(img, pt1, pt2, color, thickness)

def convert_cv_to_tk(img):
    from PIL import ImageTk, Image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(pil_img)

def normalize_and_resize(img, size=(200, 200)):
    norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    resized = cv2.resize(norm, size)
    return resized

def preprocess_for_recognition(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary
