from pydantic import ConfigDict, BaseModel

from constants import Status


class AddressModel(BaseModel):
    """
    Container for a single Address record.
    """

    # Note: we don't need commented out fields
    # id: int
    # parent_link: int
    # parent_type: str
    addr1: str
    addr2: str | None = None
    city: str
    state: str
    zip: str
    status: Status
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
