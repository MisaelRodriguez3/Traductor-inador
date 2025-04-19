from pathlib import Path
import sys
from typing import Union

def resource_path(relative_path: Union[str, Path]) -> str:
    """Obtiene la ruta absoluta para recursos empaquetados o en desarrollo"""
    base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))
    return str(base_path / relative_path)