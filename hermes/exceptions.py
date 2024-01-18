class MissingFieldError(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"Field: {field_name} is missing and is mandatory")


class NoRecipientError(Exception):
    def __init__(self):
        super().__init__("At least one recipient email should be specified")
