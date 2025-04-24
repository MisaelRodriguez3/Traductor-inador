from pathlib import Path
from app.utils.get_resource import resource_path


def load_stylesheet(filename: str, folder: str = "") -> str:
    """Loads QSS stylesheets from organized directory structure.
    
    Handles stylesheet loading for both development and packaged environments
    using resource path resolution. Returns empty string on failure.

    Args:
        filename (str): Name of the stylesheet file with extension
        folder (str, optional): Optional subdirectory within styles directory. Defaults to "".

    Returns:
        str: Stylesheet content as string. Empty string if file not found.

    Raises:
        FileNotFoundError: If requested stylesheet doesn't exist
        IOError: If file cannot be read
        PermissionError: If file access is denied

    Examples:
        # Load base stylesheet
        >>> load_stylesheet("base.qss")
        "QWidget { background: white; }"

        # Load button styles from widgets subdirectory
        >>> load_stylesheet("buttons.qss", "widgets")
        "QPushButton { color: blue; }"

    Notes:
        - Uses app/styles as root directory for styles
        - Requires .qss file extension but doesn't validate contents
        - Prints error messages to console but doesn't raise exceptions
        - Designed to fail gracefully for missing stylesheets
    """
    try:
        style_path = Path("app/styles") 
        if folder:
            style_path = style_path / folder
        style_path = style_path / filename
        
        full_path = resource_path(style_path)
        
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading styles: {str(e)}")
        return ""