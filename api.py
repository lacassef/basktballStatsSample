import requests
from requests.adapters import HTTPAdapter, Retry

# API endpoints configuration

your_key = "your_api_key"
domain = "basketapi1.p.rapidapi.com"

session = requests.Session()

# It's always good to retry when API is temporarly unavailable
retries = Retry(total=5,
                backoff_factor=10,
                status_forcelist=[500, 502, 503, 504])
# Control timeout seconds, set to None to defaults
timeout_secs = 100

session.mount('https://', HTTPAdapter(max_retries=retries))
session.headers = {
    "X-RapidAPI-Key": f"{your_key}",
    "X-RapidAPI-Host": f"{domain}"
}


# The functions

def get_league_seasons(unique_tournament_id: int):
    req = session.get(url=f'https://{domain}/api/basketball/tournament/{unique_tournament_id}/seasons',
                      timeout=timeout_secs)
    # print(req.status_code)
    return req.json()


def get_league_last_matches(unique_tournament_id: int, season_id: int, page: int):
    req = session.get(
        url=f'https://{domain}/api/basketball/tournament/{unique_tournament_id}/season/{season_id}/matches/last/{page}',
        timeout=timeout_secs)
    # print(req.status_code)
    return req.json()


def get_match_statistics(match_id: int):
    req = session.get(url=f'https://{domain}/api/basketball/match/{match_id}/statistics',
                      timeout=timeout_secs)
    # print(req.status_code)
    return req.json()


def get_pre_match_form(match_id: int):
    req = session.get(url=f'https://{domain}/api/basketball/match/{match_id}/form',
                      timeout=timeout_secs)
    # print(req.status_code)
    return req.json()


def get_match_lineups(match_id: int):
    req = session.get(url=f'https://{domain}/api/basketball/match/{match_id}/lineups',
                      timeout=timeout_secs)
    # print(req.status_code)
    return req.json()


def get_match(match_id: int):
    req = session.get(url=f'https://{domain}/api/basketball/match/{match_id}',
                      timeout=timeout_secs)
    # print(req.status_code)
    return req.json()
