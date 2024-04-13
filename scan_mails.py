import os
from email import policy
from email.parser import BytesParser
from docx import Document
from io import BytesIO
from pdfminer.high_level import extract_text
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

# Путь к папке с .eml файлами
folder_path = "C:\\SmallMailBox"
def process_file(filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    print('Тема письма:', msg['Subject'])
    print('Отправитель:', msg['From'])
    print('Получатель:', msg['To'])
    print('Дата и время:', msg['Date'])
    print('Путь к файлу: ', file_path)

    # Проверьте, есть ли текстовое тело
    if msg.get_body(preferencelist=('plain',)):
        print('Содержимое письма (текст):', msg.get_body(preferencelist=('plain',)).get_content())
    else:
        print('Содержимое письма (текст): *Пусто*')

    attachments = check_all_attachments(msg)
    with ThreadPoolExecutor() as executor:
        futures = []
        if '.pdf' in attachments:
            futures.append(executor.submit(check_pdf_attachment, msg))
        if '.txt' in attachments:
            futures.append(executor.submit(check_txt_attachment, msg))
        if '.docx' in attachments:
            futures.append(executor.submit(check_docx_attachment, msg))
        for future in futures:
            future.result()

    print('\n-----------END OF THE FILE--------------\n')

def check_docx_attachment(msg):
    for part in msg.iter_parts():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        attachment = part.get_payload(decode=True)
        if attachment is None:
            continue
        if part.get_filename() and part.get_filename().endswith('.docx'):
            doc = Document(BytesIO(attachment))
            full_text = '\n'.join([para.text for para in doc.paragraphs])
            print("Название '.docx' файла: ", part.get_filename())
            print("Содержимое '.docx' файла: ", full_text)

def check_txt_attachment(msg):
    for part in msg.iter_parts():
        if part.get_filename() and part.get_filename().endswith('.txt'):
            print(f"Название '.txt' файла: {part.get_filename()}")
            print(f"Содержимое '.txt' файла: {part.get_content().decode('utf-16')}")

def check_pdf_attachment(msg):
    for part in msg.iter_parts():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        attachment = part.get_payload(decode=True)
        if attachment is None:
            continue
        if part.get_filename() and part.get_filename().endswith('.pdf'):
            full_text = extract_text(BytesIO(attachment))
            print(f"Название '.pdf' файла: {part.get_filename()}")
            print(f"Содержимое '.pdf' файла: {full_text}")

def check_all_attachments(msg):
    attachments = []
    for part in msg.iter_parts():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        attachment = part.get_payload(decode=True)
        if attachment is None:
            continue
        if part.get_filename():
            attachments.append(os.path.splitext(part.get_filename())[1])
    return attachments

def emails_input():

    # Get a list of all .eml files in the specified folder
    files = [filename for filename in os.listdir(folder_path) if filename.endswith('.eml')]

    # Create a multiprocessing Pool
    with Pool() as p:
        p.map(process_file, files)

if __name__ == '__main__':
    emails_input()
