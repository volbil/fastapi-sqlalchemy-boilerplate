from app import constants
import math


# Helper function for toroise pagination
def pagination(page, limit=constants.SEARCH_RESULT_LIMIT):
    offset = (limit * (page)) - limit
    return limit, offset


# Helper function to make pagication dict for api
def pagination_dict(total, page, limit):
    return {
        "pages": math.ceil(total / limit),
        "total": total,
        "page": page,
    }
