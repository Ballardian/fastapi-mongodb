from typing import List
from pydantic import ConfigDict, BaseModel

from addresses.models import AddressModel
from affiliations.models import AffiliationsModel
from constants import Status
from hcps.constants import CountryIsoCode


class HcpSummaryModel(BaseModel):
    """
    Container for a single Hcp record without Affiliations.
    """

    id: int
    name: str
    address_link: AddressModel
    status: Status
    countryIsoCode: CountryIsoCode
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class HcpDetailModel(BaseModel):
    """
    Container for a single Hcp record with Affiliations.
    """

    id: int
    name: str
    address_link: AddressModel
    status: Status
    countryIsoCode: CountryIsoCode
    affiliations: List[AffiliationsModel] | None = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class HcpCollection(BaseModel):
    """
    A container holding a list of `HcpSummaryModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    hcps: List[HcpSummaryModel]
