import pandas as pd

# Load the CSV file into a pandas DataFrame

data_url = 'https://raw.githubusercontent.com/kernelshreyak/ai-ml-learning/refs/heads/master/datascience/datasets/scoobydoo.csv'

df = pd.read_csv(data_url)

# Find the title with the maximum IMDb rating
max_rating_title = df.loc[df['imdb'].idxmax()]
print(max_rating_title[['title', 'imdb']])