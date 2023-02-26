import pandas as pd
import pandas.io.formats.style


def write_df_to_html_file(html_io_wrapper, df, suffix="", title="", subtitle=""):
    """
    Write an entire dataframe to an HTML file with nice formatting.
    """

    result = """
<html>
<head>
<style>
    hr {
        border: none;
        border-top: 3px double #333;
        color: #333;
        overflow: visible;
        text-align: center;
        height: 5px;
    }
    hr:after {
    background: #fff;
    content: '§';
    padding: 0 4px;
    position: relative;
    top: -13px;
    }
    h1 {
        line-height: 1em;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    h2 {
        line-height: .7em;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    h3 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    h4 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    h5 {
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
    """
    result += "<h1> %s </h1>\n" % title
    if type(df) == pd.io.formats.style.Styler:
        result += df.render()
    else:
        result += df.to_html(classes="wide", escape=False)
    result += "<h4> %s </h4>\n" % subtitle
    result += """
</body>
</html>
"""
    html_io_wrapper.write(result + suffix)


def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds


def convert_seconds_to_time(duration_in_seconds):
    minutes = duration_in_seconds // 60
    seconds = duration_in_seconds % 60
    return f"{minutes}:{seconds:02d}"
