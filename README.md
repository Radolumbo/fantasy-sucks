# fantasy-sucks
Stats for fantasy football

## Usage
Currently only one function exists, so:
e.g. `python3 main.py print_records --league_id=480774 --year=2021`

## Bootstrap Your Dev Environment
Copy `.env_template` to `.env` and fill out with two cookies from ESPN: espn_s2 and SWID. You can find these values in Chrome at "Application > Cookies > espn.com" in the Chrome DevTools when on espn.com. You can bring up Chrome DevTools by pressing `F12` on your keyboard. **Copy the entire values for each**. If you don't use Chrome -- figure it out yourself :).

Anyway, once your `.env` file exists and is populated, run:

```bash
source bootstrap.sh
```

This will create a virtual environment for you (you must install python3.9 and python3.9-virtualenv; Google it), source your `.env` file, and source your cookie environment variables (mmm...).
