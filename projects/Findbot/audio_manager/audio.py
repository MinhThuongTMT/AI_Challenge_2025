'''
import subprocess
import os

def play_wav_background(file_path):
    """
    Phát một file WAV trong nền bằng aplay.

    Args:
        file_path (str): Đường dẫn đầy đủ đến file WAV.

    Returns:
        subprocess.Popen: Đối tượng tiến trình con nếu thành công,
                          hoặc None nếu file không tồn tại hoặc lỗi khác.
    """
    if not os.path.exists(file_path):
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        return None

    # aplay là công cụ dòng lệnh tiêu chuẩn để phát file WAV trên Linux (bao gồm Raspberry Pi)
    command = ['aplay', file_path]

    try:
        # Sử dụng Popen để chạy tiến trình trong nền.
        # stdout và stderr được chuyển hướng đến DEVNULL để tránh in ra console.
        process = subprocess.Popen(command,
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        print(f"Đang phát '{file_path}' trong nền với PID: {process.pid}")
        return process
    except FileNotFoundError:
        print(f"Lỗi: Lệnh 'aplay' không tìm thấy. Hãy đảm bảo 'alsa-utils' đã được cài đặt.")
        return None
    except Exception as e:
        print(f"Lỗi khi khởi chạy tiến trình phát audio: {e}")
        return None

# Ví dụ kiểm tra (chỉ chạy khi file này được thực thi trực tiếp)
if __name__ == "__main__":
    # Thay thế bằng đường dẫn đến file WAV của bạn để kiểm tra
    test_wav_file = "/home/ngonlua/Bao_Workspace/Findbot/hoithoai/hoithoai_xacnhan1.wav"
    print(f"Đang thử nghiệm module audio_player với file: {test_wav_file}")

    # Đảm bảo bạn có file WAV để thử nghiệm. Nếu không, hãy tạo một file nhỏ.
    # Ví dụ: download từ internet hoặc tạo bằng Audacity.

    process = play_wav_background(test_wav_file)

    if process:
        print("Đang chạy 5 giây để đợi audio phát...")
        import time
        time.sleep(5) # Đợi 5 giây để file audio có thể phát

        # Kiểm tra xem tiến trình còn chạy không
        if process.poll() is None:
            print(f"Tiến trình phát audio (PID: {process.pid}) vẫn đang chạy.")
            # Bạn có thể dừng nó nếu muốn:
            # process.terminate()
            # print("Đã gửi lệnh dừng.")
        else:
            print(f"Tiến trình phát audio đã kết thúc với mã: {process.returncode}")
    else:
        print("Không thể khởi chạy tiến trình phát audio.")

    print("Kết thúc thử nghiệm module.")

'''
import simpleaudio as sa
import os
import time

def play_wav_background(file_path):
    """
    Phát một file WAV và chờ cho đến khi nó phát xong.

    Args:
        file_path (str): Đường dẫn đầy đủ đến file WAV.
    """
    if not os.path.exists(file_path):
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        return

    try:
        # Bước 1: Đọc file WAV
        wave_obj = sa.WaveObject.from_wave_file(file_path)

        # Bước 2: Bắt đầu phát file WAV
        play_obj = wave_obj.play()
        print(f"Bắt đầu phát '{file_path}'...")

        # Bước 3: Chờ cho đến khi âm thanh phát xong
        play_obj.wait_done()
        print(f"Đã phát xong '{file_path}'.")

    except Exception as e:
        print(f"Lỗi khi phát audio: {e}")

# --- Ví dụ cách sử dụng ---
# Giả sử bạn có một file "am_thanh.wav"
# play_wav_linear("am_thanh.wav")
#
# # Công việc này sẽ chỉ được thực hiện sau khi audio đã phát xong
# print("Bây giờ tôi có thể làm các việc khác...")
