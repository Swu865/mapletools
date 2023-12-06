import re

class For_Stats():
    def __init__(self, OCR_stats: list[str], DESIRED_stats: list[dict[str, int]]):
        self.OCR_stats = OCR_stats
        self.DESIRED_stats = DESIRED_stats  # Now a list of dictionaries

    def parse_OCR_result(self) -> dict[str, int]:
        Stats_dict = {}
        str_pattern = r"([a-zA-Z\s]+): \+(\d+)%"
        for stat in self.OCR_stats:
            match = re.match(str_pattern, stat)
            if match:
                stat_name = match.group(1).strip()  # Strip to remove any leading/trailing spaces
                stat_value = int(match.group(2))
                Stats_dict[stat_name] = Stats_dict.get(stat_name, 0) + stat_value

        return Stats_dict

    def check_stat(self, OCR_stats: dict[str, int]) -> bool:
        for desired_stats in self.DESIRED_stats:  # Iterate through each DESIRED_stats dict
            if all(OCR_stats.get(stat_name, 0) >= stat_threshold for stat_name, stat_threshold in desired_stats.items()):
                return True  # Return True if any DESIRED_stats is fully met
        return False  # Return False if none of the DESIRED_stats are met

    def main(self) -> bool:
        OCR_dict = self.parse_OCR_result()
        match_desired_stats = self.check_stat(OCR_dict)
        return match_desired_stats
