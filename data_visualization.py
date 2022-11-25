import pandas as pd
import plotly.express as px
from clean_data import cleaning_data
import matplotlib.pyplot as plt
import seaborn as sns

data_path = '../../Downloads/my_vivino/data/vivino.csv'
df = cleaning_data(data_path)


def most_frequent(column, data=df):
    data = data[column].value_counts().to_frame().reset_index().rename(columns={column: 'Count', 'index': column}) # grouping the dataset by a givin feature.
    fig = px.bar(data, x=column, y='Count', color='Count', color_continuous_scale='plotly3_r')
    fig.update_layout(autosize=False, width=950, height=600, xaxis_title='Wine Type',
                            yaxis_title="Count",) # formating.
    fig.show()


def dist(x, color=None, data=df, log=False,  nbins=None): # a function to get hte distripution.
    print(f'Average wine {x} = {round(data[x].mean(),2)}')
    print(f'Most frequent wine {x} = {round(data[x].mode()[0],2)}')
    fig = px.histogram(data, x=x, color=color, log_y=log,  nbins= nbins )
    fig.update_layout(width=950, height=600, xaxis=dict(range=[2,5]), yaxis=dict(range=[0,600]))
    fig.show()


def most_wine(by, data=df, col='Name', n=20): # a function get the top wine of some column.
        d = data[[col,by]].sort_values(by=by, ascending = False).head(n)
        fig = px.bar(d ,x=col, y=by, barmode='group', color=by, color_continuous_scale='plotly3_r') # ploting a Plotly bar chart that shows the number of releases.
        fig.update_layout(autosize=False, width=950, height=600, xaxis_title=col,
                        yaxis_title=by) # formating.
        fig.show()


def most_by(col, by, data=df): # a function gets the top items of some columns to another column.
    d = data[[col,by]].groupby(col).mean().sort_values(by=by, ascending = False)
    fig = px.bar(d ,x=d.index, y=by, barmode='group', color=by, color_continuous_scale='plotly3_r') # ploting a Plotly bar chart that shows the number of releases.
    fig.update_layout(autosize=False, width=950, height=600, xaxis_title=col,
                    yaxis_title=by) # formating.
    fig.show()


def relations(cols, color=None, data=df): # a function plots the relationships between some columns.
        fig = px.scatter_matrix(data,
            dimensions=cols,
            color=color, symbol=color)
        fig.update_layout(autosize=False, width=950, height=600)
        fig.show()


def precentages(cols, tops, data=df, color=None): # a function plots the precentages of some columns to others.
        grouped = data[cols].groupby(cols).size().sort_values(ascending=False).reset_index()
        list_of_groups = []
        for col,top in zip(cols[:-1],tops):
            for unique in data[col].unique():
                list_of_groups.append(grouped[grouped[col] == unique].head(top))
        grouped_t_c = pd.concat(list_of_groups)
        
        fig = px.sunburst(grouped_t_c, path=cols, values = 0, color=color)
        
        fig.update_layout(autosize=False, width=950, height=600)
        fig.show()


def by_date(cols, data=df, color=None):
    data = data.reset_index().groupby("Year").sum()
    fig = px.bar(df, y=cols, color=color,  width=950, height=600)
    fig.update_layout(
            autosize=False,
            xaxis=dict(range=[1990,2022]))
    fig.show()


def compute_correlations_matrix(dataset):
    plt.figure(figsize=(10, 10))
    sns.heatmap(dataset.corr(), annot=True, cmap="YlOrRd", linewidths=0.1, annot_kws={"fontsize":10})
    plt.title("Correlation house prices - return rate")
    return plt.show()