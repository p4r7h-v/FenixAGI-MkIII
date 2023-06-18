class CustomerBehaviorTracker:
    def __init__(self):
        self.customer_behavior = {}

    def track_behavior(self, customer_id, page_name):
        if customer_id not in self.customer_behavior:
            self.customer_behavior[customer_id] = {page_name: 1}
        else:
            if page_name in self.customer_behavior[customer_id]:
                self.customer_behavior[customer_id][page_name] += 1
            else:
                self.customer_behavior[customer_id][page_name] = 1

    def get_behavior(self, customer_id):
        if customer_id in self.customer_behavior:
            return self.customer_behavior[customer_id]
        else:
            return "No behavior tracked for Customer ID: {}".format(customer_id)


tracker = CustomerBehaviorTracker()
tracker.track_behavior('customer1', 'homepage')
tracker.track_behavior('customer1', 'productpage')
tracker.track_behavior('customer1', 'homepage')
print(tracker.get_behavior('customer1'))