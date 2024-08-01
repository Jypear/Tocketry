from pathlib import Path
from tocketry import Tocketry
from tocketry.conds import daily

app = Tocketry()


@app.cond()
def file_exists(file):
    "Custom condition that checks if file exists"
    return Path(file).exists()


@app.task(daily & file_exists("data.csv"))
def do_things():
    "Task that runs once a day when data.csv exists"
    ...


if __name__ == "__main__":
    app.run()
