from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class HotkeyConfig:
    combo: str = "<ctrl>+<f12>"


class KillSwitch:
    """Registers a global hotkey and triggers a stop callback."""

    def __init__(self, on_trigger: Callable[[], None], config: HotkeyConfig | None = None) -> None:
        self.on_trigger = on_trigger
        self.config = config or HotkeyConfig()
        self._listener = None

    def start(self) -> None:
        keyboard_module = importlib.import_module("pynput.keyboard")
        hotkeys = keyboard_module.GlobalHotKeys({self.config.combo: self.on_trigger})
        hotkeys.start()
        self._listener = hotkeys

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
