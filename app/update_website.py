import pandas as pd
import pandas.io.formats.style
import datetime
import pytz


def update_website():
    df = pd.read_json(r'data/leaderboard.json').T
    df['avg_time'] = [convert_seconds_to_time(avg_time_in_seconds) for avg_time_in_seconds in df['avg_time']]
    df_sorted = df.sort_values(by='avg_rank')

    html_io_wrapper = open("index.html", "w")

    last_updated_string = "Last updated: " + datetime.datetime.now(pytz.timezone('US/Central')).strftime("%I:%M%p on %B %d, %Y")
    write_to_html_file(df_sorted, html_io_wrapper, title='The Real Crossword Leaderboard', subtitle=last_updated_string)

    return df


def convert_seconds_to_time(duration_in_seconds):
    minutes = duration_in_seconds // 60
    seconds = duration_in_seconds % 60
    return f"{minutes:d}:{seconds:02d}"


def write_to_html_file(df, html_io_wrapper, title='', subtitle=''):
    '''
    Write an entire dataframe to an HTML file with nice formatting.
    '''

    result = '''
<html>
<head>
<style>

    h1 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    h4 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    .wide {
        width: 90%; 
    }

</style>
</head>
<body>
    '''
    result += '<h1> %s </h1>\n' % title
    if type(df) == pd.io.formats.style.Styler:
        result += df.render()
    else:
        result += df.to_html(classes='wide', escape=False)
    result += '<h4> %s </h4>\n' % subtitle
    result += '''
</body>
</html>
'''
    html_io_wrapper.write(result)


if __name__ == "__main__":
    update_website()

