from domain.exceptions import InvalidTaskName


class TaskValidator:
    @staticmethod
    def validate_name(name: str) -> None:
        if len(name) > 10:
            raise InvalidTaskName
