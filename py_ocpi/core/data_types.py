"""
OCPI data types based on https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc
"""

from datetime import datetime, timezone
from typing import Type
from pydantic.fields import ModelField

from .config import settings


class StringBase(str):
    """
    Case sensitive String. Only printable UTF-8 allowed.
    (Non-printable characters like:
    Carriage returns, Tabs, Line breaks, etc are not allowed)
    """

    max_length: int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=["String"],
        )

    @classmethod
    def validate(cls, v, field: ModelField):
        if not isinstance(v, str):
            raise TypeError(f"excpected string but received {type(v)}")
        try:
            v.encode("UTF-8")
        except UnicodeError as e:
            raise ValueError("invalid string format") from e
        if len(v) > cls.max_length:
            raise ValueError(
                f"{field.name} length must be lower or equal to {cls.max_length}"
            )
        return cls(v)

    def __repr__(self):
        return f"String({super().__repr__()})"


class String:
    def __new__(cls, max_length: int = 255) -> Type[str]:  # type: ignore
        return type("String", (StringBase,), {"max_length": max_length})


class CiStringBase(str):
    """
    Case Insensitive String. Only printable ASCII allowed.
    (Non-printable characters like:
    Carriage returns, Tabs, Line breaks, etc are not allowed)
    """

    max_length: int

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=["string"],
        )

    @classmethod
    def validate(cls, v, field: ModelField):
        if not isinstance(v, str):
            raise TypeError(f"excpected string but received {type(v)}")
        if not v.isascii():
            raise ValueError("invalid cistring format")
        if len(v) > cls.max_length:
            raise ValueError(
                f"{field.name} length must be lower or equal to {cls.max_length}"
            )

        if settings.CI_STRING_LOWERCASE_PREFERENCE:
            return cls(v.lower())

        return cls(v.upper())

    def __repr__(self):
        return f"CiString({super().__repr__()})"


class CiString:
    def __new__(cls, max_length: int = 255) -> type:  # type: ignore
        return type("CiString", (CiStringBase,), {"max_length": max_length})


class URL(str):
    """
    An URL a String(255) type following the
    http://www.w3.org/Addressing/URL/uri-spec.html
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=["http://www.w3.org/Addressing/URL/uri-spec.html"],
        )

    @classmethod
    def validate(cls, v, field: ModelField):
        v = String(255).validate(v, field)  # type: ignore
        return cls(v)

    def __repr__(self):
        return f"URL({super().__repr__()})"


class DateTime(str):
    """
    All timestamps are formatted as string(25) following RFC 3339,
    with some additional limitations.
    All timestamps SHALL be in UTC.
    The absence of the timezone designator implies a UTC timestamp.
    Fractional seconds MAY be used.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[
                (
                    datetime.now(timezone.utc)
                    .isoformat(timespec="seconds")
                    .replace("+00:00", "Z")
                ),
            ],
        )

    @classmethod
    def validate(cls, v):
        if v.endswith("Z"):
            v = f"{v[:-1]}+00:00"

        try:
            formatted_v = datetime.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid RFC 3339 timestamp: {v}") from e

        return cls(
            formatted_v.isoformat(timespec="seconds").replace("+00:00", "Z")
        )

    def __repr__(self):
        return f"DateTime({super().__repr__()})"


class DisplayText(dict):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[{"language": "en", "text": "Standard Tariff"}],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, dict):
            raise TypeError(f"excpected dict but received {type(v)}")
        if "language" not in v:
            raise TypeError('property "language" required')
        if "text" not in v:
            raise TypeError('property "text" required')
        if len(v["text"]) > 512:
            raise TypeError("text too long")
        return cls(v)

    def __repr__(self):
        return f"DateTime({super().__repr__()})"


class Number(float):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[],
        )

    @classmethod
    def validate(cls, v):
        if not any([isinstance(v, float), isinstance(v, int)]):
            TypeError(f"excpected float but received {type(v)}")
        return cls(float(v))

    def __repr__(self):
        return f"Number({super().__repr__()})"


class Price(dict):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[{"excl_vat": 1.0000, "incl_vat": 1.2500}],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, dict):
            raise TypeError("dictionary required")
        if "excl_vat" not in v:
            raise TypeError('property "excl_vat" required')
        return cls(v)

    def __repr__(self):
        return f"Price({super().__repr__()})"
