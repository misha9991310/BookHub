from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateReview:
    book: int
    rating: int
    text: str | None


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateReview:
    book: int
    rating: int
    text: str | None

