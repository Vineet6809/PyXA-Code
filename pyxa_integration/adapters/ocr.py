from __future__ import annotations

import asyncio
import importlib

from pyxa_integration.errors import AdapterUnavailableError
from pyxa_integration.utils.telemetry import get_telemetry_recorder, now_ms


class WindowsOcrAdapter:
    """OCR adapter path with WinRT implementation and tesseract fallback."""

    def recognize_png_bytes(self, png_bytes: bytes, allow_fallback: bool = True) -> str:
        recorder = get_telemetry_recorder()
        start = now_ms()
        status = "ok"
        backend = "none"
        try:
            if not png_bytes:
                return ""

            if self.check_runtime_available(silent=True):
                backend = "winrt"
                return self._winrt_ocr(png_bytes)

            if not allow_fallback:
                raise AdapterUnavailableError("No OCR backend available")

            backend = "tesseract"
            return self._fallback_tesseract_ocr(png_bytes)
        except Exception:
            status = "error"
            raise
        finally:
            recorder.record("adapter.ocr", now_ms() - start, status, {"backend": backend})

    def _winrt_ocr(self, png_bytes: bytes) -> str:
        media_ocr = importlib.import_module("winrt.windows.media.ocr")
        imaging = importlib.import_module("winrt.windows.graphics.imaging")
        streams = importlib.import_module("winrt.windows.storage.streams")

        async def _run() -> str:
            stream = streams.InMemoryRandomAccessStream()
            writer = streams.DataWriter(stream)
            writer.write_bytes(png_bytes)
            await writer.store_async()
            writer.detach_stream()
            stream.seek(0)

            decoder = await imaging.BitmapDecoder.create_async(stream)
            software_bitmap = await decoder.get_software_bitmap_async()
            engine = media_ocr.OcrEngine.try_create_from_user_profile_languages()
            if engine is None:
                raise AdapterUnavailableError("Unable to create WinRT OcrEngine")

            result = await engine.recognize_async(software_bitmap)
            return result.text.strip()

        return self._run_async(_run)

    def _run_async(self, coro_fn):
        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                new_loop = asyncio.new_event_loop()
                try:
                    return new_loop.run_until_complete(coro_fn())
                finally:
                    new_loop.close()
        except RuntimeError:
            pass

        return asyncio.run(coro_fn())

    def _fallback_tesseract_ocr(self, png_bytes: bytes) -> str:
        pillow_image_module = importlib.import_module("PIL.Image")
        io_module = importlib.import_module("io")
        pytesseract = importlib.import_module("pytesseract")

        image = pillow_image_module.open(io_module.BytesIO(png_bytes)).convert("RGB")
        return pytesseract.image_to_string(image).strip()

    def check_runtime_available(self, silent: bool = False) -> bool:
        try:
            importlib.import_module("winrt.windows.media.ocr")
            importlib.import_module("winrt.windows.graphics.imaging")
            importlib.import_module("winrt.windows.storage.streams")
            return True
        except ModuleNotFoundError:
            if silent:
                return False
            raise AdapterUnavailableError("winrt-Windows.Media.Ocr dependencies are not installed")
