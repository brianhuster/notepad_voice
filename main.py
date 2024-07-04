import speech_recognition as sr
import pyautogui as pag
import subprocess
import time
import os

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Đang nghe...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='vi-VN')
        print(f"Đã nghe thấy: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Xin lỗi, tôi không nghe rõ lời bạn nói.")
        return ""
    except sr.RequestError:
        print("Không thể kết nối với API nhận dạng giọng nói, vui lòng kiểm tra kết nối mạng")
        return ""

def open_notepad():
    print("Đang mở Notepad++")
    subprocess.Popen(["notepad++"])
    
def create_new_file():
    print("Đang tạo file mới")
    pag.hotkey('ctrl', 'n')

def write_text(text):
    print(f"Writing text: {text}")
    pag.typewrite(text)

def save_file(location):
    print("Saving file")
    pag.hotkey('ctrl', 's')
    time.sleep(1)
    file_name = "output.txt"
    if location == "desktop":
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop_path, file_name)
    else:
        file_path = os.path.join(os.getcwd(), file_name)
    pag.typewrite(file_path)
    pag.press('enter')
    time.sleep(1)

def close_notepad():
    print("Đang đóng Notepad++")
    pag.hotkey('alt', 'f4')

def main():
    while True:
        command = recognize_speech()
        if "mở notepad" in command:
            open_notepad()
        elif "tạo file mới" in command:
            create_new_file()
        elif "ghi" in command:
            print("Listening for text to write")
            text_to_write = recognize_speech()
            write_text(text_to_write)
        elif "lưu" in command:
            save_file("desktop")
        elif "đóng" in command:
            close_notepad()
            break
        else:
            print("Không thể nhận dạng câu lệnh.")

if __name__ == "__main__":
    main()

