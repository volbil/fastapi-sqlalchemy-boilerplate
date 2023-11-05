from app import constants
from app import utils


def test_pagination():
    page = 3
    total = 24

    limit, offset = utils.pagination(page, constants.SEARCH_RESULT_LIMIT)

    assert limit == 12
    assert offset == 24

    assert {"page": 3, "pages": 2, "total": 24} == utils.pagination_dict(
        total, page, limit
    )
