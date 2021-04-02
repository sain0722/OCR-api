## 이미지 비식별화 (OCR) 코드 사용 방법

■ 선행사항

아래 블로그를 따라 Google OCR API를 사용하기 위한 준비를 마칩니다.  
https://blog.naver.com/nanotoly/222032083807 

1. 프로젝트 만들기
2. 결제 사용 설정
3. API 사용 설정
4. 서비스 계정 키 발급
5. PowerShell에서 환경 변수 설정
6. 구글 클라이언트 라이브러리 설치

## 코드 실행 프로세스

### 1. ROOT DIR을 설정

``` base_dir = '[ROOT PATH]' ```

디렉토리 구조는 다음과 같습니다.
```
root
├── sub1
│   ├── image_01.png
│   └── image_02.png
├── sub2
│   ├── image_01.png
│   └── image_02.png
└── sub3
    ├── image_01.png
    └── image_02.png
```

### 2. OUTPUT PATH를 설정

``` output_dir = '[OUTPUT PATH]' ```

### 3. 코드 실행

``` python remove_text.py ```

- argparse를 이용하여 인자를 넘길까 했지만, 파이참에서 바로 실행하는 것이 더 편리했어서 이 방법을 사용했었습니다.

## 추가 팁

이미지 한 장당 대략 3~5초 정도의 시간이 걸린다.  
이미지가 대량으로 있을 경우, 시간 단축을 위해 **역순**으로 한번 더 실행하여 시간을 단축시킬 수 있다.  

```for```문의 ```sub_dir ```을 뒤에서부터 읽도록 ```[::-1]```을 붙여서 **정방향으로 읽는 코드와 동시에 실행**시킨다.

```python
for dir in sub_dir[::-1]:
    images = glob(dir + '/*')
    print(dir)
    output_dir = '[PATH]'
    os.makedirs(output_dir, exist_ok=True)
    for x in images:
        fname = os.path.basename(x)
        output_path = os.path.join(output_dir, fname)
        total += 1
        cnt += 1
        if os.path.isfile(output_path):
            sys.stdout.write("\r{} / {}".format(cnt, len(images)))
            continue

        detect_text(x)
        sys.stdout.write("\r{} / {}".format(cnt, len(images)))

    print('\n', dir, '\t\tElapsed Time: ', datetime.now() - start)
    cnt = 0
```
