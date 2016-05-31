from channel import Channel


class Lineup(list):
    def __init__(self, *args, **kwargs):
        super(Lineup, self).__init__(*args, **kwargs)

    def get_channel_numbers(self):
        return [channel.guide_number for channel in self]

    @classmethod
    def from_iterable(cls, iterable):
        return cls([Channel.from_dict(dct) for dct in iterable])
