import logging
import os
import shutil
import threading
import customtkinter as cs
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(filename='pro.log', level=logging.DEBUG,
                    format = '%(asctime)s:%(levelname)s: Line %(lineno)d :%(message)s')

cancel_event = threading.Event()

def copy_file_worker(pathes_tuple):
    if cancel_event.is_set():
        return False
    src, dest = pathes_tuple
    shutil.copy2(src, dest)
    return True

def photo_video_copier(source_dir_path, target_dir_path):

    try:
        pathes_list = []
        logging.info("start copying the file...")

        for root, dirnames, filenames in os.walk(source_dir_path):
            if cancel_event.is_set():
                return False,"Process Cancelled"

            for filename in filenames:

                src_file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(src_file_path, source_dir_path)
                dest_file_path = os.path.join(target_dir_path, rel_path)

                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                pathes_list.append((src_file_path, dest_file_path))

        with ThreadPoolExecutor() as executor:
            for result in executor.map(copy_file_worker, pathes_list):
                if cancel_event.is_set():
                    logging.info("Copying process cancelled by user")
                    return False,"Copying Cancelled"

        logging.info("Done successfully")
        return True,"Done successfully"
    except FileNotFoundError:
        logging.error("File not found")
        return False,"Error"
    except PermissionError:
        logging.error("you don't have permission")
        return False,"Error"


def main():
    cs.set_appearance_mode("system")
    cs.set_default_color_theme("dark-blue")

    root = cs.CTk()
    root.geometry("800x750")

    frame = cs.CTkFrame(master=root)
    frame.pack(pady=50, padx=70, fill="both", expand=True)

    label = cs.CTkLabel(master=frame, text="Copy photos & videos Fast", font=("Roboto", 24))
    label.pack(pady=22, padx=20)

    entry1 = cs.CTkEntry(master=frame, placeholder_text="Source Folder Path", width=300)
    entry1.pack(pady=(10,5), padx=20)


    def browse_file():
        file_to_copy = cs.filedialog.askdirectory()
        if file_to_copy:
            entry1.delete(0, 'end')
            entry1.insert(0, file_to_copy)

    browse_btn = cs.CTkButton(master=frame, text='Select File', command=browse_file, border_width=1)
    browse_btn.pack(pady=5)

    entry2 = cs.CTkEntry(master=frame, placeholder_text="Destination Folder Path", width=300)
    entry2.pack(pady=(10,5), padx=20)

    def copy_direction():
        try:

            direction_file = cs.filedialog.askdirectory()
            if direction_file:
                entry2.delete(0, 'end')
                entry2.insert(0, direction_file)

        except FileNotFoundError:
            logging.error("File not found")
        except PermissionError:
            logging.error("you don't have permission")


    dest_btn = cs.CTkButton(master=frame, text='Select Destination', command=copy_direction, border_width=1)
    dest_btn.pack(pady=(0, 20))

    status_label = cs.CTkLabel(master=frame, text="", font=("Roboto", 14))


    def start_copy():
        try:
            cancel_event.clear()

            filepath = entry1.get().strip().strip('"')
            directionpath = entry2.get().strip().strip('"')

            if not filepath:
                status_label.configure(text="Please enter a file want to copy path first!", text_color="orange")
                return

            if not directionpath:
                status_label.configure(text="Please enter a file want to copy path first!", text_color="orange")
                return

            if os.path.exists(filepath):
                if os.path.exists(directionpath):
                    logging.info("start calling the copy function")

                    def run_in_background():
                        status_label.configure(text="Copying in progress...", text_color="yellow")
                        success,message = photo_video_copier(filepath, directionpath)

                        if success:
                            status_label.configure(text=message, text_color="green")

                        else:
                            status_label.configure(text=message, text_color="red")

                    threading.Thread(target=run_in_background, daemon=True).start()
                else:
                    logging.error("direction file does not exist")
                    status_label.configure(text="File does not exist, chek the path!", text_color="red")
            else:
                logging.error("main file does not exist")
                status_label.configure(text="File does not exist, chek the path!", text_color="red")

        except FileNotFoundError:
            logging.error("File not found")
        except PermissionError:
            logging.error("you don't have permission")

    def stop_copy():
        cancel_event.set()
        status_label.configure(text="Cancelling copy process...", text_color="orange")


    button = cs.CTkButton(master=frame, text="Copy", command=start_copy, width=200, height=45, font=("Roboto", 16, "bold"))
    button.pack(pady=15, padx=20)

    cancel_btn = cs.CTkButton(master=frame, text="Cancel", command=stop_copy, fg_color="red", hover_color="#8B0000",width=120)
    cancel_btn.pack(pady=5)
    status_label.pack(pady=15, padx=20)

    root.mainloop()


if __name__ == '__main__':
    main()

