import api


def match_processing(event):
    event_id = event["id"]

    # Match stats
    statistics = api.get_match_statistics(event_id)

    # We're just printing the stats, but you can do anything with the event and statistics like saving
    # to your database
    print(statistics)

    # Getting all other info
    lineups = api.get_match_lineups(event_id)
    form = api.get_pre_match_form(event_id)
    match = api.get_match(event_id)

    # Let's get all needed variables from match details

    # Event start timestamp (in seconds)
    startTimestamp = match["startTimestamp"]

    # Team names
    homeTeamName, awayTeamName = match["homeTeam"]["name"], match["awayTeam"]["name"]

    # Home team scores
    homeTeamFinalScore, homeTeamP1Score, homeTeamP2Score, homeTeamP3Score, homeTeamP4Score = match["homeScore"][
        "current"], match["homeScore"]["period1"], match["homeScore"]["period2"], match["homeScore"]["period3"], \
    match["homeScore"]["period4"]

    try:
        homeTeamOvertimeScore = match["homeScore"]["overtime"]
    except:
        #     No overtime logic
        pass

    # Away team scores
    awayTeamFinalScore, awayTeamP1Score, awayTeamP2Score, awayTeamP3Score, awayTeamP4Score = match["awayScore"][
        "current"], match["awayScore"]["period1"], match["awayScore"]["period2"], match["awayScore"]["period3"], \
    match["awayScore"]["period4"]

    try:
        awayTeamOvertimeScore = match["awayScore"]["overtime"]
    except:
        #     No overtime logic
        pass

    # Team standings
    homeStandings, awayStandings = form["homeTeam"]["position"], form["awayTeam"]["position"]

    # Teams players These variables are arrays and the players details are in player(item)["player"] and the stats
    # are in player(item)["statistics"]
    homePlayers, awayPlayers = lineups["home"]["players"], lineups["home"]["players"]

    # To save in dataabase I reccomend you to use csv.DictWriter.
    # More details in: https://docs.python.org/3/library/csv.html


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
                # We will use a function to process the match
                match_processing(event)

            if has_next_page:
                page += 1
            else:
                last_page = True
