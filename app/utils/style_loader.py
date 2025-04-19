from pathlib import Path
from app.utils.get_resource import resource_path


def load_stylesheet(filename: str, folder: str = "") -> str:
    """
    Carga estilos desde la estructura de carpetas organizada.
    
    Ejemplos:
    - load_stylesheet("base.qss")  # styles/base.qss
    - load_stylesheet("botones.qss", "widgets")  # styles/widgets/botones.qss
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