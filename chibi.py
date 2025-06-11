from PIL import Image
from PIL import Image
import os
import numpy as np

# import đúng các lớp từ moviepy
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os


# --- Cấu hình đường dẫn và kích thước ---
OUTPUT_DIR = "animation_output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

FRAME_RATE = 15 # Số khung hình mỗi giây
FRAME_WIDTH = 1280 # Chiều rộng của khung hình video
FRAME_HEIGHT = 720 # Chiều cao của khung hình video
BG_COLOR = (255, 255, 255) # Màu nền trắng

# --- Đường dẫn ảnh chibi đã chuẩn bị ---
PATH_CHIBI_NU_BUON = "chibi_nu_buon.png"
PATH_CHIBI_NU_VUI = "chibi_nu_vui.png"
PATH_CHIBI_NAM_TAY_QUA = "chibi_nam_tay_qua.png"
PATH_CHIBI_OM_NHAU = "chibi_om_nhau.png"

# --- Hàm hỗ trợ ---
def create_blank_frame(width, height, color):
    """Tạo một khung hình trống với màu nền."""
    return Image.new('RGB', (width, height), color)

def overlay_image(background_frame, overlay_img_path, position, size=None):
    """Chèn một ảnh lên khung hình nền."""
    try:
        overlay_img = Image.open(overlay_img_path).convert("RGBA")
        if size:
            overlay_img = overlay_img.resize(size, Image.Resampling.LANCZOS)

        # Tạo một ảnh nền có alpha để paste (nếu ảnh overlay có nền trong suốt)
        alpha_composite = Image.new('RGBA', background_frame.size)
        alpha_composite.paste(overlay_img, position, overlay_img)
        
        # Kết hợp ảnh overlay với khung hình nền
        final_frame = Image.alpha_composite(background_frame.convert("RGBA"), alpha_composite)
        return final_frame.convert("RGB") # Chuyển lại RGB để lưu video
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh {overlay_img_path}. Hãy đảm bảo đường dẫn đúng.")
        return background_frame # Trả về khung hình nền nếu lỗi

def generate_frames():
    """Tạo danh sách các khung hình cho hoạt ảnh."""
    frames = []

    # --- Cảnh 1: Nữ buồn chán ---
    duration_scene1 = 2 * FRAME_RATE # 2 giây
    for _ in range(duration_scene1):
        frame = create_blank_frame(FRAME_WIDTH, FRAME_HEIGHT, BG_COLOR)
        # Vị trí cho chibi nữ (tùy chỉnh để phù hợp với ảnh của bạn)
        frame = overlay_image(frame, PATH_CHIBI_NU_BUON, (FRAME_WIDTH // 2 - 100, FRAME_HEIGHT // 2 - 150), size=(200,300))
        frames.append(frame)

    # --- Cảnh 2: Nam bước vào và cầm quà ---
    duration_scene2 = 3 * FRAME_RATE # 3 giây
    start_x_nam = -200 # Bắt đầu từ ngoài khung hình bên trái
    end_x_nam = FRAME_WIDTH // 2 - 200 # Kết thúc ở vị trí bên cạnh nữ
    
    # Kích thước chibi nam (tùy chỉnh)
    chibi_nam_size = (200, 300) 
    
    for i in range(duration_scene2):
        frame = create_blank_frame(FRAME_WIDTH, FRAME_HEIGHT, BG_COLOR)
        
        # Chibi nữ vẫn buồn
        frame = overlay_image(frame, PATH_CHIBI_NU_BUON, (FRAME_WIDTH // 2 - 100, FRAME_HEIGHT // 2 - 150), size=(200,300))

        # Di chuyển chibi nam
        current_x_nam = start_x_nam + (end_x_nam - start_x_nam) * (i / duration_scene2)
        frame = overlay_image(frame, PATH_CHIBI_NAM_TAY_QUA, (int(current_x_nam), FRAME_HEIGHT // 2 - 150), size=chibi_nam_size)
        frames.append(frame)

    # --- Cảnh 3: Nữ vui vẻ trở lại ---
    duration_scene3 = 1 * FRAME_RATE # 1 giây
    for _ in range(duration_scene3):
        frame = create_blank_frame(FRAME_WIDTH, FRAME_HEIGHT, BG_COLOR)
        # Nữ vui vẻ
        frame = overlay_image(frame, PATH_CHIBI_NU_VUI, (FRAME_WIDTH // 2 - 100, FRAME_HEIGHT // 2 - 150), size=(200,300))
        # Nam đứng gần đó
        frame = overlay_image(frame, PATH_CHIBI_NAM_TAY_QUA, (FRAME_WIDTH // 2 - 200, FRAME_HEIGHT // 2 - 150), size=chibi_nam_size)
        frames.append(frame)

    # --- Cảnh 4: Hai người ôm nhau ---
    duration_scene4 = 2 * FRAME_RATE # 2 giây
    for _ in range(duration_scene4):
        frame = create_blank_frame(FRAME_WIDTH, FRAME_HEIGHT, BG_COLOR)
        # Hai người ôm nhau (một ảnh duy nhất)
        frame = overlay_image(frame, PATH_CHIBI_OM_NHAU, (FRAME_WIDTH // 2 - 150, FRAME_HEIGHT // 2 - 150), size=(300,300))
        frames.append(frame)

    return frames

def create_animation(frames, output_filename="chibi_animation.mp4"):
    """Tạo video từ danh sách các khung hình."""
    print("Bắt đầu tạo video...")
    try:
        clip = ImageSequenceClip([np.array(f) for f in frames], fps=FRAME_RATE)
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        clip.write_videofile(output_path, codec="libx264")
        print(f"Video đã được tạo thành công tại: {output_path}")
    except Exception as e:
        print(f"Lỗi khi tạo video: {e}")
        print("Đảm bảo bạn đã cài đặt các codec cần thiết cho MoviePy (ví dụ: ffmpeg).")
        print("Bạn có thể thử cài đặt ffmpeg thủ công hoặc kiểm tra lại cấu hình MoviePy.")
        
# --- Thực thi chương trình ---
if __name__ == "__main__":
    # Kiểm tra xem moviepy đã import numpy chưa, nếu chưa thì thêm vào
    try:
        import numpy as np
    except ImportError:
        print("Cảnh báo: Thư viện numpy chưa được cài đặt. Đang cài đặt...")
        os.system("pip install numpy")
        import numpy as np

    print("Đang tạo các khung hình hoạt ảnh...")
    animation_frames = generate_frames()

    if animation_frames:
        create_animation(animation_frames)
    else:
        print("Không có khung hình nào được tạo. Vui lòng kiểm tra lại lỗi file ảnh.")