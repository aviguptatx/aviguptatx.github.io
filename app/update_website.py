import pandas as pd
import datetime
import pytz


def update_website():
    df = pd.read_json(r'data/leaderboard.json')
    df_sorted = df.T.sort_values(by='avg_rank')
    html = open("index.html", "w")
    html.write(df_sorted.to_html(index=True))
    html.write("Last updated: " + datetime.datetime.now(pytz.timezone('US/Central')).strftime("%I:%M%p on %B %d, %Y"))

    return df


if __name__ == "__main__":
    update_website()

