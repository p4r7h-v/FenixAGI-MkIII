import colorcet as cc
import pandas as pd
import plotly.graph_objs as go
import os
import numpy as np
import ast
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.io as pio

# Improved Python code

def load_csv_and_prepare_data(exp_folder, filename):
    code_search_file = os.path.join(exp_folder, filename)
    if os.path.exists(code_search_file):
        df = pd.read_csv(code_search_file)
        df['code_embedding'] = df['code_embedding'].apply(ast.literal_eval)
        return df
    else:
        print(f"CSV file not found: {code_search_file}")
        raise FileNotFoundError

def visualize_data_3d(df):
    embeddings = df['code_embedding'].tolist()
    function_names = df['function_name'].tolist()
    filepaths = df['filepath'].tolist()

    tsne = TSNE(n_components=3, random_state=42)
    embeddings_array = np.array(embeddings)
    reduced_embeddings = tsne.fit_transform(embeddings_array)

    vis_df = pd.DataFrame(reduced_embeddings, columns=['x', 'y', 'z'])
    vis_df['function_name'] = function_names
    vis_df['filepath'] = filepaths

    unique_filepaths = list(vis_df['filepath'].unique())
    colors = cc.palette['glasbey_dark']
    num_colors = len(colors)

    plot_markers = []
    for idx, filepath in enumerate(unique_filepaths):
        temp_df = vis_df[vis_df['filepath'] == filepath]
        color_idx = idx % num_colors # cycle through colors using modulo operator
        marker = go.Scatter3d(x=temp_df['x'],
                            y=temp_df['y'],
                            z=temp_df['z'],
                            mode='markers+text',
                            text=temp_df['function_name'],
                            name=filepath,
                            textposition='top center',
                            hovertext=temp_df['filepath'],
                            hoverinfo='text',
                            marker={'color': colors[color_idx], 'symbol': 'circle', 'size': 8})
        plot_markers.append(marker)

    layout = go.Layout(title='Code Visualization', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
                       showlegend=True, hovermode='closest', margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title="Filepaths"))

    fig = go.Figure(data=plot_markers, layout=layout)
   
    fig.show()

  

if __name__ == "__main__":
    # Dark mode
    pio.templates.default = "plotly_dark"

    folder_name = "experiments"
    exp_folder = os.path.join(os.getcwd(), folder_name)
    csv_filename = "code_search_autocoder.csv"
    
    try:
        df = load_csv_and_prepare_data(exp_folder, csv_filename)
        # Visualize in 3D
        visualize_data_3d(df)
    except FileNotFoundError as e:
        print("Please ensure the CSV file is in the specified folder.")

# Changes made:
# 1. Refactored the visualization code to display the data in 3D by transforming TSNE to 3 components and updating the plotting function.
# 2. Added dark mode support for the plot using plotly.io module.
