from datetime import datetime
import os
import sys

# Get the current timestamp with milliseconds
def get_now() -> str:
    """Returns the current timestamp with milliseconds."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

class Logger:
    """Manages the creation, initialization, and writing to the log file."""
    
    def __init__(self, directory: str, filename: str, format: str) -> None:
        # Check if format is a string
        if not isinstance(format, str):
            raise TypeError('Format should be a string')
        # Check if directory is a string
        if not isinstance(directory, str):
            raise TypeError('Directory should be a string')
        # Check if filename is a string
        if not isinstance(filename, str):
            raise TypeError('Filename should be a string')
        # Check if format is either 'md' or 'log'
        if format not in ('md', 'log'):
            raise ValueError("Format should be 'md' or 'log'")
        
        self._format = format
        self._filename = filename
        
        # Set the directory path based on the platform or use the provided directory
        if directory == 'default':
            if sys.platform == 'win32':
                self._directory = os.path.expandvars('%localappdata%/a4a')
            elif sys.platform == 'linux':
                self._directory = os.path.expanduser('~/.a4a')
            else:
                self._directory = os.path.join(os.path.expanduser('~'), '.a4a')
        else:
            self._directory = directory
        
        # Create the directory if it doesn't exist
        os.makedirs(self._directory, exist_ok=True)
        
        # Construct the full file path
        self._filepath = os.path.join(self._directory, f"{self._filename}.{self._format}")
        
        # Get the current timestamp
        timestamp = get_now()
        
        # Initialize the log file with a timestamp
        with open(self._filepath, 'w') as file:
            file.write(f"Initialized: {timestamp}\n")
    
    # Property to get the log file path
    @property
    def path(self) -> str:
        return self._filepath
    
    # Property to get the log file extension
    @property
    def extension(self) -> str:
        return self._format

class Message:
    """Represents a log message with a level and text."""
    
    # Dictionary mapping level codes to their full names
    LEVEL_NAMES = {
        'd': 'Debug',
        'i': 'Info',
        'w': 'Warning',
        'e': 'Error'
    }
    
    def __init__(self, message: str, level: str = 'd'):
        # Initialize message text and level
        self._message = str(message)
        self._level = level
        if not isinstance(level, str):
            raise TypeError('Level should be a string')
        if level not in ('d', 'i', 'w', 'e'):
            raise ValueError("Level must be one of 'd', 'i', 'w', 'e'")
    
    # Property to get the message text
    @property
    def message(self) -> str:
        return self._message
    
    # Property to get the message level
    @property
    def level(self) -> str:
        return self._level
    
    # Format the message based on the specified log format
    def format_for_log(self, log_format: str) -> str:
        if log_format == 'md':
            return f'\n## [{self.LEVEL_NAMES.get(self.level)}]\n{self.message}\n'
        else:
            return f'[{self.LEVEL_NAMES.get(self.level)}]\t{self.message}\n'
    
    # Write the formatted message to the log file
    def on_file(self, logger: Logger) -> None:
        line = self.format_for_log(logger.extension)
        with open(logger.path, 'a') as file:
            file.write(line)
    
    # Return a string representation of the message
    def __str__(self) -> str:
        return f'[{self.LEVEL_NAMES.get(self.level)}]\t{self.message}'