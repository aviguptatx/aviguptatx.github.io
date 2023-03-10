import pandas as pd
import pandas.io.formats.style


def write_df_to_html_file(
    html_io_wrapper,
    df,
    suffix="",
    df_title="",
    df_subtitle="",
    style_sheet_link="",
    title="Untitled Page",
    icon_link="",
):
    """
    Write an entire dataframe to an HTML file with nice formatting.
    """

    result = "<html>"

    if style_sheet_link != "":
        result += f"""
<head>
    <link rel="icon" type="image/x-icon" href="{icon_link}">
    <title>{title}</title>
    <link rel="stylesheet" href="{style_sheet_link}"
</head>
"""

    result += "<body>"

    result += "\n<h1> %s </h1>\n" % df_title
    if type(df) == pd.io.formats.style.Styler:
        result += df.render()
    else:
        result += df.to_html(classes="wide", escape=False)
    result += "\n<h4> %s </h4>" % df_subtitle
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
