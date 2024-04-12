import os
from email import policy
from email.parser import BytesParser

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

            # print('Тема письма:', msg['Subject'])
            # print('Отправитель:', msg['From'])
            # print('Получатель:', msg['To'])
            # print('Дата и время:', msg['Date'])
            # print('Номер: ',eml_count)
            # print('Путь к файлу: ',file_path)


            # # Проверьте, есть ли текстовое тело
            # if msg.get_body(preferencelist=('plain',)):
            #     print('Содержимое письма (текст):', msg.get_body(preferencelist=('plain',)).get_content())
            # else:
            #     print('Содержимое письма (текст): *Пусто*')
            #
            # check_txt_attachment(file_path)
            #
            # print('\n-----------END OF THE FILE--------------\n')


def check_txt_attachment(eml_file):
    with open(eml_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    for part in msg.iter_parts():
        if part.get_filename() and part.get_filename().endswith('.txt'):
            # print(f"Название '.txt' файла: {part.get_filename()}")
            # print(f"Содержимое файла: {part.get_content().decode('utf-16')}")
            break

emails_input()