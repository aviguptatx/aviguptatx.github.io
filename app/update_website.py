import pandas as pd
import datetime
import pytz
import os
from utils import convert_seconds_to_time, write_df_to_html_file


def update_main_leaderboard():
    df = pd.read_json(r"data/leaderboard.json").T

    # make avg_time look nicer and rename columns
    df["avg_time"] = [
        convert_seconds_to_time(int(avg_time_in_seconds))
        for avg_time_in_seconds in df["avg_time"]
    ]

    df.drop(labels=["mu", "sigma"], axis=1, inplace=True)

    # convert avg_ratio to a percentage
    df["avg_ratio"] = pd.Series(
        ["{0:.2f}%".format(val * 100) for val in df["avg_ratio"]], index=df.index
    )

    # rename columns
    df.rename(
        columns={
            "avg_ratio": "Avg. % of Winner's Time",
            "avg_rank": "Avg. Rank",
            "avg_time": "Avg. Time",
            "num_wins": "# Wins",
            "num_games": "# Games Played",
            "elo": "ELO",
        },
        inplace=True,
    )

    # move ELO to the front of the df
    ELO = df["ELO"]
    df.drop(labels=["ELO"], axis=1, inplace=True)
    df.insert(0, "Username", df.index)
    df.insert(1, "ELO", ELO)

    # sort table and add rank column name
    df_sorted = df.sort_values(by="ELO", ascending=False).reset_index(drop=True)
    df_sorted.columns.name = "Rank"
    df_sorted.index = df_sorted.index + 1

    # write HTML to index.html to display df
    html_io_wrapper = open("index.html", "w")
    last_updated_string = "Last updated: " + datetime.datetime.now(
        pytz.timezone("US/Central")
    ).strftime("%I:%M%p on %B %d, %Y")
    write_df_to_html_file(
        html_io_wrapper,
        df_sorted,
        title="The Real Crossword Leaderboard",
        subtitle=last_updated_string,
    )

    # Create history links
    directory = "history"
    html_files = [f for f in os.listdir(directory) if f.endswith(".html")]
    html_files.sort(reverse=True)
    # Generate HTML code for the links to each page
    links_html = "<h3>"
    for file in html_files:
        # Get the name of the file without the extension
        name = os.path.splitext(file)[0]
        # Generate the link HTML
        link_html = f'<a href="{directory}/{file}">{name}</a><br>\n'
        # Append the link HTML to the overall HTML for the page
        links_html += link_html
    links_html += "</h3>"

    html_io_wrapper.write("<h1> Daily History </h1>")
    html_io_wrapper.write(links_html)


if __name__ == "__main__":
    update_main_leaderboard()
