#!/usr/bin/python3

__author__ = 'Konstantin Vannson'

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from shutil import move
from time import sleep
import os

# full path for Mac like /Users/user_name/Downloads
source_dir = ''
image_dir = ''
video_dir = ''
audio_dir = ''
document_dir = ''
trash_dir = ''

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt",
                    ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


class MyHandler(FileSystemEventHandler):
    def process_file(self, event):
        file = os.path.basename(event.src_path)
        if file.startswith('.'):
            return None
        filename, extension = os.path.splitext(file)
        extension = extension.lower()

        if extension in image_extensions:
            self.change_dir(event, 'image')
        elif extension in video_extensions:
            self.change_dir(event, 'video')
        elif extension in audio_extensions:
            self.change_dir(event, 'audio')
        elif extension in document_extensions:
            self.change_dir(event, 'document')
        else:
            self.change_dir(event, 'trash')

    @staticmethod
    def change_dir(event, file_type: str):
        end_path_without_file = (
            image_dir if file_type == 'image' else
            video_dir if file_type == 'video' else
            audio_dir if file_type == 'audio' else
            document_dir if file_type == 'document' else
            trash_dir
        )
        base_filename, file_extension = os.path.splitext(os.path.basename(event.src_path))
        end_file_path = os.path.join(end_path_without_file, f'{base_filename}{file_extension}')

        counter = 2
        while os.path.exists(end_file_path):
            end_file_path = os.path.join(end_path_without_file, f'{base_filename}_{counter}{file_extension}')
            counter += 1
        move(event.src_path, end_file_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event)


def main():
    observer = Observer()
    observer.schedule(MyHandler(), path=source_dir, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()
