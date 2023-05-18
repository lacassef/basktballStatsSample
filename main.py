# Press the green button in the gutter to run the script.
import api

if __name__ == '__main__':
    # NBA id is 132
    unique_tournament_id = 132

    # getting the seasons array from the response
    seasons = api.get_league_seasons(unique_tournament_id)['seasons']

    # here we're just slicing the seasons array to the first 3 seasons (the returned result is in descending order)
    # so we are getting the most recent seasons
    for i in seasons[:3]:
        season_id = i['id']


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
