from ..document import CodeBlock
from .base import HookBase


class Hook(HookBase):
    def on_read(self, code: CodeBlock):
        lines = code.source.splitlines()
        if len(lines) == 0:
            return

        if lines[0].startswith("#!"):
            code.header = lines[0]
            code.source = "\n".join(lines[1:])

        return
