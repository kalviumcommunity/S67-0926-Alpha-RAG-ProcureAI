from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Final
from uuid import uuid4

from fastapi import UploadFile


CHUNK_SIZE: Final = 1024 * 1024


class FileSizeLimitExceeded(Exception):
    pass


@dataclass(frozen=True)
class StoredFile:
    relative_path: str
    absolute_path: Path
    file_size: int


async def save_upload_file(
    upload_file: UploadFile,
    extension: str,
    upload_directory: Path,
    max_size_bytes: int,
) -> StoredFile:
    upload_directory.mkdir(parents=True, exist_ok=True)
    stored_path = upload_directory / f"{uuid4()}{extension}"
    file_size = 0

    try:
        with stored_path.open("wb") as destination:
            while chunk := await upload_file.read(CHUNK_SIZE):
                file_size += len(chunk)
                if file_size > max_size_bytes:
                    raise FileSizeLimitExceeded
                await asyncio.to_thread(destination.write, chunk)
    except Exception:
        stored_path.unlink(missing_ok=True)
        raise

    return StoredFile(
        relative_path=str(Path("uploads") / stored_path.name),
        absolute_path=stored_path,
        file_size=file_size,
    )


async def delete_stored_file(
    stored_file: StoredFile,
    missing_ok: bool = False,
) -> None:
    await asyncio.to_thread(
        stored_file.absolute_path.unlink,
        missing_ok=missing_ok,
    )


def stored_file_from_reference(
    relative_path: str,
    upload_directory: Path,
) -> StoredFile:
    return StoredFile(
        relative_path=relative_path,
        absolute_path=upload_directory / Path(relative_path).name,
        file_size=0,
    )
