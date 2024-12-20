

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# from google.colab import drive
# drive.mount('/content/drive')

def load_and_clean_data(file_path):
    df = pd.read_excel(file_path)  # Reading Excel file

    # Convert 'Sales' and 'Profit' columns to numeric (in case they are not in numeric format)
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')  # 'coerce' will convert errors to NaN
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')

    # Drop rows with any missing values in numeric columns
    df = df.dropna(subset=['Sales', 'Profit'])

    return df

def plot_histogram(df, column):
    plt.figure(figsize=(10,6))
    sns.histplot(df[column], kde=True, bins=30)
    plt.title(f'{column} Distribution')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.savefig('histogram.png')
    plt.show()

def plot_scatter_with_clusters(df, x_col, y_col):
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(df[[x_col, y_col]])
    df['Cluster'] = clusters
    print("fromhere scatter", df['Cluster'].value_counts(), "till here")


    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df[x_col], y=df[y_col], hue=df['Cluster'], palette="viridis")
    plt.title("Scatter Plot with K-means Clustering")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(title="Cluster")
    plt.savefig("scatterplot.png")
    plt.show()
    print("Scatter plot saved!")

def plot_heatmap(df):
    numeric_df = df.select_dtypes(include=['number'])
    correlation = numeric_df.corr()
    plt.figure(figsize=(10,6))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.savefig("heatmap.png")

    plt.show()

def plot_elbow(df, columns):
    # Standardize the data before KMeans
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[columns])

    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_data)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10,6))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method for KMeans Clustering')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.savefig("elbow.png")

    plt.show()

def plot_linear_regression(df, column1, column2):
    X = df[column1].values.reshape(-1, 1)  # Reshaping for linear regression
    y = df[column2]

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    plt.figure(figsize=(10,6))
    plt.scatter(df[column1], df[column2], color='blue', alpha=0.5)
    plt.plot(df[column1], y_pred, color='red', linewidth=2)
    plt.title(f'Linear Regression: {column1} vs {column2}')
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.savefig("Linear.png")
    plt.show()

def main():
    # Load and clean data
    file_path = "Retail-Supply-Chain-Sales-Dataset.xlsx"  # Update with your file name
    df = load_and_clean_data(file_path)

    # Ensure sufficient numeric data for all plots
    if df.shape[1] < 2:
        print("ERROR: The dataset must have at least two numeric columns.")
        return

    # Select columns for plots (adjust as needed)
    column1 = 'Sales'  # Adjust this as needed
    column2 = 'Profit'  # Adjust this as needed

    # Print data summary
    print(df[['Sales', 'Profit']].describe())

    # Generate Plots
    plot_histogram(df, column1)
    plot_scatter_with_clusters(df, column1, column2)
    plot_heatmap(df)
    plot_elbow(df, [column1, column2])
    plot_linear_regression(df, column1, column2)

# Execute main function
if __name__ == "__main__":
    main()
