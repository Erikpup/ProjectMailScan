import asyncio
import aiofiles
import os
from email import policy
from email.parser import BytesParser
from pdfminer.high_level import extract_text
from docx import Document
from io import BytesIO
import time
start_time = time.time()
async def read_file(file_path):
    async with aiofiles.open(file_path, mode='rb') as f:
        content = await f.read()
    return content

async def process_eml(file_path):
    content = await read_file(file_path)
    msg = BytesParser(policy=policy.default).parsebytes(content)

    print(f"Информация о файле {file_path}:")
    print(f"Отправитель: {msg['From']}")
    print(f"Получатель: {msg['To']}")
    print(f"Дата и время: {msg['Date']}")
    print(f"Заголовок: {msg['Subject']}\n")

    body = msg.get_body(preferencelist=('plain'))
    if body is not None:
        print(f"Текст из файла {file_path}:")
        print(body.get_content())

    for part in msg.iter_parts():
        content_type = part.get_content_type()
        if part.get_filename() and part.get_filename().endswith('.pdf'):
            attachment = part.get_content()
            full_text = extract_text(BytesIO(attachment))
            print(f"Название '.pdf' файла: {part.get_filename()}")
            print(f"Содержимое '.pdf' файла: {full_text}")
        if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Обработка DOCX вложений
            doc = Document(BytesIO(part.get_content()))
            text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
            print(f"\nТекст из DOCX вложения в файле {file_path}:")
            print(text)
        if content_type == "text/plain":
            # Обработка TXT вложений
            print(f"\nТекст из TXT вложения в файле {file_path}:")
            print(part.get_content())

async def process_directory(dir_path):
    tasks = []
    for file in os.listdir(dir_path):
        if file.endswith(".eml"):
            task = asyncio.ensure_future(process_eml(os.path.join(dir_path, file)))
            tasks.append(task)
    await asyncio.gather(*tasks)

# Запуск обработки директории
dir_path = "C:\\SmallMailBox"
asyncio.run(process_directory(dir_path))
end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time} секунд")