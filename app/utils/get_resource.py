import sys
from pathlib import Path

def resource_path(relative_path: str | Path) -> str:
    """Get absolute path to resource for both packaged and development environments.
    
    Resolves resource paths in a way that works:
    - During normal Python execution
    - When frozen as a single-file bundle using PyInstaller
    
    Args:
        relative_path (str | Path): Resource path relative to either:
            - The application root in development mode
            - The temp bundle directory when frozen
    
    Returns:
        str: Absolute filesystem path as string
        
    Examples:
        # Development environment
        >>> resource_path('app/assets/icon.png')
        '/home/project/app/assets/icon.png'
        
        # Packaged executable
        >>> resource_path('app/assets/icon.png')
        '/tmp/_MEI123456/app/assets/icon.png'
    
    Notes:
        Uses PyInstaller's runtime temp directory detection via sys._MEIPASS
        Fallback to 3-level parent directory structure assumption when not frozen
    """
    base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent.parent))
    return str(base_path / relative_path)