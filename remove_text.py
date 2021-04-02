import cv2
import numpy as np
import os
from glob import glob
from google.cloud import vision
import io
from datetime import datetime
import sys

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
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 박스를 그리기 위해 cv 형태의 이미지 로드
    encoded_img = np.frombuffer(content, dtype=np.uint8)
    img_cv = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    # 0번 인덱스는 이미지의 최대 크기의 vertices를 갖고 있어서 미포함.
    # bounding box를 그리기 위해 필요한 것은 좌상, 우하의 좌표만 필요함.
    # v는 투플 형태로 (x, y) 좌표가 저장됨.
    # cv2.rectangle(img, pt1, pt2, color, thickness)
    # (0, 255, 0) -> Green
    # thickness = -1 : 박스 안을 채움.
    for text in texts[1:]:
        v = [(v.x, v.y) for v in text.bounding_poly.vertices]
        cv2.rectangle(img_cv, v[0], v[2], (0, 255, 0), -1)

    imwrite(output_path, img_cv)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


if __name__ == '__main__':

    # ROOT DIR
    base_dir = '[ROOT_PATH]'            # fill root path
    os.chdir(base_dir)

    # SUB_DIR
    sub_dir = glob('*')
    print(sub_dir)

    # Google API 호출
    client = vision.ImageAnnotatorClient()

    # 로그를 위한 숫자
    # cnt = 한 서브 디렉토리 내의 비식별화 완료 개수를 세기 위한 변수
    # total = 총 이미지 개수
    # start = running time 계산을 위한 시작시간
    cnt = 0
    total = 0
    start = datetime.now()

    # 각 디렉토리를 순회
    for dir in sub_dir:
        # images = dir 내 들어있는 모든 이미지 주소
        # ex) D:/data 폴더에 결함별로 이미지가 분류되어 있을 경우.
        #       ROOT DIR = 'D:/data'
        #       SUB_DIR = ['D:/data/균열', 'D:/data/파손']
        #       images = '균열' 폴더에 있는 모든 이미지

        images = glob(dir + '/*')
        print(dir)

        # 저장할 dir 주소
        # 해당 폴더가 없으면 만듦
        output_dir = os.path.join('[OUTPUT_PATH]', dir)            # fill output path
        os.makedirs(output_dir, exist_ok=True)

        # 해당 dir 안의 모든 이미지를 차례로 순회
        for x in images:

            file_name = os.path.basename(x)
            output_path = os.path.join(output_dir, file_name)
            total += 1
            cnt += 1
            # 만약, 코드 실행 중 중단될 경우 다시 코드를 실행했을 때,
            # 이미 비식별화가 진행된 파일은 output_path 에 파일이 존재할 것이므로
            # output_path 가 존재한다면, 로그를 남기고, continue
            if os.path.isfile(output_path):
                sys.stdout.write("\r{} / {}".format(cnt, len(images)))
                continue
            # 비식별화 함수
            detect_text(x)

            # 진행상황 로그
            sys.stdout.write("\r{} / {}".format(cnt, len(images)))

        # 해당 디렉토리의 경과시간 로그
        print('\n', dir, '\t\tElapsed Time: ', datetime.now() - start)

        # 카운팅 초기화
        cnt = 0

    # 총 경과시간을 알기 위해 실행이 끝났을 때의 시간을 저장한 변수
    end = datetime.now()

    print("\n\n%d images Done!!" % total)
    print("Total Elapsed Time: ", end - start)