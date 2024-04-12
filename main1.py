import os
from email import policy
from email.parser import BytesParser
from docx import Document
import io

# Путь к папке с .eml файлами
folder_path = "C:\\SmallMailBox"

def emails_input():
    # Счётчик для файлов .eml
    eml_count = 0

    # Обход всех .eml файлов в указанной папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.eml'):
            eml_count += 1
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)

            print('Тема письма:', msg['Subject'])
            print('Отправитель:', msg['From'])
            print('Получатель:', msg['To'])
            print('Дата и время:', msg['Date'])
            print('Номер: ',eml_count)
            print('Путь к файлу: ',file_path)
            # Проверьте, есть ли текстовое тело
            if msg.get_body(preferencelist=('plain',)):
                print('Содержимое письма (текст):', msg.get_body(preferencelist=('plain',)).get_content())
            else:
                print('Содержимое письма (текст): *Пусто*')

            check_txt_attachment(file_path)
            check_word_attachment(file_path)

            print('\n-----------END OF THE FILE--------------\n')

def check_word_attachment(eml_file):
    if os.path.exists(eml_file):
        with open(eml_file, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        for part in msg.iter_parts():
            if part.get_filename() and part.get_filename().endswith('.docx'):
                print(f"Название '.docx' файла: {part.get_filename()}")
                doc_content = part.get_content()
                document = Document(io.BytesIO(doc_content))
                doc_text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
                print(f"Содержимое '.docx' файла: {doc_text}")
                break
    else:
        print("Файл не найден.")

def check_txt_attachment(eml_file):
    with open(eml_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    for part in msg.iter_parts():
        if part.get_filename() and part.get_filename().endswith('.txt'):
            print(f"Название '.txt' файла: {part.get_filename()}")
            print(f"Содержимое '.txt' файла: {part.get_content().decode('utf-16')}")
            break

emails_input()