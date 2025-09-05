import sys
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/animations')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/Manager')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/audio_manager')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/Uart_manager')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/GUI')
sys.path.append(r'/home/ngonlua/Bao_Workspace/Findbot/FindbotMqtt')

import socket
from uart_module import Uart  # Thay UartListener, UartSender bằng Uart
import time
import queue
import threading
import serial
import subprocess
from audio import play_wav_background
from querylocation import query_findbot_product
from querylocation import find_category
import json
import faulthandler  # Thêm để debug segfault
faulthandler.enable()

class SocketSender:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    def send_message(self, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            client_socket.send(message.encode())
            print(f"Socket sent to main.py: {message}")
            client_socket.close()
            return True
        except Exception as e:
            print(f"Error sending socket message: {e}")
            return False

def process_1(uart, socket_sender):
    uart.send_message("001")
    socket_sender.send_message("starthello")
    print('Xin chao, ban muon tim san pham nao ?')
    play_wav_background("/home/ngonlua/Bao_Workspace/Findbot/hoithoai/xinchao.wav")
    socket_sender.send_message("listen")
    uart.send_message("002")

def process_2(itemname, uart, socket_sender):
    uart.send_message("001")
    uart.send_message("005")        
    socket_sender.send_message("startconfirm")
    itemlink = f"/home/ngonlua/Bao_Workspace/Findbot/hoithoai/{itemname}.wav"
    print(f'Co phai ban muon tim san pham {itemname} khong ?')
    play_wav_background("/home/ngonlua/Bao_Workspace/Findbot/hoithoai/xacnhan1.wav")
    play_wav_background(itemlink)
    uart.send_message("002")

def process_3(itemname, uart, socket_sender, p_name):
    uart.send_message("001")
    sp = query_findbot_product('F1', p_name)
    print(f"{sp}\n")
    socket_sender.send_message(sp[2])
    play_wav_background("/home/ngonlua/Bao_Workspace/Findbot/hoithoai/ketthuc2.wav")
    socket_sender.send_message("smile")
    uart.send_message("002")

def process_4(uart, socket_sender):
    uart.send_message("001")
    socket_sender.send_message("confirmno")
    print('Moi ban vui long noi lai ten san pham')
    play_wav_background("/home/ngonlua/Bao_Workspace/Findbot/hoithoai/doansai.wav")
    socket_sender.send_message("listen")
    uart.send_message("002")
    uart.send_message("005")

def process_5(uart, socket_sender):
    socket_sender.send_message("smile")
    print('/home/ngonlua/Bao_Workspace/Findbot/hoithoai/ketthuc1.wav')  

def process_uart_messages(message_queue, uart, socket_sender, p_name):
    while True:
        try:
            message = message_queue.get(timeout=1)
            if message == "start":
                process_1(uart, socket_sender)
            elif message == 'end':
                process_5(uart, socket_sender)
            elif message == 'reactivated':
                continue
            else:
                if message == 'dung':
                    process_3(message, uart, socket_sender, p_name)
                elif message == 'sai':
                    process_4(uart, socket_sender)
                else:
                    if message != 'xinchao':
                        audio_productname = find_category(message)  
                        p_name = message                    
                        process_2(audio_productname, uart, socket_sender)
            message_queue.task_done()
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error processing message from queue: {e}")
            message_queue.task_done()

def run_mqtt_process():
    try:
        process = subprocess.Popen(['python3', '/home/ngonlua/Bao_Workspace/Findbot/FindbotMqtt/mqtt_interface.py'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print("Main process: Child process started with PID:", process.pid)     
        return process
    except Exception as e:
        print(f"Error running mqtt process: {e}")

if __name__ == '__main__':
    run_mqtt_process()
    p = subprocess.Popen(["python", "GUI/GUInew/main.py"])
    uart_port = '/dev/ttyAMA0'
    baud_rate = 115200
    uart_message_queue = queue.Queue()
    socket_sender = SocketSender()
    print("Starting Manager...")
    uart = None
    processing_thread = None
    p_name = ''
    try:
        uart = Uart(uart_port, baud_rate, uart_message_queue)
        uart.start()
        processing_thread = threading.Thread(target=process_uart_messages, args=(uart_message_queue, uart, socket_sender, p_name))
        processing_thread.daemon = True
        processing_thread.start()
        print('Message listen processing start')
        while True:
            time.sleep(1)
    except serial.SerialException as e:
        print(f"Lỗi cổng nối tiếp: {e}. Đảm bảo cổng {uart_port} khả dụng và đúng.")
    except KeyboardInterrupt:
        print("Chương trình Manager bị ngắt.")
    finally:
        if uart:
            uart.stop()
        if processing_thread and processing_thread.is_alive():
            uart_message_queue.join()
        p.terminate()
        print("Manager exited.")
