import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import json
import trueskill
from trueskill import Rating, rate
from utils import write_df_to_html_file, convert_seconds_to_time


def update_database_and_history():
    # pass in cookies and headers for request -- yes this isn't super secure but it's good enough
    cookies = {
        "nyt-a": "1Cnj_QdNOQ4lY6fMFyViCV",
        "purr-cache": "<K0<r<C_<G_<S0",
        "_cb": "IIFFzwZ0toCZYDiI",
        "FPC": "id=e61f8960-19b4-4b3d-82df-c78b0d412418",
        "datadome": "Zp8UR9~.Rp_YYvZfwnlqfGiodxYDYG~FYVQ2b3Cl8QKy44HO8_4ImRAP99PnVv9nP-WbdCgC2.0EXEbN6.XZ3g7bvgYqxnMzh.J~TaO1MhajkfW~pK52QbEBC81a.w6",
        "nyt-purr": "cfhhcfhhhckfhd",
        "edu_opt": "%7B%22orgName%22%3A%22Our%20Lady%20of%20the%20Lake%20University%22%2C%22nickName%22%3A%22%22%7D",
        "edu_cig_opt": "%7B%22isEduUser%22%3Atrue%7D",
        "_gcl_au": "1.1.765225773.1676619033",
        "walley": "GA1.2.615765266.1676619033",
        "WTPERSIST": "regi_id=199236716",
        "nyt-auth-method": "username",
        "nyt-xwd-hashd": "false",
        "nyt-gdpr": "0",
        "b2b_cig_opt": "%7B%22isCorpUser%22%3Afalse%7D",
        "walley_gid": "GA1.2.1794611066.1677184267",
        "nyt-geo": "US",
        "_cb_svref": "null",
        "iter_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwidXNlcl9pZCI6IjYyMDljMmI1MjQwMjVlMDAwMWRmNTQ1MSIsInVzZXJfaWRfZXh0Ijp0cnVlLCJpYXQiOjE2NzcxODcxMDJ9.8RQJ7hwD5ddiNC-TNIuvyCjnddPs8Mn1EKxfDgLLaYg",
        "RT": '"z=1&dm=nytimes.com&si=06405f15-2353-464a-a811-7c4299c9df4e&ss=lehluo2o&sl=3&tt=2k3&bcn=%2F%2F17de4c1f.akstat.io%2F&ld=2si8&ul=31j9&hd=31n3"',
        "nyt-b3-traceid": "9b227355fdba48b6a0387d1f82a80987",
        "nyt-m": "D5800984CB7EFD370CFBE8E0715F0988&imv=i.0&s=s.core&cav=i.0&ica=i.0&iru=i.1&v=i.0&g=i.0&er=i.1677187590&vp=i.0&ft=i.0&iub=i.0&e=i.1677679200&uuid=s.b39033c3-a2d0-48a5-9029-2d2707f1ddc4&igd=i.0&ird=i.0&igu=i.1&ira=i.0&iir=i.0&t=i.1&vr=l.4.0.0.0.0&iue=i.0&iga=i.0&fv=i.0&imu=i.1&prt=i.0&n=i.2&rc=i.0&ifv=i.0&igf=i.0&pr=l.4.0.0.0.0&ier=i.0",
        "SIDNY": "CBMSJQjZr9-fBhDcu9-fBhoSMS2yMmUhvcDzQmomE_ygSnChIOy4gF8aQAGNMMdn4e9n7hhDyPejVZRGNeAsrrwnSCIQqQtbbobdNV4W1pMJ69ngaLz5DpZ8pBZCppkqahJOIYkTxj4YXgU=",
        "NYT-S": "1oCnm3sCqUNbP5lOCI/J1KOCqmuMa00/E3R7yakO2Cztu/8xTHRbN27DuMfNjiIU6ljOoea6bgYnRxNtEefmkOCf7JqWSAapro785byieP2DsUpZZcwOatwg00^^^^CBMSJQjZr9-fBhDcu9-fBhoSMS2yMmUhvcDzQmomE_ygSnChIOy4gF8aQAGNMMdn4e9n7hhDyPejVZRGNeAsrrwnSCIQqQtbbobdNV4W1pMJ69ngaLz5DpZ8pBZCppkqahJOIYkTxj4YXgU=",
        "datadome": "1DHKKtKpSLGalxo2euKfNWjBhcsvb2HPZEE_Og9zkdZJgDFnEI880AKXE4W5f_kuFxXebPhFE0wCLVA1PlnQkzOVflZ1rfqNM4I2-z80eC56v-j6JSKbdocbWpf3qisi",
        "nyt-jkidd": "uid=199236716&lastRequest=1677188452477&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C1%5D&adv=2&a7dv=2&a14dv=2&a21dv=2&lastKnownType=regi&newsStartDate=&entitlements=",
        "_gat_UA-58630905-2": "1",
        "_chartbeat2": ".1618989681491.1677188453175.0000000001000001.BL52BqDU4i9iB9Jt0NCDMOSTDnHvsk.8",
    }

    headers = {
        "authority": "www.nytimes.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        # 'cookie': 'nyt-a=1Cnj_QdNOQ4lY6fMFyViCV; purr-cache=<K0<r<C_<G_<S0; _cb=IIFFzwZ0toCZYDiI; FPC=id=e61f8960-19b4-4b3d-82df-c78b0d412418; datadome=Zp8UR9~.Rp_YYvZfwnlqfGiodxYDYG~FYVQ2b3Cl8QKy44HO8_4ImRAP99PnVv9nP-WbdCgC2.0EXEbN6.XZ3g7bvgYqxnMzh.J~TaO1MhajkfW~pK52QbEBC81a.w6; nyt-purr=cfhhcfhhhckfhd; edu_opt=%7B%22orgName%22%3A%22Our%20Lady%20of%20the%20Lake%20University%22%2C%22nickName%22%3A%22%22%7D; edu_cig_opt=%7B%22isEduUser%22%3Atrue%7D; _gcl_au=1.1.765225773.1676619033; walley=GA1.2.615765266.1676619033; WTPERSIST=regi_id=199236716; nyt-auth-method=username; nyt-xwd-hashd=false; nyt-gdpr=0; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; walley_gid=GA1.2.1794611066.1677184267; nyt-geo=US; _cb_svref=null; iter_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwidXNlcl9pZCI6IjYyMDljMmI1MjQwMjVlMDAwMWRmNTQ1MSIsInVzZXJfaWRfZXh0Ijp0cnVlLCJpYXQiOjE2NzcxODcxMDJ9.8RQJ7hwD5ddiNC-TNIuvyCjnddPs8Mn1EKxfDgLLaYg; RT="z=1&dm=nytimes.com&si=06405f15-2353-464a-a811-7c4299c9df4e&ss=lehluo2o&sl=3&tt=2k3&bcn=%2F%2F17de4c1f.akstat.io%2F&ld=2si8&ul=31j9&hd=31n3"; nyt-b3-traceid=9b227355fdba48b6a0387d1f82a80987; nyt-m=D5800984CB7EFD370CFBE8E0715F0988&imv=i.0&s=s.core&cav=i.0&ica=i.0&iru=i.1&v=i.0&g=i.0&er=i.1677187590&vp=i.0&ft=i.0&iub=i.0&e=i.1677679200&uuid=s.b39033c3-a2d0-48a5-9029-2d2707f1ddc4&igd=i.0&ird=i.0&igu=i.1&ira=i.0&iir=i.0&t=i.1&vr=l.4.0.0.0.0&iue=i.0&iga=i.0&fv=i.0&imu=i.1&prt=i.0&n=i.2&rc=i.0&ifv=i.0&igf=i.0&pr=l.4.0.0.0.0&ier=i.0; SIDNY=CBMSJQjZr9-fBhDcu9-fBhoSMS2yMmUhvcDzQmomE_ygSnChIOy4gF8aQAGNMMdn4e9n7hhDyPejVZRGNeAsrrwnSCIQqQtbbobdNV4W1pMJ69ngaLz5DpZ8pBZCppkqahJOIYkTxj4YXgU=; NYT-S=1oCnm3sCqUNbP5lOCI/J1KOCqmuMa00/E3R7yakO2Cztu/8xTHRbN27DuMfNjiIU6ljOoea6bgYnRxNtEefmkOCf7JqWSAapro785byieP2DsUpZZcwOatwg00^^^^CBMSJQjZr9-fBhDcu9-fBhoSMS2yMmUhvcDzQmomE_ygSnChIOy4gF8aQAGNMMdn4e9n7hhDyPejVZRGNeAsrrwnSCIQqQtbbobdNV4W1pMJ69ngaLz5DpZ8pBZCppkqahJOIYkTxj4YXgU=; datadome=1DHKKtKpSLGalxo2euKfNWjBhcsvb2HPZEE_Og9zkdZJgDFnEI880AKXE4W5f_kuFxXebPhFE0wCLVA1PlnQkzOVflZ1rfqNM4I2-z80eC56v-j6JSKbdocbWpf3qisi; nyt-jkidd=uid=199236716&lastRequest=1677188452477&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C0%2C0%2C0%2C1%5D&adv=2&a7dv=2&a14dv=2&a21dv=2&lastKnownType=regi&newsStartDate=&entitlements=; _gat_UA-58630905-2=1; _chartbeat2=.1618989681491.1677188453175.0000000001000001.BL52BqDU4i9iB9Jt0NCDMOSTDnHvsk.8',
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    # load previous data, if it exists
    f = open("data/leaderboard.json")
    prev_data = {}
    try:
        prev_data = json.load(f)
    except:
        pass

    # fetch current daily leaderboard
    r = requests.get(
        "https://www.nytimes.com/puzzles/leaderboards", cookies=cookies, headers=headers
    )
    soup = BeautifulSoup(r.text, "html.parser")
    leaderboard_scores = soup.find("div", {"class": "lbd-board__items"}).find_all(
        "div", {"class": "lbd-score"}
    )

    # get current year (for the history page)
    date = (
        soup.find("div", {"class": "lbd-board__header lbd-type__centered"})
        .find("h3", {"class": "lbd-type__date"})
        .text.strip()
    )
    year = date[-4:]

    # new leaderboard dict
    leaderboard = {}

    # daily leaderboard for match history
    today_ranks = []
    today_names = []
    today_times = []

    # trueskill stuff
    trueskills = []
    ranks = []
    prev_mus = []
    prev_sigmas = []
    post_mus = []
    post_sigmas = []
    usernames = []

    # used in the case of equivalent times -- makes sure NYT ordering doesn't matter
    prev_time = -1
    winning_time = 0

    # iterate through all daily leaderboard entries and update database
    for rank, item in enumerate(leaderboard_scores, 1):
        # skip this player if they have no time
        if item.find("p", {"class": "lbd-score__time"}).text.strip() == "--":
            continue

        # fetch player username
        username = item.find("p", {"class": "lbd-score__name"}).text.strip()
        if (
            username == "avi (you)"
        ):  # needed because we are pulling data from my own leaderboard -- can consider using a separate indexer account
            username = "avi"
        usernames.append(username)

        # fetch player time
        time_in_seconds = convert_time_to_seconds(
            item.find("p", {"class": "lbd-score__time"}).text.strip()
        )

        if rank == 1:
            winning_time = time_in_seconds

        # account for ties
        if time_in_seconds == prev_time:
            rank = rank - 1

        # update daily stats
        today_ranks.append(rank)
        today_names.append(username)
        today_times.append(convert_seconds_to_time(time_in_seconds))

        winning_time_ratio = time_in_seconds / winning_time

        if not username in prev_data:  # our current contestant is not in the database
            avg_rank = rank
            avg_time = time_in_seconds
            avg_ratio = winning_time_ratio
            num_wins = 1 if rank == 1 else 0
            num_games = 1
            prev_mu = trueskill.MU
            prev_sigma = trueskill.SIGMA
        else:  # current contestant is in the database
            player_data = prev_data[username]
            prev_num_games = player_data["num_games"]

            avg_rank = (player_data["avg_rank"] * prev_num_games + rank) / (
                prev_num_games + 1
            )
            avg_time = (player_data["avg_time"] * prev_num_games + time_in_seconds) / (
                prev_num_games + 1
            )
            avg_ratio = (
                player_data["avg_ratio"] * prev_num_games + winning_time_ratio
            ) / (prev_num_games + 1)
            num_games = prev_num_games + 1
            num_wins = player_data["num_wins"] + (1 if rank == 1 else 0)
            prev_mu = player_data["mu"]
            prev_sigma = player_data["sigma"]

        # update leaderboard stats
        leaderboard[username] = {
            "avg_ratio": avg_ratio,
            "avg_rank": avg_rank,
            "avg_time": avg_time,
            "num_wins": num_wins,
            "num_games": num_games,
        }

        prev_mus.append(prev_mu)
        prev_sigmas.append(prev_sigma)

        # trueskill ranks are 0-indexed
        ranks.append(rank - 1)
        trueskills.append(Rating(mu=prev_mu, sigma=prev_sigma))

        prev_time = time_in_seconds

    # update ratings
    trueskills_tuples = [(x,) for x in trueskills]
    try:
        # get results from trueskill method
        results = rate(trueskills_tuples, ranks=ranks)
        #  store new mu and sigma for each player
        for result in results:
            post_mus.append(round(result[0].mu, 2))
            post_sigmas.append(round(result[0].sigma, 2))
    except:  # if something goes wrong, just use previous ratings
        post_mus = prev_mus
        post_sigmas = prev_sigmas

    for i, username in enumerate(usernames):
        mu = post_mus[i]
        sigma = post_sigmas[i]
        leaderboard[username]["mu"] = mu
        leaderboard[username]["sigma"] = sigma
        leaderboard[username]["elo"] = (mu - 3 * sigma) * 60

    # write today's performances to the history file
    today_df = pd.DataFrame(
        {"Rank": today_ranks, "Time": today_times}, index=today_names
    )
    today_df.columns.name = "Username"
    update_history(today_df, year, date)

    # add back old data for contestants that didn't participate in this puzzle
    for username in prev_data:
        if not username in leaderboard:
            leaderboard[username] = prev_data[username]

    # write data to database
    with open("data/leaderboard.json", "w") as f:
        json.dump(leaderboard, f)


def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds


def update_history(today_df, year: str, date: str):
    # pull existing history html, if any (we will prepend to this)
    try:
        with open(f"history/{year}.html", "r") as f:
            existing_html = f.read()
    except:
        existing_html = ""

    # write today's results to the history file
    html_io_wrapper = open(f"history/{year}.html", "w")
    write_df_to_html_file(html_io_wrapper, today_df, suffix=existing_html, title=date)


if __name__ == "__main__":
    update_database_and_history()
