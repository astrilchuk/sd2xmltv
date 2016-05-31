import logging
from programdescription import ProgramDescription


class ProgramDescriptionList(list):
    def __init__(self, *args, **kwargs):
        super(ProgramDescriptionList, self).__init__(*args, **kwargs)

    def languages(self):
        return list({description.language for description in self})

    def ordered_by_text_length(self, reverse=False):
        return sorted(self, key=lambda description: len(description.text), reverse=reverse)

    def get_shortest_text(self, language="en"):
        return next((description.text for description in self.ordered_by_text_length(False) if description.language == language), None)

    def get_longest_text(self, language="en"):
        return next((description.text for description in self.ordered_by_text_length(True) if description.language == language), None)

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramDescriptionList
        """

        :param dct:
        :return:
        """
        program_description_list = cls()

        if "description100" in dct:
            program_description_list.extend(ProgramDescription.from_iterable(dct.pop("description100")))

        if "description1000" in dct:
            program_description_list.extend(ProgramDescription.from_iterable(dct.pop("description1000")))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramDescriptions: %s", ", ".join(dct.keys()))

        return program_description_list
