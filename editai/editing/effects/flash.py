from editai.editing.effects.base import Effect

EFFECT = Effect("flash", "Короткая вспышка")
FILTER_TEMPLATE = 'eq=brightness=0.02*sin(12*t)'
