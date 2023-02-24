import pandas as pd

def update_website():
    df = pd.read_json(r'data/leaderboard.json')
    
    df.to_html('index.html')

    return df


if __name__ == "__main__":
    update_website()

