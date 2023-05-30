import api


def match_processing(event):
    event_id = event["id"]

    # Match stats
    try:
        statistics = api.get_match_statistics(event_id)
    except Exception as ex:
        # If no stats just return, skipping the match
        print(f"HTTP error with the stats: {ex}")
        return

    # We're just printing the stats, but you can do anything with the event and statistics like saving
    # to your database
    print(statistics)
    # Getting all other info
    try:
        lineups = api.get_match_lineups(event_id)
    except Exception as ex:
        # If no lineups just return, skipping the match
        print(f"HTTP error with the lineups: {ex}")
        return
    form = None
    try:
        form = api.get_pre_match_form(event_id)
    except Exception as ex:
        # If no form you decide what action to do. It can happen in playoff matches
        print(f"HTTP error with the form: {ex}")
    try:
        match = api.get_match(event_id)
    except Exception as ex:
        # Who knows what can happen to the match, if any error skip
        print(f"HTTP error with the match: {ex}")
        return

    # Let's get all needed variables from match details

    # Event start timestamp (in seconds)
    startTimestamp = match["event"]["startTimestamp"]

    # Team names
    homeTeamName, awayTeamName = match["event"]["homeTeam"]["name"], match["event"]["awayTeam"]["name"]

    # Home team scores
    homeTeamFinalScore, homeTeamP1Score, homeTeamP2Score, homeTeamP3Score, homeTeamP4Score = \
    match["event"]["homeScore"][
        "current"], match["event"]["homeScore"]["period1"], match["event"]["homeScore"]["period2"], \
    match["event"]["homeScore"]["period3"], \
        match["event"]["homeScore"]["period4"]

    try:
        homeTeamOvertimeScore = match["event"]["homeScore"]["overtime"]
    except:
        #     No overtime logic
        pass

    # Away team scores
    awayTeamFinalScore, awayTeamP1Score, awayTeamP2Score, awayTeamP3Score, awayTeamP4Score = \
    match["event"]["awayScore"][
        "current"], match["event"]["awayScore"]["period1"], match["event"]["awayScore"]["period2"], \
    match["event"]["awayScore"]["period3"], \
        match["event"]["awayScore"]["period4"]

    try:
        awayTeamOvertimeScore = match["event"]["awayScore"]["overtime"]
    except:
        #     No overtime logic
        pass

    # Team standings
    if form is not None:
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
