from editai.editing.effects.base import Effect

EFFECT = Effect("fade", "Плавное появление/исчезновение")
FILTER_TEMPLATE = 'fade=t=in:st=0:d={transition},fade=t=out:st={fade_out}:d={transition}'
