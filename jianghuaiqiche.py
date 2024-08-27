import fitz  # PyMuPDF
import pandas as pd
import json

def extract_tables_from_pdf(pdf_path):
    # 打开PDF文件
    document = fitz.open(pdf_path)
    tables = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text_page = page.get_text("text")
        tables_on_page = extract_tables_from_text(text_page)
        tables.extend(tables_on_page)

    return tables

def extract_tables_from_text(text_page):
    # 这里假设表格是以某种格式分隔的文本
    # 你可以根据实际情况调整这个函数
    lines = text_page.split('\n')
    tables = []
    table = []
    for line in lines:
        if line.strip():
            row = line.split()
            if table and len(row) != len(table[0]):
                continue  # 跳过列数不匹配的行
            table.append(row)
        else:
            if table:
                tables.append(table)
                table = []
    if table:
        tables.append(table)
    return tables

def convert_tables_to_json(tables):
    json_data = []
    for table in tables:
        if len(table) > 1:  # 确保表格至少有两行（表头和一行数据）
            df = pd.DataFrame(table[1:], columns=table[0])
            json_data.append(df.to_dict(orient='records'))
    return json.dumps(json_data, ensure_ascii=False, indent=4)

def main(pdf_path):
    tables = extract_tables_from_pdf(pdf_path)
    json_data = convert_tables_to_json(tables)
    print(json_data)

if __name__ == "__main__":
    pdf_path = "202408.pdf"  # 替换为你的PDF文件路径
    main(pdf_path)
