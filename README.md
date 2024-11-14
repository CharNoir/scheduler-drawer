# `pyplot_drawer.py`

`pyplot_drawer.py` is a Python library for visualizing scheduling-related tasks, such as real-time systems scheduling, using matplotlib. The tool creates detailed, customizable Gantt-like charts to depict task execution, task arrivals, deadlines, idling periods, and scheduling periods. Additionally, it allows loading scheduling data from `.xlsx` files and saving visualization data back into `.xlsx` format.

---

## Features
- Generate visual Gantt-like charts for scheduling tasks.
- Support for:
  - Task execution rectangles
  - Task arrivals (arrows)
  - Displayed deadlines (arrows)
  - Idle periods (striped rectangles)
  - Scheduler periodic execution (highlighted areas)
- Load task and scheduling information from `.xlsx` files.
- Save scheduling data into a structured `.xlsx` format with multiple sheets.
- Dynamic creation of directories to ensure proper data storage.

---

## Installation
To use `pyplot_drawer.py`, clone this repository and ensure the following Python libraries are installed:
```bash
pip install matplotlib pandas openpyxl
```

How to Use
# 1. Loading and Visualizing Scheduling Data

Prepare an .xlsx file with the format found in `Schedule Template.xlsx`:

Load the .xlsx file and visualize the schedule
```bash
load("example_schedule")  # Assumes `example_schedule.xlsx` exists in the current directory
```

# 2. Direct Visualization

You can also directly call the draw function:

```bash
from pyplot_drawer import draw

executed_parts = [["Task1", 0, 4], ["Task2", 5, 3]]
tasks_arrivals = [["Task1", 0], ["Task2", 5]]
displayed_deadlines = [["Task1", 8], ["Task2", 10]]
scheduler = [12, 2]  # Period T, Execution Time C
idling = [[9, 3]]  # Idle periods

draw(
    "Example Schedule",
    executed_parts=executed_parts,
    tasks_arrivals=tasks_arrivals,
    displayed_deadlines=displayed_deadlines,
    max_time=20,
    sch_T=scheduler[0],
    sch_C=scheduler[1],
    idling=idling,
    save=True  # Save to an Excel file
)
```