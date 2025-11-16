# pypdf
from pypdf import PdfReader
from PyPDF2 import PdfReader
import PyPDF2
import numpy as np
import pandas as pd
import re
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# flag students for intervention

def set_priorities_per_student(df, idx):
    
    # Priority based on Performance
    # set priotity 0 
    if df.loc[idx, 'Hours On Program'] < 1:
        df.loc[idx, 'Priority Perf'] = 0
    # set priority 1
    elif df.loc[idx, 'Overall Percentage Score'] < 60:
        df.loc[idx, 'Priority Perf'] = 1
    # set priority 2
    elif df.loc[idx, 'Overall Percentage Score'] < 75 and df.loc[idx, 'Overall Percentage Score'] >= 60:
        df.loc[idx, 'Priority Perf'] = 2
        
    elif df.loc[idx, 'Overall Percentage Score'] >= 75:
        df.loc[idx, 'Priority Perf'] = 3
    else:
        df.loc[idx, 'Priority Perf'] = 3
    
    # Priority based on Number of Lessons Completed
    # max value of Lesson Completed
    max_N_lesson = df['Lesson Completed'].max()
    median_N_lesson = df['Lesson Completed'].median()
    #calculate interquartile range 
    q3, q1 = np.percentile(df['Lesson Completed'], [75 ,25])
    
    # set priotity 0 
    if df.loc[idx, 'Lesson Completed'] == 0:
        df.loc[idx, 'Priority N_Lesson'] = 0
    # set priority 1
    elif df.loc[idx, 'Lesson Completed'] < q1:
        df.loc[idx, 'Priority N_Lesson'] = 1
    # set priority 2
    elif df.loc[idx, 'Lesson Completed'] < q3 and df.loc[idx, 'Lesson Completed'] >= q1:
        df.loc[idx, 'Priority N_Lesson'] = 2
        
    elif df.loc[idx, 'Lesson Completed'] >= q3:
        df.loc[idx, 'Priority N_Lesson'] = 3
    else:
        df.loc[idx, 'Priority N_Lesson'] = 3
    return df

def flag_students(df):

    # change type of all columns to float
    for col in ['Lesson Completed', 'Hours On Program', 'English Test Taken', 'English Test with Excellent/Good', 'Overall Percentage Score']:
        df[col] = df[col].astype(float)

    df['Priority Perf'] = None
    
    for i in range(len(df)):
        df = set_priorities_per_student(df, i)

     #print(f"Length of dataframe: {len(df)}")
    
    return df


def flag_students_per_perf(df):

    # change type of all columns to float
    for col in ['Lesson Completed', 'Hours On Program', 'English Test Taken', 'English Test with Excellent/Good', 'Overall Percentage Score']:
        df[col] = df[col].astype(float)

    df['Priority Perf'] = None
    
    for idx in range(len(df)):
        #df = set_priorities_per_student(df, i)
        # Priority based on Performance
        # set priotity 0 
        #if df.loc[idx, 'Hours On Program'] < 1:
        if df.loc[idx, 'Lesson Completed'] == 0:
            df.loc[idx, 'Priority Perf'] = 0
        # set priority 1
        elif df.loc[idx, 'Overall Percentage Score'] < 50:
            df.loc[idx, 'Priority Perf'] = 1
        # set priority 2
        elif df.loc[idx, 'Overall Percentage Score'] < 75 and df.loc[idx, 'Overall Percentage Score'] >= 50:
            df.loc[idx, 'Priority Perf'] = 2
            
        elif df.loc[idx, 'Overall Percentage Score'] >= 75:
            df.loc[idx, 'Priority Perf'] = 3
        else:
            df.loc[idx, 'Priority Perf'] = 3   

    #print(f"Length of dataframe: {len(df)}")
    
    return df


