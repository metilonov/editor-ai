from editai.editing.effects.base import Effect

EFFECT = Effect("shake", "Мягкая имитация shake")
FILTER_TEMPLATE = "crop=iw-8:ih-8:4+4*sin(18*t):4+4*cos(15*t),scale=1080:1920"
