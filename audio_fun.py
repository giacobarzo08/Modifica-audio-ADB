import ffmpeg
import os
import shutil

def convert_3gp_to_mp3(input_file: str, output_file: str) -> None:
    """Convert a 3GP audio file to MP3 format using ffmpeg."""
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, format='mp3', ar=44100, ac=2, audio_bitrate='192k')
    ffmpeg.run(stream, overwrite_output=True)

def copy_all_music_files(
    source_dir: str, 
    destination_dir: str, 
) -> None:
    """Copy all music files with the specified extension from source to destination directory."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    for root, _, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith('.3gp'):
                src_file = os.path.join(root, filename)
                dst_file = os.path.join(destination_dir, filename)
                convert_3gp_to_mp3(src_file, dst_file.replace('.3gp', '.mp3'))
                # shutil.copy2(src_file, dst_file)
                # convert_3gp_to_mp3(src_file, dst_file.replace('.3gp', '.mp3'))