# plot barplots
def plot_barplots(df):
    colors = ['purple', 'red', 'orange', 'green']
    fig, axs = plt.subplots(1, 4, figsize=(15, 4))
    for i, col in enumerate(['Lesson Completed', 'Hours On Program', 'English Test Taken', 'Overall Percentage Score']):
        sns.barplot(data=df, y=col, hue='Priority Perf', ax=axs[i], capsize=0.25, palette=colors)
        axs[i].set_title(f'{col}', fontsize = 16)
        axs[i].legend()
    
    plt.suptitle('Priority based on Performance', fontsize = 20)
    plt.tight_layout()
    plt.show()

    colors = ['purple', 'red', 'orange', 'green']
    #fig, axs = plt.subplots(1, 4, figsize=(15, 4))
    #for i, col in enumerate(['Lesson Completed', 'Hours On Program', 'English Test Taken', 'Overall Percentage Score']):
    #    sns.barplot(data=df, y=col, hue='Priority N_Lesson', ax=axs[i], capsize=0.25, palette=colors)
    #    axs[i].set_title(f'{col}', fontsize = 16)
    #    #axs[i].legend()
    #plt.suptitle('Priority based on Number of Lessons Completed', fontsize = 20)
    #plt.tight_layout()
    #plt.show()
    
def plot_piecharts(df, stream):
    # Count the occurrences of each category
    category_counts_perf = df['Priority Perf'].value_counts()
    #category_counts_lesson = df['Priority N_Lesson'].value_counts()

    # set color code: 0: purple, 1: red, 2: orange, 3: green
    colors = ['purple', 'red', 'orange', 'green']

    fig = plt.figure(figsize=(5, 5))
    #fig, axs = plt.subplots(1, 2, figsize = (12,5))
    # Plotting the pie chart
    plt.pie(category_counts_perf, labels=category_counts_perf.index, autopct='%1.1f%%', startangle=140, colors=[colors[idx] for idx in category_counts_perf.index])
    plt.title(f'{stream}\n{len(df)} Students', fontsize=11)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # set legend as bounding box on right
    plt.legend(title='Priority', loc='center right', bbox_to_anchor=(1, 0, 0.5, 1))

    #axs[1].pie(category_counts_lesson, labels=category_counts_lesson.index, autopct='%1.1f%%', startangle=140, colors=[colors[idx] for idx in category_counts_lesson.index])
    #axs[1].set_title(f'Priority of intervention Lesson Completed \n {len(df)} Students', fontsize=15)
    #axs[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #axs[1].legend()
    #plt.text(0.5, 0.05, 'Priority 0: No activity\n Priority 1: Very low performance\n Priority 2: Low performance\n Priority 3: Great', ha='center', va='center', fontsize=15, color='black')
    #plt.savefig('pie_chart.pdf')
    #plt.suptitle(suptitle, fontsize = 18)
    plt.tight_layout()
    plt.show()

