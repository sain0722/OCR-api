import cv2
import numpy as np
from google.cloud import vision
import io
from datetime import datetime
import argparse

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "[GOOGLE KEY]"

"""
    Google Cloud Platform, 
    Google Vision API(OCR) 사용
    https://cloud.google.com/vision/docs/ocr?hl=ko
"""


# 이미지 저장 함수, 수정부분 X
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


"""Detects text in the file."""


def detect_text(path):

    st = datetime.now()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 박스를 그리기 위해 cv 형태의 이미지 로드
    encoded_img = np.frombuffer(content, dtype=np.uint8)
    img_cv = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    # origin_img = img_cv.copy()
    # 0번 인덱스는 이미지의 최대 크기의 vertices를 갖고 있어서 미포함.
    # bounding box를 그리기 위해 필요한 것은 좌상, 우하의 좌표만 필요함.
    # v는 투플 형태로 (x, y) 좌표가 저장됨.
    # cv2.rectangle(img, pt1, pt2, color, thickness)
    # (0, 255, 0) -> Green
    # thickness = -1 : 박스 안을 채움.
    for text in texts[1:]:
        v = [(v.x, v.y) for v in text.bounding_poly.vertices]
        cv2.rectangle(img_cv, v[0], v[2], (0, 255, 0), -1)
    end = datetime.now()
    print("\nTotal Elapsed Time: ", end - st)
    imwrite(output_path, img_cv)
    # cv2.imshow('original image', origin_img)
    # cv2.imshow('result image', img_cv)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # 입력받을 인자값 등록
    parser.add_argument('-i', '--image_path', required=True, help='Write the file path')
    parser.add_argument('-f', '--folder_path')
    parser.add_argument('-o', '--one', type=bool, default=1)
    args = parser.parse_args()

    # Google API 호출
    client = vision.ImageAnnotatorClient()

    # 사용자에게 받은 파일 이름
    file_path = args.image_path
    print("FILE PATH:", file_path)

    file_name = os.path.basename(file_path)
    output_path = os.path.join(os.getcwd(), 'result_' + file_name)
    x = file_path

    # 비식별화 함수
    detect_text(x)

    print("\n\nimage De-Identification Done!!")
    print("\nSAVE PATH:", output_path)