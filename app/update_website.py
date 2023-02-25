import pandas as pd
import datetime

def update_website():
    df = pd.read_json(r'data/leaderboard.json')
    
    df.to_html('index.html')

    html = open("index.html", "a")
    html.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    return df


if __name__ == "__main__":
    update_website()

