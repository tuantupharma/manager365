import os
import shutil
import subprocess
import argparse

def is_compressible(filename):
    # Danh sách các đuôi file nén tốt (word, excel, blend, text...)
    exts = ['.doc', '.docx', '.xls', '.xlsx', '.blend', '.blend1', '.blend2', '.txt']
    _, ext = os.path.splitext(filename)
    return ext.lower() in exts

def main():
    parser = argparse.ArgumentParser(description="Tách và nén các file có thể nén tốt.")
    parser.add_argument("source_dir", help="Đường dẫn đến thư mục nguồn (A)")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source_dir)
    if not os.path.isdir(source_dir):
        print(f"Lỗi: Thư mục {source_dir} không tồn tại.")
        return

    parent_dir = os.path.dirname(source_dir)
    base_name = os.path.basename(source_dir)
    
    # Tạo thư mục A_arc ngang hàng với thư mục A
    arc_dir = os.path.join(parent_dir, f"{base_name}_arc")
    
    if not os.path.exists(arc_dir):
        os.makedirs(arc_dir)

    print(f"Đang di chuyển các file có thể nén tốt sang {arc_dir}...")
    moved_count = 0

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if is_compressible(file):
                src_path = os.path.join(root, file)
                # Tính đường dẫn tương đối so với thư mục nguồn
                rel_path = os.path.relpath(src_path, source_dir)
                dest_path = os.path.join(arc_dir, base_name, rel_path) 
                # Chú ý: để giải nén ra đè lên đúng kiến trúc, 
                # tốt nhất đưa file vào cấu trúc A_arc/A/...
                # Khi giải nén A_arc.7z sẽ được thư mục A_arc chứa thư mục A (nơi có các file)
                # Sau đó copy thư mục A đó đè lên thư mục A ban đầu là xong.
                
                # Tạo các thư mục con tương ứng bên đích
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Di chuyển file sang thư mục đích
                shutil.move(src_path, dest_path)
                print(f"Đã chuyển: {rel_path}")
                moved_count += 1

    print(f"Hoàn tất di chuyển {moved_count} file.")

    # Nén thư mục A_arc bằng 7zip
    # Yêu cầu: dùng -mqs=on để gom các file cùng loại tăng hiệu quả nén, -mmt2 dùng 2 luồng
    archive_name = os.path.join(parent_dir, f"{base_name}_arc.7z")
    
    print(f"Đang nén thư mục thành {archive_name}...")
    try:
        # Gọi 7z. Máy tính cần cài đặt 7-Zip và cấu hình biến môi trường PATH cho 7z, 
        # hoặc nếu ở Windows có thể gọi đường dẫn thực thi C:\Program Files\7-Zip\7z.exe
        seven_zip_path = "7z"
        if os.path.exists(r"C:\Program Files\7-Zip\7z.exe"):
            seven_zip_path = r"C:\Program Files\7-Zip\7z.exe"
            
        cmd = [
            seven_zip_path, "a", archive_name, 
            os.path.join(arc_dir, "*"), 
            "-mx9",       # Nén tối đa
            "-mqs=on",    # Sort files for solid archive
            "-mmt2"       # 2 threads
        ]
        
        # Chạy lệnh
        subprocess.run(cmd, check=True)
        print("Hoàn tất nén!")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy 7z. Hãy đảm bảo đã cài 7-Zip và thêm vào biến môi trường PATH.")
    except Exception as e:
        print(f"Có lỗi xảy ra khi nén: {e}")

if __name__ == "__main__":
    main()
