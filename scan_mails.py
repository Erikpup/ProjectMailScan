import asyncio
import aiofiles
import os
from email import policy
from email.parser import BytesParser
from pdfminer.high_level import extract_text
from docx import Document
from io import BytesIO
import time
import ctypes

start_time = time.time()
pattern = {
    1: "\\b\\d{4} \\d{4} \\d{4} \\d{4}\\b|\\d{4} \\d{4} \\d{4} \\d{4}(?!\\d)|\\d{16}$(?!\\d)|^d{16}\\$",
    2:  "\\b\\d{20}\\b|\\d{20}(?!\\d)"
    }
def c_analys(text, pattern, file_path, type_file):
    dll_module = ctypes.CDLL('./Dll1.dll')
    dll_module.leakDetection.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    dll_module.leakDetection.restype = ctypes.c_bool
    for key, info in pattern.items():
        if dll_module.leakDetection(text.encode("utf-8"), info.encode("utf-8")):
            print(f"Done {file_path}  |  {type_file}  |  {pattern[key]}  |")
            return 1
    return 0


async def read_file(file_path):
    async with aiofiles.open(file_path, mode='rb') as f:
        content = await f.read()
    return content

async def process_eml(file_path, pattern):
    content = await read_file(file_path)
    msg = BytesParser(policy=policy.default).parsebytes(content)

    # print(f"Информация о файле {file_path}:")
    # print(f"Отправитель: {msg['From']}")
    # print(f"Получатель: {msg['To']}")
    # print(f"Дата и время: {msg['Date']}")
    # print(f"Заголовок: {msg['Subject']}\n")

    body = msg.get_body(preferencelist=('plain'))
    if body is not None:
        # print(f"Текст из файла {file_path}:")
        # print(body.get_content())
        c_analys(body.get_content(), pattern, file_path, 'text')

    for part in msg.iter_parts():
        await check_pdf_attachment(msg, part, file_path, pattern)
        await check_docx_attachment(msg, part, file_path, pattern)
        await check_txt_attachment(msg, part, file_path, pattern)

async def check_docx_attachment(msg, part, file_path, pattern):
    if part.get_content_maintype() == 'multipart':
        return
    if part.get('Content-Disposition') is None:
        return
    attachment = part.get_payload(decode=True)
    if attachment is None:
        return
    if part.get_filename() and part.get_filename().endswith('.docx'):
        doc = Document(BytesIO(attachment))
        text = '\n'.join([para.text for para in doc.paragraphs])
        c_analys(text, pattern, file_path, '.docx')
        #print("Название '.docx' файла: ", part.get_filename())
        #print("Содержимое '.docx' файла: ", full_text)

async def check_txt_attachment(msg, part, file_path, pattern):
    if part.get_filename() and part.get_filename().endswith('.txt'):
        #print(f"Название '.txt' файла: {part.get_filename()}")
        #print(f"Содержимое '.txt' файла: {part.get_content().decode('utf-16')}")
        c_analys(part.get_content().decode('utf-16'), pattern, file_path, '.txt')

async def check_pdf_attachment(msg, part, file_path, pattern):
    if part.get_content_maintype() == 'multipart':
        return
    if part.get('Content-Disposition') is None:
        return
    attachment = part.get_payload(decode=True)
    if attachment is None:
        return
    if part.get_filename() and part.get_filename().endswith('.pdf'):
        text = extract_text(BytesIO(attachment))
        c_analys(text, pattern, file_path, '.pdf')
        #print(f"Название '.pdf' файла: {part.get_filename()}")
        #print(f"Содержимое '.pdf' файла: {full_text}")

async def process_directory(dir_path, pattern):
    tasks = []
    for file in os.listdir(dir_path):
        if file.endswith(".eml"):
            task = asyncio.create_task(process_eml(os.path.join(dir_path, file), pattern))
            tasks.append(task)
    await asyncio.gather(*tasks)

# Запуск обработки директории
dir_path = "C:\\Users\\Loque\\Desktop\\Samples\\card"
asyncio.run(process_directory(dir_path, pattern))
end_time = time.time()
execution_time = end_time - start_time

print(f"Время выполнения программы: {execution_time/60} минут")