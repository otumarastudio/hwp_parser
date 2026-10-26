import os
import zipfile

def unzip_hwpx(hwpx_file_path, output_dir):
    """
    HWPX 파일의 압축을 지정된 폴더에 해제합니다.

    :param hwpx_file_path: HWPX 파일의 경로
    :param output_dir: 압축 해제된 파일들을 저장할 폴더명
    """
    # HWPX 파일이 존재하는지 확인
    if not os.path.exists(hwpx_file_path):
        print(f"오류: '{hwpx_file_path}' 파일을 찾을 수 없습니다.")
        return

    # 출력 폴더 생성 (이미 폴더가 있어도 오류 발생 안 함)
    os.makedirs(output_dir, exist_ok=True)

    print(f"'{hwpx_file_path}' 파일의 압축 해제를 시작합니다...")
    print(f"대상 폴더: '{output_dir}'")

    try:
        # HWPX 파일을 ZIP으로 열고 모든 내용을 지정된 폴더에 압축 해제
        with zipfile.ZipFile(hwpx_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        print(f"\n'{output_dir}' 폴더에 모든 파일을 성공적으로 압축 해제했습니다.")
        print("이제 폴더에서 파일 구조를 확인해 보세요.")

    except zipfile.BadZipFile:
        print(f"오류: '{hwpx_file_path}' 파일은 유효한 HWPX(ZIP) 파일이 아닙니다.")
    except Exception as e:
        print(f"압축 해제 중 오류가 발생했습니다: {e}")

# --- 실행 부분 ---
if __name__ == '__main__':
    # HWPX 파일 경로 설정
    hwp_file = os.path.join('data', '스마트 건설기술 가이드북 ver13.hwpx')
    
    # 압축 해제할 폴더명 설정
    extract_folder = 'unzipped_hwpx_contents'
    
    # 압축 해제 함수 호출
    unzip_hwpx(hwp_file, extract_folder)