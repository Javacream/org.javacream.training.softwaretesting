class StoreService:
    def __init__(self):
        self.store = {}

    def get_stock(self, category, item):
        category_dict = self.store.get(category)
        if not category_dict:
            return 0
        return category_dict.get(item, 0)

    def set_stock(self, category, item, stock):
        category_dict = self.store.setdefault(category, {})
        category_dict[item] = stock
