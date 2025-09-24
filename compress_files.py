import os
import shutil
import subprocess
# gen by gemin 2.5 flash
def create_and_move_files(source_dir, dest_dir, extensions):
    """Di chuyển các file có đuôi mở rộng xác định sang thư mục mới, giữ nguyên cấu trúc.

    Args:
        source_dir (str): Thư mục gốc để tìm kiếm.
        dest_dir (str): Thư mục đích để di chuyển các file đến.
        extensions (list): Danh sách các đuôi mở rộng cần di chuyển.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(tuple(extensions)):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                dest_path = os.path.join(dest_dir, relative_path)
                
                # Tạo thư mục con nếu chưa tồn tại
                dest_subdir = os.path.dirname(dest_path)
                if not os.path.exists(dest_subdir):
                    os.makedirs(dest_subdir)
                
                try:
                    shutil.move(source_path, dest_path)
                    print(f"Moved: {source_path} -> {dest_path}")
                except Exception as e:
                    print(f"Error moving {source_path}: {e}")

def compress_files_with_7z(folder_to_compress, output_archive):
    """Nén thư mục bằng 7-Zip với các tùy chọn đã chỉ định.

    Args:
        folder_to_compress (str): Thư mục cần nén.
        output_archive (str): Tên file nén đầu ra.
    """
    try:
        # Lệnh 7z: a - thêm file vào archive, -t7z - định dạng 7z, -m0s - nén không sử dụng khối lượng lớn, -mmt=2 - sử dụng 2 luồng '-md=256m', 
        cmd = ['7zr.exe', 'a', '-t7z', '-mx9','-md=27', '-mmt=2', '-mqs', output_archive, folder_to_compress]
        print("Starting compression...")
        subprocess.run(cmd, check=True)
        print(f"Successfully compressed {folder_to_compress} to {output_archive}")
        
    except FileNotFoundError:
        print("Error: 7-Zip executable not found. Please make sure it's installed and in your system's PATH.")
        exit
    except subprocess.CalledProcessError as e:
        print(f"Error during 7-Zip compression: {e}")
        exit
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit

def gom_files_with_7z(folder_to_compress, output_archive):
    """Nén thư mục bằng 7-Zip với các tùy chọn đã chỉ định.

    Args:
        folder_to_compress (str): Thư mục cần nén.
        output_archive (str): Tên file nén đầu ra.
    """
    try:
        # Lệnh 7z: a - thêm file vào archive, -t7z - định dạng 7z, -m0s - nén không sử dụng khối lượng lớn, -mmt=2 - sử dụng 2 luồng
        cmd = ['7zr.exe', 'a', '-t7z', '-mx3', '-mmt=2', output_archive, folder_to_compress]
        print("Starting compression...")
        subprocess.run(cmd, check=True)
        print(f"Successfully compressed {folder_to_compress} to {output_archive}")
        
    except FileNotFoundError:
        print("Error: 7-Zip executable not found. Please make sure it's installed and in your system's PATH.")
        exit
    except subprocess.CalledProcessError as e:
        print(f"Error during 7-Zip compression: {e}")
        exit
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit

def compress_each_subfolder_with_7z(source_dir, output_dir):
    """
    Nén từng thư mục con trực tiếp trong source_dir thành file .7z riêng biệt trong output_dir.
    Args:
        source_dir (str): Thư mục gốc chứa các thư mục con.
        output_dir (str): Thư mục lưu các file nén.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for name in os.listdir(source_dir):
        subfolder_path = os.path.join(source_dir, name)
        if os.path.isdir(subfolder_path):
            archive_name = os.path.join(output_dir, f"{name}.7z")
            gom_files_with_7z(subfolder_path, archive_name)
            try:
                shutil.rmtree(subfolder_path)
                print(f"Successfully removed temporary directory: {subfolder_path}")
            except Exception as e:
                print(f"Error removing temporary directory: {e}")


def main():
    """Chức năng chính để thực thi toàn bộ quy trình."""
    # Thay đổi 'A' thành đường dẫn thư mục gốc của bạn
    source_dir = r'D:\backup\Taydachet2'
    arc_dir = "C:/tmp/arc"
    archive_name = os.path.join(source_dir,'blendfiles.7z')
    
    # Định nghĩa các đuôi mở rộng cần nén
    extensions_to_compress = ['.blend', '.blend1', '.docx', '.xls', '.blend2', '.fbx', '.obj',]
    
    print("--- Starting file processing ---")
    
    # Bước 1: Tạo và di chuyển các file
    create_and_move_files(source_dir, arc_dir, extensions_to_compress)
    
    # Bước 2: Nén thư mục đã di chuyển
    compress_files_with_7z(arc_dir, archive_name)
    
    # Bước 3: Dọn dẹp: xóa thư mục tạm thời sau khi nén
    print("\n--- Cleaning up temporary directory ---")
    try:
        #shutil.rmtree(arc_dir)
        print(f"Successfully removed temporary directory: {arc_dir}")
    except Exception as e:
        print(f"Error removing temporary directory: {e}")
        
    print("\n--- Process completed! ---")

    
    output_dir = source_dir
    compress_each_subfolder_with_7z(source_dir, output_dir)



if __name__ == "__main__":
    main()