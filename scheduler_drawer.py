import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import os

def draw(name,  
         executed_parts=None, 
         tasks_arrivals=None, 
         displayed_deadlines=None,
         max_time=None, 
         sch_T=None, 
         sch_C=None, 
         idling=None, 
         save=None):
    # Collect unique task names
    labels = set()
    for task in executed_parts:
        labels.add(task[0])
    labels = sorted(labels)  # Sort labels to ensure consistent ordering
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_ylim(0, len(labels) + 0.5)  # Vertical limit to allow for visual separation of tasks
    ax.set_xlim(0, max_time)  # Timeline limit

    # Hide the default y-axis scale
    ax.yaxis.set_ticks_position('none')  # Remove the ticks on the y-axis

    # Set custom y-axis labels using the actual task names
    ax.set_yticks([i + 0.5 for i in range(len(labels))])  # Shift by 0.5 units
    ax.set_yticklabels(labels)  # Use task names directly

    # Set custom x-axis ticks at every 12 units
    x_ticks = np.arange(0, max_time + 1, sch_T)  # Generate ticks at intervals of 12
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(tick) for tick in x_ticks])  # Label tickss
    
    ax.set_xlabel("Time [ms]")
    task_color = 'blue'
    idle_color = 'black'
    
    # Draw scheduler periods as green rectangles
    time_stamp = 0
    while time_stamp < max_time:
        ax.add_patch(plt.Rectangle((time_stamp, len(labels)), sch_C, 0.5,
                                   color='green', alpha=0.7))
        time_stamp += sch_T

    # Draw task execution rectangles
    if executed_parts:
        for task in executed_parts:
            task_name, start_time, duration = task
            y_position = labels.index(task_name)
            ax.add_patch(plt.Rectangle((start_time, y_position), duration, 1,
                                    color=task_color, alpha=0.7))
            
    # Draw arrows for specified task arrival time
    if tasks_arrivals:
        for task_name, time in tasks_arrivals:
            y_position = labels.index(task_name)
            ax.annotate('', xy=(time, y_position), xytext=(time, y_position + 0.5),
                        arrowprops=dict(arrowstyle="<-", color="red", lw=1.5))
    
     # Draw arrows for specified deadlines    
    if displayed_deadlines:
        for task_name, time in displayed_deadlines:
            y_position = labels.index(task_name)
            ax.annotate('', xy=(time, y_position), xytext=(time, y_position + 0.5),
                        arrowprops=dict(arrowstyle="->", color="violet", lw=1.5))
        
    # Draw idle periods as transparent striped rectangles
    if idling:
        for idle_start, idle_duration in idling:
            ax.add_patch(plt.Rectangle((idle_start, 0), idle_duration, len(labels),
                                       color='black', alpha=0.1, hatch='//'))

    if save:
        save_data(name, executed_parts, tasks_arrivals, displayed_deadlines, [sch_T, sch_C], idling)
    
    plt.legend(loc="upper left")
    plt.title(name)
    plt.show()

def load(tableName):
    file_path = f"{tableName}.xlsx"

    excel_file = pd.ExcelFile(file_path)
    sheet_names = excel_file.sheet_names
    print("Available sheets:", sheet_names)
    
    executed_parts_sheet = pd.read_excel(file_path, sheet_name="Executed Parts")
    executed_parts = executed_parts_sheet.iloc[:, :3].values.tolist()
    
    task_arrivals_sheet = pd.read_excel(file_path, sheet_name="Tasks Arrivals")
    tasks_arrivals = task_arrivals_sheet.iloc[:, :2].values.tolist()
    
    displayed_deadlines_sheet = pd.read_excel(file_path, sheet_name="Displayed Deadlines")
    displayed_deadlines = displayed_deadlines_sheet.iloc[:, :2].values.tolist()
    
    scheduler_sheet = pd.read_excel(file_path, sheet_name="Scheduler")
    sch = scheduler_sheet.iloc[:, :2].values.tolist()[0]
    
    idling_sheet = pd.read_excel(file_path, sheet_name="Idling")
    idling = idling_sheet.iloc[:, :2].values.tolist()[0]

    draw(tableName,
         executed_parts=executed_parts, 
         tasks_arrivals=tasks_arrivals, 
         displayed_deadlines=displayed_deadlines,
         max_time=None, 
         sch_T=sch[0], 
         sch_C=sch[1], 
         idling=idling)
    
def save_data(name, executed_parts, tasks_arrivals, displayed_deadlines, scheduler, idling):
    # Save data to Excel with specified sheet structure
    directory = "solutions"
    file_path = os.path.join(directory, f"{name}.xlsx")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with pd.ExcelWriter(file_path) as writer:
        # Save executed parts
        executed_parts_df = pd.DataFrame(executed_parts, columns=["Task Name", "Start Time", "Duration"])
        executed_parts_df.to_excel(writer, sheet_name="Executed Parts", index=False)
        
        # Save task arrivals
        tasks_arrivals_df = pd.DataFrame(tasks_arrivals, columns=["Task Name", "Arrival Time"])
        tasks_arrivals_df.to_excel(writer, sheet_name="Tasks Arrivals", index=False)
        
        # Save displayed deadlines
        displayed_deadlines_df = pd.DataFrame(displayed_deadlines, columns=["Task Name", "Deadline"])
        displayed_deadlines_df.to_excel(writer, sheet_name="Displayed Deadlines", index=False)
        
        # Save scheduler information
        scheduler_df = pd.DataFrame([scheduler], columns=["Period (T)", "Execution Time (C)"])
        scheduler_df.to_excel(writer, sheet_name="Scheduler", index=False)
        
        # Save idling information
        idling_df = pd.DataFrame(idling, columns=["Idle Start", "Idle Duration"])
        idling_df.to_excel(writer, sheet_name="Idling", index=False)
        
    print(f"Data successfully saved to {file_path}")