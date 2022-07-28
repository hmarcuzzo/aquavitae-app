from datetime import date, datetime

from src.core.common.dto.exception_response_dto import DetailResponseDto


class JsonUtils:
    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, DetailResponseDto):
            return obj.__dict__
        raise TypeError("Type %s not serializable" % type(obj))
