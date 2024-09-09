class RoundRobinScheduler:
    def __init__(self, sellers):
        self.sellers = sellers

    def get_sellers_for_page(self, page, per_page):
        total_sellers = len(self.sellers)
        start_index = (page - 1) * per_page % total_sellers
        sellers = [self.sellers[(start_index + i) % total_sellers] for i in range(per_page)]
        return sellers
