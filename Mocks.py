class Mocks:
    def __init__(self):
        self.mocks = {}

    def get_award_categories(self):
        # TODO - implement actual mock
        if 'AwardCategoriesMock' not in self.mocks:
            self.mocks['AwardCategoriesMock'] = []

        return self.mocks['AwardCategoriesMock']

    def get_award_names(self):
        # TODO - implement actual mock
        if 'AwardNamesMock' not in self.mocks:
            self.mocks['AwardNamesMock'] = []

        return self.mocks['AwardNamesMock']

    def get_presenter_for_award(self):
        # TODO - implement actual mock
        if 'AwardPresentersMock' not in self.mocks:
            self.mocks['AwardPresentersMock'] = []

        return self.mocks['AwardPresentersMock']

    def get_winner_for_award(self):
        # TODO - implement actual mock
        if 'AwardWinnersMock' not in self.mocks:
            self.mocks['AwardWinnersMock'] = []

        return self.mocks['AwardWinnersMock']

    def get_nominees_for_award(self, award):
        # TODO - implement actual mock
        if 'AwardNomineesMock' not in self.mocks:
            self.mocks['AwardNomineesMock'] = []

        return self.mocks['AwardNomineesMock']

    def get_hosts(self):
        # TODO - implement actual mock
        if 'HostsMock' not in self.mocks:
            self.mocks['HostsMock'] = []

        return self.mocks['HostsMock']
