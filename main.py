import speech_recognition as sr
import pyautogui as pag
import subprocess
import time
import os
import platform

os_name = platform.system()
if os_name == "Windows":
    app_name = "notepad++"
else:
    app_name = "notepad-plus-plus" # The Linux/MacOS version is for snap package "notepad-plus-plus"

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
    subprocess.Popen([app_name])
    
def create_new_file():
    print("Đang tạo file mới")
    pag.hotkey('ctrl', 'n')

def write_text(text):
    print(f"Writing text: {text}")
    array= text.split()
    if len(array)==0:
        return 0
    command=[app_name, "-qt='"]
    command[1]+=array[0]
    for i in range(1,len(array)):
        command+=[array[i]]
    command[len(command)-1]+="'"
    print(command)
    subprocess.run(command)

def save_file(location):
    print("Saving file")
    pag.hotkey('ctrl', 'shift','s')
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
    if os_name == "Windows":
        subprocess.run(["taskkill", "/f", "/im", app_name+".exe"])
    else:
        subprocess.run(["killall", app_name])

def main():
    while True:
        command = recognize_speech()
        if "mở notepad" in command:
            open_notepad()
        elif "mới" in command:
            create_new_file()
        elif "ghi" in command or "viết" in command or "gõ" in command:
            print("Hãy đọc nội dung văn bản bạn muốn ghi vào file.")
            text_to_write=""
            while not text_to_write:
                text_to_write = recognize_speech()
            write_text(text_to_write)
        elif "lưu" in command:
            if "desktop" in command:
                save_file("desktop")
            else:
                save_file("current")
        elif "đóng" in command:
            close_notepad()
            break
        else:
            print("Không thể nhận dạng câu lệnh.")

if __name__ == "__main__":
    main()

