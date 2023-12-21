from .querries import BaseTable

class MemberTable(BaseTable):
    def __init__(self) -> None:
        super().__init__('member')
    
    def reset_limit(self):
        self.client.rpc('daily_reset', {}).execute()
        

class GiveAwayTable(BaseTable):
    def __init__(self) -> None:
        super().__init__("give_away")

    def update(self):
        raise NotImplementedError("Update method hasn't been implemented yet.")