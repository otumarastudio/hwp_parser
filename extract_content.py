import os
import xml.etree.ElementTree as ET
import json

def parse_hwpx_tables(xml_file_path):
    """
    HWPX의 section.xml 파일에서 표(table)를 찾아 내용을 추출하고 구조화합니다.
    """
    if not os.path.exists(xml_file_path):
        print(f"오류: '{xml_file_path}' 파일을 찾을 수 없습니다.")
        return

    print(f"'{xml_file_path}' 파일 분석을 시작합니다...\n")

    try:
        # XML 파일 파싱
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # OWPML은 네임스페이스(namespace)를 사용하므로 꼭 지정해야 합니다.
        # XML 태그 앞부분에 붙는 {http://www.hancom.co.kr/xml/hwpml} 같은 긴 이름입니다.
        namespaces = {
            'h': 'http://www.hancom.co.kr/xml/hwpml'
        }

        # 문서 내의 모든 표(tbl)를 찾습니다.
        tables = root.findall('.//h:tbl', namespaces)
        
        if not tables:
            print("문서에서 표를 찾지 못했습니다.")
            return

        print(f"총 {len(tables)}개의 표를 찾았습니다.")
        print("-" * 30)

        all_tables_data = []
        for i, table in enumerate(tables):
            print(f"\n[ 표 {i+1} 데이터 추출 ]")
            
            # 표의 헤더(첫 번째 행)를 추출
            header_row = table.find('h:tr', namespaces)
            if header_row is None:
                continue

            headers = ["".join(tc.itertext()).strip() for tc in header_row.findall('h:tc', namespaces)]
            
            table_data = []
            # 두 번째 행부터 데이터로 처리
            data_rows = table.findall('h:tr', namespaces)[1:]

            for row in data_rows:
                cells = row.findall('h:tc', namespaces)
                row_data = [("".join(tc.itertext()).strip()) for tc in cells]
                
                # 열 병합(colspan) 등으로 인해 셀 개수가 헤더와 맞지 않는 경우를 대비
                # 여기서는 간단히 헤더의 수에 맞춰 데이터를 채웁니다.
                row_dict = dict(zip(headers[:len(row_data)], row_data))
                table_data.append(row_dict)

            all_tables_data.append(table_data)
            
            # 추출된 데이터 출력 (가독성을 위해 JSON 형태로 예쁘게 출력)
            print(json.dumps(table_data, indent=2, ensure_ascii=False))

        return all_tables_data

    except Exception as e:
        print(f"XML 파싱 중 오류가 발생했습니다: {e}")
        return None

# --- 실행 부분 ---
if __name__ == '__main__':
    # 압축 해제된 폴더 안의 section0.xml 파일 경로
    xml_file = os.path.join('unzipped_hwpx_contents', 'Contents', 'section0.xml')
    
    # 표 분석 함수 호출
    extracted_data = parse_hwpx_tables(xml_file)