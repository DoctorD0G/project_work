class InvalidTaskName(Exception):
    def __init__(self):
        super().__init__("Невалидное имя задачи")


class DbObjExistsException(Exception): ...


class MultipleResultException(Exception): ...
