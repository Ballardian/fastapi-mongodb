from typing import Optional, List
from pydantic import ConfigDict, BaseModel

from constants import Status
from affiliations.constants import Type


class AffiliationsModel(BaseModel):
    """
    Container for a single Affiliation record.
    """

    # TODO change parent/child_link to HcpSummaryModel - currently causes circular import
    # Note: we don't need these fields
    # id: int
    # parent_link: int | dict
    child_link: int | dict
    status: Status
    type: Type
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
