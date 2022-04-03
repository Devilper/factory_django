#  分页 current_page--当前页码  per_page---每页条数
from restapi.schema import Pagination


class PageUtil:
    def __init__(self, page, page_size):
        try:
            self.page = int(page)
        except Exception as e:
            self.page = 1
        self.page_size = page_size

    def start(self):
        return (self.page - 1) * self.page_size

    def end(self):
        return self.page * self.page_size


def handle_pagination(page, page_size, total):
    return Pagination(
        page=page,
        page_size=page_size,
        total=total
    )
