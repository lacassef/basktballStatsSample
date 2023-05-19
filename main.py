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
        # take care with this infinite loop
        last_page = False
        page = 0

        while not last_page:
            try:
                matches = api.get_league_last_matches(unique_tournament_id, season_id, page)
            except Exception as exception:
                # print(exception)
                break

            try:
                events, has_next_page = matches["events"], matches["hasNextPage"]
            except Exception as exception:
                # print(exception)
                break

            if len(events) == 0:
                break

            for event in events:
                statistics = api.get_match_statistics(event["id"])
                print(statistics)

            if has_next_page:
                page += 1
            else:
                last_page = True



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
