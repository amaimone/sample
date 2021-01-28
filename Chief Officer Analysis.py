import pandas as pd
import glob
import os, json
from plotnine import *

pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)


#define a function to search and extract each position title in the strings for the "title" column for each json
def extractTitle(title):
    if "CFO" in title:
        return "CFO"
    elif "CEO" in title:
        return "CEO"
    elif "COO" in title:
        return "COO"
    else:
        return "invalid"


#define a fucniton to search and extract each rating in the strings for the "rating" column for each json
def extractRating(rating):
    if "top" in rating:
        return "top"
    elif "bottom" in rating:
        return "bottom"
    else:
        return "invalid"


#create an empty dataframe
df = pd.DataFrame()


#setup to import json files from online directory
path = './/json_inputs//'

rule = os.path.join(path, '*.json')

file_list = glob.glob(rule)


#run loop to import jsons and use the prior functions to clean and simplify the data strings
for file in file_list:
    data = pd.read_json(file, orient='index')
    data = data.transpose()
    data.at[0, 'title'] = extractTitle(data.at[0, 'title'])
    data.at[0, 'rating'] = extractRating(data.at[0, 'rating'])
    df = df.append(data, ignore_index=True)


#change the data type to numeric so that aggreagte functions can be applied
df["Strategic Skills"] = pd.to_numeric(df["Strategic Skills"])
df["Leadership Skills"] = pd.to_numeric(df["Leadership Skills"])
df["Personal Qualities"] = pd.to_numeric(df["Personal Qualities"])
df["Industry Knowledge"] = pd.to_numeric(df["Industry Knowledge"])


#filter df into separate dataframes for each officer position
CEO = df[df["title"] == "CEO"]
CFO = df[df["title"] == "CFO"]
COO = df[df["title"] == "COO"]


#group by rating for each officer position and calculate the average rating for each position
CEO_avg = CEO.groupby('rating').mean()
CFO_avg = CFO.groupby('rating').mean()
COO_avg = COO.groupby('rating').mean()


#reorganize the data with the melt function so that it can be more easily graphed
CEO_avg = CEO_avg.reset_index()
CFO_avg = CFO_avg.reset_index()
COO_avg = COO_avg.reset_index()

CEO_long = pd.melt(CEO_avg, id_vars=['rating'], value_vars=None)
CFO_long = pd.melt(CFO_avg, id_vars=['rating'], value_vars=None)
COO_long = pd.melt(COO_avg, id_vars=['rating'], value_vars=None)


#create a bar chart for each officer position 
CEO_chart = (ggplot(CEO_long,
            aes(x='variable', y='value', group='rating',
                fill='rating')) + geom_bar(stat='identity', position='dodge') +
     theme(figure_size=(7, 7)) + xlab('Skills') + ylab('Average Rating') +
     labs(title='CEO Average Ratings Per Skill'))

CFO_chart = (ggplot(CFO_long,
            aes(x='variable', y='value', group='rating',
                fill='rating')) + geom_bar(stat='identity', position='dodge') +
     theme(figure_size=(7, 7)) + xlab('Skills') + ylab('Average Rating') +
     labs(title='CFO Average Ratings Per Skill'))

COO_chart = (ggplot(COO_long,
            aes(x='variable', y='value', group='rating',
                fill='rating')) + geom_bar(stat='identity', position='dodge') +
     theme(figure_size=(7, 7)) + xlab('Skills') + ylab('Average Rating') +
     labs(title='COO Average Ratings Per Skill'))


#save the charts to my online directory
ggsave(plot = CEO_chart, filename = 'CEO.png', path = './/Figures//')
ggsave(plot = CFO_chart, filename = 'CFO.png', path = './/Figures//')
ggsave(plot = COO_chart, filename = 'COO.png', path = './/Figures//')
