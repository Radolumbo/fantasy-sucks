# fantasy-sucks
Stats for fantasy football using https://github.com/cwendt94/espn-api, but I don't like that module and want to replace it with raw API calls eventually.

## Usage
`python3 main.py print_records --league_id=480774 --year=2021`
`python3 main.py print_all_alternate_records_for_person --league_id=480774 --year=2021 --person_name="Nick Palumbo"`

## Bootstrap Your Dev Environment
Copy `.env_template` to `.env` and fill out with two cookies from ESPN: espn_s2 and SWID. You can find these values in Chrome at "Application > Cookies > espn.com" in the Chrome DevTools when on espn.com. You can bring up Chrome DevTools by pressing `F12` on your keyboard. **Copy the entire values for each**. If you don't use Chrome -- figure it out yourself :).

Anyway, once your `.env` file exists and is populated, run:

```bash
source bootstrap.sh
```

This will create a virtual environment for you (you must install python3.9 and python3.9-virtualenv; Google it), source your `.env` file, and source your cookie environment variables (mmm...).

## Notes for Nick
You should probably just name it Team instead of Person, dumbass. A later problem...
