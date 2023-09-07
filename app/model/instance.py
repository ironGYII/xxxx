class Instance:
    def __init__(self, addr, lease_id, start_time, end_time, device_id):
        self.addr = addr
        self.lease_id = lease_id
        self.start_time = start_time
        self.end_time = end_time
        self.device_id = device_id

    @classmethod
    def init_from_contract(cls, addr, lease_id, start_time, end_time, device_id):
        # demo '0xA24d5b9CEFDe16cEfB488040B4f7de99e4dE92bB', 2, 1694053093, 1694053103, 2
        return Instance(addr, lease_id, start_time, end_time, device_id)

    def is_recipient(self):
        pass

    def is_owner(self):
        pass


class Billing:
    def __init__(self, addr, bill_id, lease_id, provider_blocked_fund, recipient_blocked_funds, amount, status, bill_type):
        self.addr = addr
        self.bill_id = bill_id
        self.lease_id = lease_id
        self.provider_blocked_fund = provider_blocked_fund
        self.recipient_blocked_funds = recipient_blocked_funds
        self.amount = amount
        self.status = status
        self.bill_type = bill_type

    @classmethod
    def init_from_contract(cls, addr, bill_id, lease_id, provider_blocked_fund, recipient_blocked_funds, amount, status, bill_type):
        return Billing(addr, bill_id, lease_id, provider_blocked_fund, recipient_blocked_funds, amount, status, bill_type)

    def data(self, instance, machine):
        return dict(instance_id=instance.lease_id, device=machine.market_id, amount=self.amount, recipient_address=self.addr, provider_address=machine.pub_key, setlle_at=instance.end_time, start_time=instance.start_time)