def plot_piecharts_all(df_all):
    # plot pie chart for each strean in a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for idx, stream in enumerate(["3A", "3B", "4A", "4B"]):
        df = df_all[df_all['Class'] == stream]
        # Count the occurrences of each category
        category_counts_perf = df['Priority Perf'].value_counts()
        # set color code: 0: purple, 1: red, 2: orange, 3: green
        colors = ['purple', 'red', 'orange', 'green']
        # Plotting the pie chart with custom radius
        axs[idx//2, idx%2].pie(category_counts_perf, 
                                labels=category_counts_perf.index, 
                                autopct='%1.1f%%', 
                                startangle=140, 
                                colors=[colors[idx] for idx in category_counts_perf.index])
        axs[idx//2, idx%2].set_title(f'{stream}\n{len(df)} Students', fontsize=11)
        axs[idx//2, idx%2].axis('equal')
        # set legend as bounding box on right
        axs[idx//2, idx%2].legend(title='Priority', loc='center right', bbox_to_anchor=(1, 0, 0.5, 1))
    
    #plt.legend(title='Priority', loc='center right', bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    plt.show()

def plot_piecharts_all_new(df_all, pie_radius=1):
    # Plot pie chart for each stream in a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    colors = ['purple', 'red', 'orange', 'green']  # Define colors outside loop

    for idx, stream in enumerate(["3A", "3B", "4A", "4B"]):
        df = df_all[df_all['Class'] == stream]
        category_counts_perf = df['Priority Perf'].value_counts()

        # Plotting the pie chart with custom radius
        wedges, texts, autotexts = axs[idx // 2, idx % 2].pie(
            category_counts_perf,
            labels=category_counts_perf.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=[colors[int(i)] for i in category_counts_perf.index],  # Ensure index is int
            radius=pie_radius
        )

        axs[idx // 2, idx % 2].set_title(f'{stream}\n{len(df)} Students', fontsize=11)
        axs[idx // 2, idx % 2].axis('equal')

    # Define color patches explicitly
    color_map = {'Purple': 'purple', 'Red': 'red', 'Orange': 'orange', 'Green': 'green'}
    handles = [mpatches.Patch(color=color_map[label], label=f'{i}: {label}')
            for i, label in enumerate(color_map.keys())]

    # Set the legend with a fixed order
    fig.legend(
        handles=handles,
        labels=[f'{i}' for i, label in enumerate(color_map.keys())],
        title='Priority',
        loc='center right',
        bbox_to_anchor=(1.05, 0.5)
    )

    plt.tight_layout(rect=[0, 0, 0.9, 1])  # Adjust layout to make space for legend
    plt.show()


# plot time series
def plot_time_series_N_Lesson(df_ts_N_Lesson, height, save_fig = False, path = None):
    
    fig = plt.figure(figsize=(20, height))

    # Define custom colors
    colors = ['purple', 'red', 'orange', 'green']
    custom_cmap = ListedColormap(colors)

    sns.heatmap(df_ts_N_Lesson, annot=False, cmap=custom_cmap, cbar=True, linewidths=0.05, linecolor='black')

    plt.xlabel('Students')
    #plt.ylabel('Time')
    plt.yticks(rotation=360)

    plt.title('Number of Lessons in Time')
    plt.show()

    if save_fig:
        fig.savefig(path, format="png")
    
def plot_time_series_perf(df_ts_perf, height, save_fig = False, path = None):
    
    fig = plt.figure(figsize=(20, height))

    # Define custom colors
    colors = ['purple', 'red', 'orange', 'green']
    custom_cmap = ListedColormap(colors)

    sns.heatmap(df_ts_perf, annot=False, cmap=custom_cmap, cbar=True, linewidths=0.05, linecolor='black')

    plt.xlabel('Students')
    #plt.ylabel('Time')
    plt.yticks(rotation=360)

    plt.title('Performance in Time')
    plt.show()

    if save_fig:
        fig.savefig(path, format="png")

def check_sync(english_eshuleni):
    english_eshuleni['Sync date cat'] = english_eshuleni['Sync date'].apply(lambda x: 'min ago' if 'min ago' in x else ('hour(s) ago' if 'hour(s) ago' in x else 'other'))

    fig, axs = plt.subplots(1, 4, figsize=(15, 5))

    axs[0].pie(english_eshuleni['Sync date cat'].value_counts(), labels = english_eshuleni['Sync date cat'].value_counts().index, autopct='%1.1f%%')
    axs[0].set_title('Sync date categories')

    sns.countplot(data = english_eshuleni[english_eshuleni['Sync date cat'] == 'min ago'], x = "Sync date", ax = axs[1])
    axs[1].set_title('Data synced min ago')
    sns.countplot(data = english_eshuleni[english_eshuleni['Sync date cat'] == 'hour(s) ago'], x = "Sync date", ax = axs[2])
    axs[2].set_title('Data synced hour(s) ago')
    sns.countplot(data = english_eshuleni[english_eshuleni['Sync date cat'] == 'other'], x = "Sync date", ax = axs[3])
    axs[3].set_title('Data synced other')

    for i in range(1, 4):
        axs[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def create_intervention_table(df_analytics):
    df_intervention = pd.DataFrame(columns = ['Student', 'Class', 'Priority N_Lesson', 'Priority Perf',  'Addressed', 'Issue', 'Action proposed', 'Action Taken', 'Unit failed'])

    for i in range(len(df_analytics)):
        df_intervention.loc[i, 'Student'] = df_analytics.loc[i, 'Name']
        df_intervention.loc[i, 'Class'] = df_analytics.loc[i, 'Class']
        df_intervention.loc[i, 'Priority N_Lesson'] = df_analytics.loc[i, 'Priority N_Lesson']
        df_intervention.loc[i, 'Priority Perf'] = df_analytics.loc[i, 'Priority Perf']
    # sort by "Issue"
    #df_intervention.sort_values(by='Priority N_Lesson', ascending=True, inplace=True)

    # order of priority
    # 0 > N_Lesson 1 > Perf 2 > Perf 1
    intervention_table = df_intervention[(df_intervention['Priority N_Lesson'] == 0) & (df_intervention['Priority Perf'] == 0)]
    intervention_table = pd.concat([intervention_table, df_intervention[(df_intervention['Priority N_Lesson'] == 1)].sort_values(by='Priority Perf', ascending=True)])
    intervention_table = pd.concat([intervention_table, df_intervention[(df_intervention['Priority Perf'] == 2)].sort_values(by='Priority N_Lesson', ascending=True)])
    intervention_table = pd.concat([intervention_table, df_intervention[(df_intervention['Priority Perf'] == 1)].sort_values(by='Priority N_Lesson', ascending=True)])

    duplicates = intervention_table[intervention_table.duplicated(subset=['Student'], keep='first')]
    if len(duplicates) > 0:
        print(f"Warning: {len(duplicates)} students have multiple entries in the intervention table")
        #print(duplicates)
    # remove the duplicates
    intervention_table = intervention_table[~intervention_table.duplicated(subset=['Student'], keep='first')]

    # group by "Class"
    intervention_table = intervention_table.groupby('Class').apply(lambda x: x.reset_index(drop=True)).drop('Class', axis=1)

    return intervention_table, duplicates

def create_new_intervention_table(df_all):
    df_intervention = pd.DataFrame(columns = ['Student', 'Class', 'Priority Perf', 'Nb Lessons',  'Addressed', 'Issue', 'Action proposed', 'Action Taken', 'Unit failed'])

    for i in range(len(df_all)):
        df_intervention.loc[i, 'Student'] = df_all.loc[i, 'Name']
        df_intervention.loc[i, 'Class'] = df_all.loc[i, 'Class']
        df_intervention.loc[i, 'Priority Perf'] = df_all.loc[i, 'Priority Perf']
        df_intervention.loc[i, 'Nb Lessons'] = df_all.loc[i, 'Lesson Completed']

    # sort by "Issue"
    #df_intervention.sort_values(by='Priority N_Lesson', ascending=True, inplace=True)

    # order of priority
    # 0 > Perf 1 > Perf 2 > Perf 3, then decreasing number of Lessons
    intervention_table = pd.DataFrame()
    # order per stream 
    for idx, stream in enumerate(["3A", "3B", "4A", "4B"]):
        df_intervention_stream = df_intervention[df_intervention['Class'] == stream]
        for group in [0, 1, 2, 3]:
            if group in df_intervention_stream['Priority Perf'].unique():
                tmp = df_intervention_stream[df_intervention_stream['Priority Perf'] == group].sort_values(by='Nb Lessons', ascending = False) 
                intervention_table = pd.concat([intervention_table, tmp]).reset_index(drop=True)
            else:
                continue

    # group by "Class"
    #intervention_table = intervention_table.groupby('Class').apply(lambda x: x.reset_index(drop=True)).drop('Class', axis=1)

    return intervention_table

def plot_piecharts_all_new_plotly(df_all, 
                                  layout="2x2", 
                                  hole=0,
                                  output_file=None):
    # Define streams and colors
    streams = ["3A", "3B", "4A", "4B"]
    colors = ['purple', 'red', 'orange', 'green', 'blue']
    
    # Determine layout configuration
    if layout == "2x2":
        rows, cols = 2, 2
    elif layout == "1x4":
        rows, cols = 1, 4
    else:
        raise ValueError("Invalid layout option. Choose either '2x2' or '1x4'.")
    
    # Create subplot figure
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"{stream}" for stream in streams],
                        specs=[[{"type": "domain"}]*cols for _ in range(rows)],
                        horizontal_spacing=0.1)

    for idx, stream in enumerate(streams):
        df = df_all[df_all['Class'] == stream]
        category_counts_perf = df['Priority Perf'].value_counts()
        
        labels = category_counts_perf.index
        # rename label 4 to Absent
        labels = ['Absent' if label == 4 else label for label in labels]
        values = category_counts_perf
        
        row, col = divmod(idx, cols)  # Determine subplot position
        fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                hole=hole,  # Adjust pie size based on radius
                marker=dict(colors=[colors[int(i)] for i in category_counts_perf.index]),
                textinfo='label+percent'
            ),
            row=row+1, col=col+1
        )

    # Update layout
    fig.update_layout(
        title_text="Student Performance Priority",
        height=500 if layout == "2x2" else 300,  # Adjust height based on layout
        showlegend=True
    )
    # add "N = {len(df)}" to each subplot title
    for idx, stream in enumerate(streams):
        fig.layout.annotations[idx].update(text=f"{stream}<br>N = {len(df_all[df_all['Class'] == stream])}")
        fig.layout.annotations[idx].font.size = 13
        fig.layout.annotations[idx].font.color = "grey"


    # Save as HTML
    if output_file:
        fig.write_html(output_file)
        print(f"Plot saved as {output_file}")
    return fig

# remove kids that left the program

def remove_OOP_students(df_all):

    # import the file with out of program students
    left_students = pd.read_excel('./../Pilot 2025/Data Enuma LMS/students_out_of_program_2025.xlsx')
    print(f"Number of students that left the program: {len(left_students)}")

    # check the priority perf of left students, should be 0
    left_students_flagged = flag_students(df_all[df_all['Name'].isin(left_students['Name'])].reset_index(drop=True))
    # print value counts to check
    #print(left_students_flagged['Priority Perf'].value_counts())
    if len(left_students_flagged[left_students_flagged['Priority Perf'] != 0]) > 0:
        print(f"Warning: {len(left_students_flagged[left_students_flagged['Priority Perf'] != 0])} students that left the program have a priority different from 0")

    # remove students that left the program
    df_all_out = df_all[~df_all['Name'].isin(left_students['Name'])].reset_index(drop=True)
    print(f"Removed {len(df_all) - len(df_all_out)} students from data")
    return df_all_out

def remove_last_N_days(df_old, df_new):
    # change Nan values to 0 in columns "Lesson Completed", "Hours On Program", "English Test Taken", "English Test with Excellent/Good"
    for col in ["Lesson Completed", "Hours On Program", "English Test Taken", "English Test with Excellent/Good"]:
        df_new.fillna({col: 0}, inplace=True)
        df_old.fillna({col: 0}, inplace=True)

    df_updated = df_new.copy()
    # drop column "Priority Perf" and "Priority N_Lesson" if there are
    if 'Priority Perf' in df_new.columns:
        df_updated.drop('Priority Perf', axis=1, inplace=True)
    if 'Priority N_Lesson' in df_new.columns:
        df_updated.drop('Priority N_Lesson', axis=1, inplace=True)

    df_updated['Lesson Completed'] = df_updated['Lesson Completed'] - df_old['Lesson Completed']
    df_updated['Hours On Program'] = df_updated['Hours On Program'] - df_old['Hours On Program']
    df_updated['English Test Taken'] = df_updated['English Test Taken'] - df_old['English Test Taken']
    df_updated['English Test with Excellent/Good'] = df_updated['English Test with Excellent/Good'] - df_old['English Test with Excellent/Good']
    df_updated['Overall Percentage Score'] = 100* df_updated['English Test with Excellent/Good']/df_updated['English Test Taken']
    return df_updated