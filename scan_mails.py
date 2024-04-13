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
        await check_pdf_attachment(msg, part)
        await check_docx_attachment(msg, part)
        await check_txt_attachment(msg, part)

async def check_docx_attachment(msg, part):
    if part.get_content_maintype() == 'multipart':
        return
    if part.get('Content-Disposition') is None:
        return
    attachment = part.get_payload(decode=True)
    if attachment is None:
        return
    if part.get_filename() and part.get_filename().endswith('.docx'):
        doc = Document(BytesIO(attachment))
        full_text = '\n'.join([para.text for para in doc.paragraphs])
        print("Название '.docx' файла: ", part.get_filename())
        print("Содержимое '.docx' файла: ", full_text)

async def check_txt_attachment(msg, part):
    if part.get_filename() and part.get_filename().endswith('.txt'):
        print(f"Название '.txt' файла: {part.get_filename()}")
        print(f"Содержимое '.txt' файла: {part.get_content().decode('utf-16')}")

async def check_pdf_attachment(msg, part):
    if part.get_content_maintype() == 'multipart':
        return
    if part.get('Content-Disposition') is None:
        return
    attachment = part.get_payload(decode=True)
    if attachment is None:
        return
    if part.get_filename() and part.get_filename().endswith('.pdf'):
        full_text = extract_text(BytesIO(attachment))
        print(f"Название '.pdf' файла: {part.get_filename()}")
        print(f"Содержимое '.pdf' файла: {full_text}")

async def process_directory(dir_path):
    tasks = []
    for file in os.listdir(dir_path):
        if file.endswith(".eml"):
            task = asyncio.create_task(process_eml(os.path.join(dir_path, file)))
            tasks.append(task)
    await asyncio.gather(*tasks)

# Запуск обработки директории
dir_path = "C:\\SmallMailBox"
asyncio.run(process_directory(dir_path))
end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time/60} минут")