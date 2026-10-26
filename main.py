import zipfile
import re
import os

def extract_images_from_hwpx(hwpx_file_path, output_dir='images'):
    """
    HWPX 파일에서 모든 이미지를 추출하여 지정된 폴더에 저장합니다.

    :param hwpx_file_path: HWPX 파일의 경로
    :param output_dir: 이미지를 저장할 폴더명
    """
    # HWPX 파일이 존재하는지 확인
    if not os.path.exists(hwpx_file_path):
        print(f"오류: '{hwpx_file_path}' 파일을 찾을 수 없습니다.")
        return

    # 출력 폴더 생성 (이미 폴더가 있어도 오류 발생 안 함)
    os.makedirs(output_dir, exist_ok=True)

    print(f"'{hwpx_file_path}' 파일에서 이미지 추출을 시작합니다...")

    try:
        # HWPX 파일을 ZIP으로 열기
        with zipfile.ZipFile(hwpx_file_path, 'r') as hwp_zip:
            
            # ZIP 파일 내의 모든 파일 목록 가져오기
            file_list = hwp_zip.namelist()
            
            # BinData 폴더에 있는 이미지 파일만 필터링
            # 이미지 확장자: png, jpg, jpeg, gif, bmp 등
            image_files = [
                f for f in file_list 
                if f.startswith('BinData/') and re.search(r'\.(png|jpg|jpeg|gif|bmp)$', f, re.IGNORECASE)
            ]

            if not image_files:
                print("파일에서 추출할 이미지를 찾지 못했습니다.")
                return

            # 이미지 추출 및 저장
            image_count = 0
            for image_file in sorted(image_files): # 파일명 순으로 정렬하여 순서를 보장
                image_count += 1
                
                # 원본 파일의 확장자 가져오기
                _, extension = os.path.splitext(image_file)
                
                # 새 파일명 생성 (페이지 번호 대신 순번 사용)
                # 예: 추출_이미지_1.png, 추출_이미지_2.jpg
                new_filename = f"추출_이미지_{image_count}{extension}"
                output_path = os.path.join(output_dir, new_filename)
                
                # 이미지 데이터 읽기
                image_data = hwp_zip.read(image_file)
                
                # 새 파일로 저장
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"  - '{image_file}' -> '{output_path}' 저장 완료")

        print(f"\n총 {image_count}개의 이미지를 '{output_dir}' 폴더에 성공적으로 추출했습니다.")

    except zipfile.BadZipFile:
        print(f"오류: '{hwpx_file_path}' 파일은 유효한 HWPX(ZIP) 파일이 아닙니다.")
    except Exception as e:
        print(f"이미지 추출 중 오류가 발생했습니다: {e}")

# --- 실행 부분 ---
if __name__ == '__main__':
    # 여기에 HWPX 파일의 실제 경로를 입력하세요.
    # 스크립트 파일과 guide_book 폴더가 같은 위치에 있다고 가정합니다.
    hwp_file = os.path.join('data', '스마트 건설기술 가이드북 ver13.hwpx')
    
    # 이미지 추출 함수 호출
    extract_images_from_hwpx(hwp_file)