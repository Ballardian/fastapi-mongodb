from fastapi import APIRouter, Request, HTTPException

from hcps.models import HcpSummaryModel, HcpDetailModel, HcpCollection

router = APIRouter()


@router.get(
    "/hcps/",
    response_description="List all hcp",
    response_model=HcpCollection,
    response_model_by_alias=False,
)
async def list_hcps(request: Request, search: str | None = None):
    """
    List all of the hcp data in the database.
    Optional search query params to filter results.
    Notes:
    1. can currently only search by name.
    2. returning an empty filtered list is valid response


    The response is unpaginated and limited to 1000 results.
    """

    # TODO expand search criteria functionality to use fuzzysearch
    search_criteria = {"name": search} if search else {}

    hcp_list = (
        await request.app.hcp_collection.find(search_criteria, {"affiliations": 0})
        .sort({"id": 1})
        .to_list(1000)
    )
    return HcpCollection(hcps=hcp_list)


@router.get(
    "/hcps/{hcp_id}",
    response_description="Single detailed hcp",
    response_model=HcpDetailModel,
    response_model_by_alias=False,
)
async def get_hcp(hcp_id: int, request: Request):
    """
    Get a single HCP
    """

    if (hcp := await request.app.hcp_collection.find_one({"id": hcp_id})) is not None:
        return hcp
    else:
        # Note: Exception has to be raised in this way instead of try/except
        # because ResponseValidationError (object not found) is only raised during the return
        # and not during the query

        # send/log to DD etc
        raise HTTPException(
            status_code=404, detail=f"[get_hcp()] Hcp {hcp_id} not found"
        )
