import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc_forum_pageviews.csv", index_col='date', parse_dates=['date'])

# Clean data
bottom_views = df['value'].quantile(0.025)
top_views = df['value'].quantile(0.975)
df = df[(df['value'] >= bottom_views) & (df['value'] <= top_views)]

cleaned_row_count = df['value'].count()
print(cleaned_row_count)

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize =(32,10))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():

    df['year'] = df.index.year
    df['month'] = df.index.month
    df_bar = df.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()

    ax = df_bar.plot.bar(legend=True, figsize=(15.14, 13.3))
    ax.set_ylabel("Average Page Views", fontsize=14)
    ax.set_xlabel("Years", fontsize=14)
    fig = ax.figure
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = ([d.strftime('%b') for d in df_box.date])


    # Draw box plots (using Seaborn)
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")
    sns.set_color_codes(palette='deep')

    # Set up the figure with 2 subplots side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(28.8,10.8))
    flier_props = dict(marker='o', markersize=2, markerfacecolor='black')

    # Year-wise Box Plot (Trend)
    axes[0] = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axes[0], palette='husl', flierprops=flier_props)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    axes[1] = sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axes[1], palette='husl', flierprops=flier_props)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
