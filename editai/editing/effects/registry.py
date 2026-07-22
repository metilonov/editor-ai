from __future__ import annotations

from importlib import import_module


def effect_filter(key:str,**values:float)->str:
    try: module=import_module(f"editai.editing.effects.{key}")
    except ModuleNotFoundError: return ""
    template=str(getattr(module,"FILTER_TEMPLATE","") or "")
    return template.format(**values) if template else ""
