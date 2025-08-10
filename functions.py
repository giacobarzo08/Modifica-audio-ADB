import os
import shutil
import subprocess
import numpy as np
from matplotlib import pyplot as plt
from typing import Optional, Union
from numpy.typing import ArrayLike
from audio_fun import copy_all_music_files

# Function to prompt the user for a yes/no confirmation
def ask_confirmation() -> bool:
    choice = ''
    while choice not in ('y', 'n'):
        choice = input("Do you want to continue? (y/n): ").lower()
    return choice == 'y'


# Function to compute the average frequency of audio data using FFT
def average_frequency(audio_data: np.ndarray, sample_rate: int) -> Union[int, float]:
    # Perform real FFT on the audio samples
    fft_values = np.fft.rfft(audio_data)
    # Compute corresponding frequencies for each FFT bin
    fft_frequencies = np.fft.rfftfreq(len(audio_data), d=1/sample_rate)
    
    magnitudes = np.abs(fft_values)
    # Weighted average of frequencies by their magnitudes
    avg_freq = np.sum(fft_frequencies * magnitudes) / np.sum(magnitudes)
    
    return avg_freq


# Function to plot the audio waveform with optional horizontal and vertical lines
def plot_audio_waveform_with_lines(
    audio_data: np.ndarray,
    horizontal_lines: Optional[ArrayLike] = None,
    vertical_lines: Optional[ArrayLike] = None
) -> None:
    plt.figure(figsize=(10, 4))
    plt.plot(audio_data, color='blue')
    
    # Draw horizontal lines if provided
    if horizontal_lines is not None:
        for y in horizontal_lines:
            plt.axhline(
                y=y,
                color='red',
                linestyle='--',
                label=f'y={y}',
                alpha=0.5
            )
    
    # Draw vertical lines if provided
    if vertical_lines is not None:
        for x in vertical_lines:
            plt.axvline(
                x=x,
                color='green',
                linestyle='--',
                label=f'x={x}',
                alpha=0.5
            )
    
    plt.title("Recorded Audio Amplitude Plot")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

# Function to pull files from an Android device via ADB, copying only .mp3 files
def adb_pull(remote_path: str, local_dir: Optional[str] = None) -> bool:
    # Determine local directory for pull; default under LOCALAPPDATA/a4a
    if local_dir is None:
        local_dir = os.path.join(os.getenv('LOCALAPPDATA', ''), 'a4a')
    
    # Create base directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)
    
    
    # Prepare a temporary directory for pulling files
    temp_pull_dir = os.path.join(local_dir, "temp_music_pull")
    if os.path.exists(temp_pull_dir):
        shutil.rmtree(temp_pull_dir)
    os.makedirs(temp_pull_dir)
    
    # Run the adb pull command
    try:
        subprocess.run(
            ['adb', 'pull', remote_path, temp_pull_dir],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ADB pull error: {e.stderr}")
        return False
    
    # Look for the pulled Music folder
    source_music_dir = os.path.join(temp_pull_dir)
    if not os.path.exists(source_music_dir):
        print("Music folder not found in the temporary directory.")
        shutil.rmtree(temp_pull_dir)
        return False
    
    # Move only .mp3 files into the local Music directory
    copy_all_music_files(source_music_dir, local_dir)
    
    # Clean up the temporary pull directory
    shutil.rmtree(temp_pull_dir)
    
    print("Synchronization completed.")
    return True
