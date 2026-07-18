class NotFoundError(Exception):
    def __init__(self, entity: str, id: str):
        self.entity = entity
        self.id = id
        super().__init__(f"{entity} with ID {id} not found.")


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
