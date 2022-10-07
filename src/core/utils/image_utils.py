import base64
import os
from typing import Optional, TypedDict, Union

from PIL import Image
from sqlalchemy_utils import URLType

from config import ROOT_DIR
from src.core.types.exceptions_type import BadRequestException


class ValidImageResponse(TypedDict):
    image: bytes
    format: str


class ImageUtils:
    def __init__(self, path: str):
        self.path = ROOT_DIR + os.path.join(path)

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    @staticmethod
    def valid_image64(image64: Optional[bytes]) -> Optional[ValidImageResponse]:
        if image64:
            if image64.split(str.encode(";"))[0] in (
                str.encode("data:image/jpeg"),
                str.encode("data:image/png"),
            ):
                return ValidImageResponse(
                    image=image64.split(str.encode(","))[1],
                    format="jpeg" if str.encode("jpeg") in image64 else "png",
                )
            else:
                raise BadRequestException("Invalid image format.")

        return None

    def get_image(self, filename: Union[str, URLType] = None) -> Optional[bytes]:
        if filename:
            return base64.b64encode(Image.open(f"{self.path}/{filename}").tobytes())

        return None

    def save_image(self, user_id: str, image: Optional[ValidImageResponse]) -> str:
        if image:
            img_data = base64.b64decode(image["image"])
            filename = f"{user_id}.{image['format']}"
            with open(f"{self.path}/{filename}", "wb") as f:
                f.write(img_data)

        return filename if "filename" in locals() else None

    def delete_image(self, filename: str = None) -> bool:
        try:
            if filename:
                os.remove(f"{self.path}/{filename}")
        except Exception as e:
            raise e

        return True
