import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Tasks with start and end dates
tasks = [
    ("Planning Phase", "July 29, 2025", "August 4, 2025"),
    ("Research and Define Scope", "July 29, 2025", "July 31, 2025"),
    ("Create Project Plan", "August 1, 2025", "August 3, 2025"),
    ("Gather Resources", "August 4, 2025", "August 5, 2025"),
    ("Create Work Breakdown Structure (WBS)", "August 6, 2025", "August 6, 2025"),
    ("Design Phase", "August 7, 2025", "August 21, 2025"),
    ("UI/UX Design", "August 7, 2025", "August 11, 2025"),
    ("Wireframe and Prototyping", "August 12, 2025", "August 16, 2025"),
    ("Feedback and Iteration", "August 17, 2025", "August 21, 2025"),
    ("Development Phase", "August 22, 2025", "September 25, 2025"),
    ("Backend Setup", "August 22, 2025", "August 26, 2025"),
    ("Frontend Development", "August 27, 2025", "September 3, 2025"),
    ("Admin Panel Features", "September 4, 2025", "September 10, 2025"),
    ("Integrating Features", "September 11, 2025", "September 14, 2025"),
    ("Testing and Debugging", "September 15, 2025", "September 18, 2025"),
    ("Deployment Phase", "September 26, 2025", "October 2, 2025"),
    ("Prepare Production Environment", "September 26, 2025", "September 28, 2025"),
    ("Deploy to Production", "September 29, 2025", "October 1, 2025"),
    ("Verify Deployment and QA", "October 2, 2025", "October 2, 2025"),
    ("Post-Deployment Phase", "October 3, 2025", "October 6, 2025"),
    ("Collect User Feedback", "October 3, 2025", "October 4, 2025"),
    ("Refinement and Final Adjustments", "October 5, 2025", "October 6, 2025"),
    ("User Acceptance Testing (UAT)", "October 3, 2025", "October 6, 2025")
]

# Convert strings to datetime objects
task_names = [t[0] for t in tasks]
start_dates = [datetime.strptime(t[1], "%B %d, %Y") for t in tasks]
end_dates = [datetime.strptime(t[2], "%B %d, %Y") for t in tasks]

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
for i in range(len(tasks)):
    ax.barh(task_names[i], end_dates[i] - start_dates[i], left=start_dates[i], height=0.8)

# Format x-axis
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=45)

# Labels
ax.set_xlabel('Timeline')
ax.set_ylabel('Tasks')
ax.set_title('Gantt Chart for AI Solutions Platform Project')
plt.tight_layout()
plt.show()
plt.savefig('gantt_chart.jpg', format='jpg')
