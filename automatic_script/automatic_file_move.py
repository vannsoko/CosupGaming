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
other_dir = ''

file_extensions = {
    ".jpg": image_dir, ".jpeg": image_dir, ".jpe": image_dir, ".jif": image_dir, ".jfif": image_dir, ".jfi": image_dir,
    ".png": image_dir, ".gif": image_dir, ".webp": image_dir, ".tiff": image_dir, ".tif": image_dir, ".psd": image_dir,
    ".raw": image_dir, ".arw": image_dir, ".cr2": image_dir, ".nrw": image_dir, ".k25": image_dir, ".bmp": image_dir,
    ".dib": image_dir, ".heif": image_dir, ".heic": image_dir, ".ind": image_dir, ".indd": image_dir, ".indt": image_dir,
    ".jp2": image_dir, ".j2k": image_dir, ".jpf": image_dir, ".jpx": image_dir, ".jpm": image_dir, ".mj2": image_dir,
    ".svg": image_dir, ".svgz": image_dir, ".ai": image_dir, ".eps": image_dir, ".ico": image_dir,
    
    ".webm": video_dir, ".mpg": video_dir, ".mp2": video_dir, ".mpeg": video_dir, ".mpe": video_dir, ".mpv": video_dir,
    ".ogg": video_dir, ".mp4": video_dir, ".mp4v": video_dir, ".m4v": video_dir, ".avi": video_dir, ".wmv": video_dir,
    ".mov": video_dir, ".qt": video_dir, ".flv": video_dir, ".swf": video_dir, ".avchd": video_dir,
    
    ".m4a": audio_dir, ".flac": audio_dir, ".mp3": audio_dir, ".wav": audio_dir, ".wma": audio_dir, ".aac": audio_dir,
    
    ".doc": document_dir, ".docx": document_dir, ".odt": document_dir, ".pdf": document_dir, ".xls": document_dir,
    ".xlsx": document_dir, ".ppt": document_dir, ".pptx": document_dir
}


class MyHandler(FileSystemEventHandler):
    def process_file(self, event):
        file = os.path.basename(event.src_path)
        if file.startswith('.'):
            return None
        filename, extension = os.path.splitext(file)
        extension = extension.lower()
        self.change_dir(event, extension)

    @staticmethod
    def change_dir(event, extension: str):
        end_path_without_file = file_extensions.get(extension, other_dir)
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
