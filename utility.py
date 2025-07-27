import os
from logger import Logger, Message
import noisereduce as nr
import sounddevice as sd
import soundfile as sf
import functions
import numpy as np
from typing import Optional, Union, List

# Initialize a file logger for this module
log = Logger('default', 'Audio_For_Android', 'md')


class AudioFile:
    """
    Represents an audio file loaded from disk.
    """

    def __init__(self, file_path: str) -> None:
        # Validate that file_path is a string
        if not isinstance(file_path, str):
            Message(f'file_path must be a string, not {type(file_path)}', 'e').on_file(log)
            raise TypeError(f'Invalid path type: {type(file_path)}')

        # Attempt to read audio data and sample rate
        try:
            self._audio_data, self._sample_rate = sf.read(file_path, dtype='float64')
        except Exception as e:
            Message(f'Error reading file: {e}', 'e').on_file(log)
            raise


    @property
    def sample_rate(self) -> int:
        """
        Returns the audio's sample rate.
        """
        return self._sample_rate


    @property
    def audio_data(self) -> np.ndarray:
        """
        Returns the raw audio samples as a NumPy array.
        """
        return self._audio_data



class AudioData:
    """
    Provides analysis and manipulation methods for audio sample arrays.
    """

    def __init__(self, audio_file: AudioFile) -> None:
        # Store raw data and rate
        self.data: np.ndarray = audio_file.audio_data
        self.rate: int = audio_file.sample_rate

        # Compute average of positive and negative amplitudes separately
        positives = [v for v in self.data if v > 0]
        negatives = [v for v in self.data if v < 0]
        avg_pos = sum(positives) / len(positives) if positives else 0
        avg_neg = sum(negatives) / len(negatives) if negatives else 0

        # Store the midpoint amplitude
        self._mid_amplitude = (avg_pos - avg_neg) / 2


    def is_distorted(self) -> bool:
        """
        Returns True if more than 10% of samples exceed the [-1, 1] range.
        """
        out_of_range_count = sum(1 for v in self.data if abs(v) > 1)
        return (out_of_range_count / len(self.data)) > 0.1


    def is_balanced(self) -> bool:
        """
        Checks left-right channel balance by comparing even and odd samples.
        """
        left_channel = self.data[0::2]
        right_channel = self.data[1::2]

        avg_left = sum(left_channel) / len(left_channel) if (len(left_channel) != 0) else 0
        avg_right = sum(right_channel) / len(right_channel) if (len(right_channel) != 0) else 0

        # Balanced if difference within 5%
        return abs(avg_left - avg_right) / max(abs(avg_left), abs(avg_right), 1e-9) <= 0.05


    def is_rising_trend(self) -> bool:
        """
        Splits data into 0.1-second frames and checks if each frame's
        average amplitude strictly increases over time.
        """
        frame_size = int(self.rate * 0.1)
        means: List[float] = []

        # Compute mean amplitude per frame
        for start in range(0, len(self.data), frame_size):
            frame = self.data[start:start + frame_size]
            if len(frame) != 0:
                means.append(sum(frame) / len(frame))

        # Verify strictly increasing trend
        return all(means[i] > means[i - 1] for i in range(1, len(means)))


    def increase_volume(self, factor: Union[float, int] = 1.5) -> None:
        """
        Scales all samples by factor. Issues warnings if factor extreme.
        """
        if not isinstance(factor, (int, float)):
            Message(f'volume factor must be int or float, not {type(factor)}', 'e').on_file(log)
            return

        if factor < 0.5:
            Message('Volume will be more than halved', 'w').on_file(log)
        elif factor > 2:
            Message('Volume will be more than doubled', 'w').on_file(log)

        # Apply scaling
        self.data = self.data * factor


    def has_annoying_frequency(self) -> bool:
        """
        Returns True if the audio's average frequency falls between 2 kHz and 5 kHz.
        """
        avg_freq = functions.average_frequency(self.data, self.rate)
        return 2000 < avg_freq < 5000


    def reduce_noise_section(self, start_time: float, end_time: float) -> None:
        """
        Uses noisereduce to remove background noise sampled from a time window.
        """
        start_idx = int(start_time * self.rate)
        end_idx = int(end_time * self.rate)

        # Validate time window
        if start_idx < 0 or start_idx > len(self.data):
            Message('Start time out of range', 'e').on_file(log)
            raise ValueError('Invalid start time')
        if end_idx < start_idx or end_idx > len(self.data):
            Message('End time out of range', 'e').on_file(log)
            raise ValueError('Invalid end time')
        if (end_time - start_time) < 3:
            Message('At least 3 seconds required to sample noise', 'w').on_file(log)

        noise_sample = self.data[start_idx:end_idx]
        # Perform noise reduction
        self.data = nr.reduce_noise(y=self.data, y_noise=noise_sample, sr=self.rate)


    def plot_max_amplitude_limits(self) -> None:
        """
        Plot waveform with lines at max, min, and clipping thresholds ±1.
        """
        top = np.max(self.data)
        bottom = np.min(self.data)
        functions.plot_audio_waveform_with_lines(
            self.data,
            horizontal_lines=[top, bottom, 1, -1]
        )


    def plot_average_values(self) -> None:
        """
        Recomputes average positive and negative amplitudes and plots them.
        """
        positives = [v for v in self.data if v > 0]
        negatives = [v for v in self.data if v < 0]
        avg_pos = sum(positives) / len(positives) if positives else 0
        avg_neg = sum(negatives) / len(negatives) if negatives else 0
        self._mid_amplitude = (avg_pos - avg_neg) / 2

        functions.plot_audio_waveform_with_lines(
            self.data,
            horizontal_lines=[avg_pos, avg_neg]
        )


    def plot_long_silences(
        self,
        threshold: Optional[float] = None,
        min_duration: Optional[Union[int, float]] = None
    ) -> None:
        """
        Finds silent segments longer than min_duration (seconds) below threshold
        and overlays vertical lines at their start/end points.
        """
        if threshold is None:
            threshold = 0.5 * self._mid_amplitude
        if min_duration is None:
            min_duration = 0.1 * len(self.data) / self.rate

        min_samples = int(min_duration * self.rate)
        borders: List[int] = []
        is_silent = abs(self.data[0]) < threshold

        if is_silent:
            borders.append(0)

        # Detect transitions in and out of silence
        for idx, sample in enumerate(self.data):
            currently_silent = abs(sample) < threshold
            if currently_silent and not is_silent:
                borders.append(idx)
                is_silent = True
            elif not currently_silent and is_silent:
                borders.append(idx)
                is_silent = False

        if is_silent:
            borders.append(len(self.data) - 1)

        # Filter only long silent segments
        valid_borders: List[int] = []
        for i in range(0, len(borders) - 1, 2):
            start, end = borders[i], borders[i + 1]
            if (end - start) >= min_samples:
                valid_borders.extend([start, end])

        functions.plot_audio_waveform_with_lines(self.data, vertical_lines=valid_borders)


    def play_audio(self) -> None:
        """
        Plays the current audio data through the default output device.
        """
        sd.play(self.data, self.rate)
        sd.wait()