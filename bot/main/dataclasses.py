from datetime import datetime
from dataclasses import dataclass


@dataclass
class Article:
    name: str
    url: str

    def __str__(self):
        return f"Article({self.name}, {self.url}, {self.time_posted})"

    def __repr__(self):
        return f"Article({self.name}, {self.url}, {self.time_posted})"


@dataclass
class Match:
    time_matches: datetime
    match_info: str
    team_names: str
    tournament_name: str
    url_match: str
    url_analytic: str

    def __str__(self):
        return f"Match({self.team_names}, {self.tournament_name})"

    def __repr__(self):
        return f"Match({self.team_names}, {self.tournament_name})"


@dataclass
class Result:
    team_names: str
    tournament_name: str
    match_result: str
    url_match: str

    def __str__(self):
        return f"Result({self.team_names}, {self.tournament_name})"

    def __repr__(self):
        return f"Result({self.team_names}, {self.tournament_name})"

