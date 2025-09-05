'''
import serial
import threading
import time
import queue

class UartListener:
	def __init__(self, port, baudrate, message_queue):
		self.ser = serial.Serial(port, baudrate, timeout=1)
		self.message_queue = message_queue
		self._running = False
		self.thread = None
		print(f'Listen on {port}@{baudrate}')
	def _listen(self):
		while self._running:
			if self.ser.in_waiting > 0:
				try:
					message = self.ser.readline().decode('utf-8').strip()
					if message:
						print(f'UART receive {message}')
						self.message_queue.put(message)
				except Exception as e:
					print(f'Error {e}')

	def start(self):
		if not self._running:
			self._running = True
			self.thread = threading.Thread(target = self._listen)
			self.thread.daemon = True
			self.thread.start()
			print('UART Listen start')
	def stop(self):
		self._running = False
		if self.thread and self.thread.is_alive():
			self.thread.join()
		self.ser.close()
		print('UART stop')




class UartSender:
    def __init__(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"UART Sender initialized on {port}@{baudrate}")
        except serial.SerialException as e:
            print(f"Error opening UART port {port}: {e}")
            self.ser = None # Đặt ser thành None nếu có lỗi

    def send_message(self, message):
        if self.ser and self.ser.is_open:
            try:
                # Mã hóa chuỗi thành bytes trước khi gửi
                encoded_message = message.encode('utf-8')
                self.ser.write(encoded_message)
                print(f"UART Sender sent: '{message}'")
                return True
            except serial.SerialException as e:
                print(f"Error sending message via UART: {e}")
                return False
            except Exception as e:
                print(f"An unexpected error occurred while sending: {e}")
                return False
        else:
            print("UART port is not open or not initialized.")
            return False

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("UART Sender closed.")
            
            
            
'''
import serial
import threading
import time
import queue

class Uart:
    def __init__(self, port, baudrate, message_queue):
        self.message_queue = message_queue
        self.lock = threading.Lock()
        self._running = False
        self.thread = None
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"UART initialized on {port}@{baudrate}")
        except serial.SerialException as e:
            print(f"Error opening UART port {port}: {e}")
            self.ser = None
            raise

    def send_message(self, message):
        if not self.ser or not self.ser.is_open:
            print("UART port is not open or not initialized.")
            return False
        try:
            with self.lock:
                encoded_message = message.encode('utf-8')
                self.ser.write(encoded_message)
                print(f"UART sent: '{message}'")
                return True
        except serial.SerialException as e:
            print(f"Error sending message via UART: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error while sending: {e}")
            return False

    def receive_message(self):
        if not self.ser or not self.ser.is_open:
            print("UART port is not open or not initialized.")
            return
        while self._running:
            try:
                with self.lock:
                    if self.ser.in_waiting > 0:
                        raw_data = self.ser.readline()
                        print(f"Raw UART data: {raw_data!r}")  # Debug raw data
                        message = raw_data.decode('utf-8', errors='ignore').strip()
                        if message:
                            print(f"UART receive: {message}")
                            self.message_queue.put(message)
            except serial.SerialException as e:
                print(f"Error receiving message via UART: {e}")
            except Exception as e:
                print(f"Unexpected error while receiving: {e}")
            time.sleep(0.01)  # Ngăn CPU usage cao

    def start(self):
        if not self._running and self.ser and self.ser.is_open:
            self._running = True
            self.thread = threading.Thread(target=self.receive_message)
            self.thread.daemon = True
            self.thread.start()
            print("UART receive start")

    def stop(self):
        self._running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("UART closed")
