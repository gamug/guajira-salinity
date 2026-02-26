import config, os
import plotly.express as px, plotly.graph_objects as go
from sklearn.impute import KNNImputer
import pandas as pd, numpy as np
from scipy import stats
import geopandas as gpd

from commons import profile_dataset


def get_salinity() -> pd.DataFrame:
    """Fetch the salinity dataset from the specified URL and save it locally."""
    try:
        salinity = pd.read_csv(os.environ['SALINITY_URL'])
        salinity.to_csv(os.path.join(config.path['raw_data'], '_Salinidad_Guajira.csv'), index=0)
        return salinity
    except Exception as e:
        raise e

def select_salinity_cols(salinity: pd.DataFrame) -> pd.DataFrame:
    """Select and clean the relevant columns from the salinity dataset based on the configuration.
    This function performs several cleaning steps, including:
    - Removing non-numeric characters from numeric columns and converting them to the appropriate data types.
    - Replacing zero values in numeric columns with NaN to indicate missing data.
    - Dropping columns that are excluded or have too many missing values.
    - Standardizing categories in the 'Uso_del_Su' column based on defined aliases.
    Args:
        salinity (pd.DataFrame): The raw salinity dataset to be processed.
    Returns:
        pd.DataFrame: The cleaned and pre-curated salinity dataset.
    """
    for col, typ in config.salinity_data_dictionary.items():
        if typ in [float, int]:
            salinity[col] = salinity[col].astype(str).str.replace('[^a-zA-Z0-9.,]', '', regex=True)
            if typ==float:
                salinity[col] = salinity[col].str.replace(',', '.', regex=True).str.replace('[a-zA-Z]+', '', regex=True)
            for i in range(5):
                salinity[col] = salinity[col].replace(' '*i, np.nan)
    for col, typ in config.salinity_data_dictionary.items():
        if typ in [str, 'category']:
            for i in range(5):
                salinity[col] = salinity[col].replace(' '*i, np.nan)
        if typ in [float, int]:
            salinity.loc[salinity[col]==0, col] = np.nan
    salinity.drop(config.salinity_exclude_cols, axis=1, inplace=True)
    salinity.drop(config.salinity_missing_cols, axis=1, inplace=True)
    #excluding registers with more than 5 mising values
    salinity = salinity[salinity.isna().sum(axis=1)<5]
    #standard Uso_del_Su col categories
    for label, aliases in config.salinity_group_use_aliases.items():
        salinity['Uso_del_Su'] = salinity['Uso_del_Su'].replace({alias: label for alias in aliases})
    salinity = salinity.astype({key: value for key, value in config.salinity_data_dictionary.items() if key in salinity.columns})
    #exporting pre-curated database
    salinity.to_csv(os.path.join(config.path['precurated_data'], 'salinity_precurated.csv'), index=0)
    return salinity.reset_index(drop=True)

def input_numeric_cols(salinity: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values in numeric columns of the salinity dataset using KNN imputation.
    This function selects the numeric columns from the salinity dataset, applies KNN imputation to
    fill in missing values, and returns a new DataFrame containing the imputed numeric data.
    Args:
        salinity (pd.DataFrame): The salinity dataset with potential missing values in numeric columns.
    Returns:
        pd.DataFrame: A DataFrame containing the numeric columns with imputed values.
    """
    numeric_inputted_set = salinity[config.salinity_numeric_cols]
    imputer = KNNImputer(n_neighbors=3)
    numeric_inputted_set = pd.DataFrame(
        data=imputer.fit_transform(numeric_inputted_set),
        columns=numeric_inputted_set.columns
    )
    return numeric_inputted_set

def join_gepandas(file_path: str) -> pd.DataFrame:
    """Create a geospatially joined dataset of salinity points and hydrogeologic classes. 
    This function builds an output file linking salinity locations to their corresponding hydrogeologic classification.

    Args:
        file_path: Destination path where the joined dataset will be saved as a CSV file.

    Returns:
        pd.DataFrame: The geospatially joined dataset of salinity points and hydrogeologic classes.
    """
    hidrogeology = gpd.read_file(os.path.join(config.path['raw_data'], 'Mapa_hidrogeologico_polygon.zip'))
    hidrogeology = hidrogeology[['class_hidr', 'geometry']]
    hidrology_cats = gpd.read_file(os.path.join(config.path['raw_data'], '_Salinidad_Guajira.zip'))
    hidrology_cats = hidrology_cats.to_crs(hidrogeology.crs)
    hidrology_cats = gpd.sjoin(hidrology_cats, hidrogeology, how="left", predicate="within")
    hidrology_cats = hidrology_cats[['X', 'Y', 'class_hidr']]
    hidrology_cats.to_csv(file_path, index=0)
    return hidrology_cats

def estimate_terciles(values: pd.Series) -> tuple[float]:
    """Estimate tercile thresholds from a salinity distribution using an alpha distribution fit.
    This function derives two cutoff values that split the input salinity values into three categories.

    Args:
        values (pd.Series): Series of numeric salinity values used to fit the distribution and compute terciles.

    Returns:
        tuple[float]: A tuple containing the first and second tercile thresholds.
    """
    a, b, c = stats.alpha.fit(values)
    fig = px.histogram(values, nbins=50, opacity=0.6, histnorm='probability density',
                    title="Histogram with Fitted Normal Distribution")
    x = np.linspace(min(values), max(values), 100)
    pdf = stats.alpha.pdf(x, a, b, c)
    fig.add_trace(go.Scatter(x=x, y=pdf, mode='lines', name='Fitted Distribution'))
    # Show plot
    fig.write_html(os.path.join(config.path['curated_data'], 'distribution_aproximation.html'))
    #tercile calculus
    q1 = stats.alpha.ppf(1/3, a, b, c)
    q2 = stats.alpha.ppf(2/3, a, b, c)
    return q1, q2

def get_salt_categories(dataset: pd.DataFrame) -> pd.DataFrame:
    """Categorize salinity values into three categories based on estimated terciles.
    This function assigns a categorical label to each salinity value in the dataset
    based on its position relative to the estimated tercile thresholds. The categories are defined as follows:
    - 'SALINIDAD_BAJA' for values below the first tercile (q1)
    - 'SALINIDAD_MEDIA' for values between the first and second terciles (q1 and q2)
    - 'SALINIDAD_ALTA' for values above the second tercile (q2)
    After categorization, the original numeric salinity column is dropped from the dataset.
    Args:
        dataset (pd.DataFrame): The input dataset containing a numeric 'SAL' column to be categorized.
    Returns:
        pd.DataFrame: The dataset with a new 'CATEGORIA_SAL' column containing the salinity categories,
        and the original 'SAL' column removed.
    """
    q1, q2 = estimate_terciles(dataset['SAL'])
    dataset.loc[(dataset.SAL<q1), 'CATEGORIA_SAL'] = 'SALINIDAD_BAJA'
    dataset.loc[(dataset.SAL>q1)&(dataset.SAL<q2), 'CATEGORIA_SAL'] = 'SALINIDAD_MEDIA'
    dataset.loc[(dataset.SAL>q2), 'CATEGORIA_SAL'] = 'SALINIDAD_ALTA'
    dataset = dataset.drop('SAL', axis=1)
    return dataset

def build_dataset(numeric_inputted_set: pd.DataFrame, salinity: pd.DataFrame) -> pd.DataFrame:
    """Construct the final curated salinity dataset by combining imputed numeric data with categorical data and hydrogeologic classifications.
    This function performs several steps to build the final dataset:
    - It starts with the imputed numeric dataset and adds the relevant categorical columns from the original salinity dataset.
    - It performs a geospatial join to associate each salinity point with its corresponding hydrogeologic class, using the 'X' and 'Y' coordinates for the join.
    - It categorizes the salinity values into defined categories based on estimated terciles.
    - It drops columns that are excluded from correlation analysis and filters the dataset to include only records of type 'Pozo'.
    - Finally, it removes duplicates based on the 'X' and 'Y' coordinates and saves the curated dataset as a CSV file in the designated directory.
    Args:
        numeric_inputted_set (pd.DataFrame): The dataset containing imputed numeric values for the salinity data.
        salinity (pd.DataFrame): The original salinity dataset containing categorical columns and coordinates.
    Returns:
        pd.DataFrame: The final curated salinity dataset ready for analysis.
    """
    dataset = numeric_inputted_set.copy()
    dataset[config.salinity_cat_cols] = salinity[config.salinity_cat_cols]
    file_path = os.path.join(config.path['curated_data'], 'hidrology_cats.csv')
    hidrology_cats = pd.read_csv(file_path) if os.path.exists(file_path) else join_gepandas(file_path)
    dataset = dataset.join(hidrology_cats.set_index(['X', 'Y']), on=('X','Y')).dropna(subset=['class_hidr'])
    dataset = get_salt_categories(dataset)
    dataset.drop(config.salinity_correlation_excludes, axis=1, inplace=True)
    dataset = dataset[dataset.Tipo_de_Ca=='Pozo']
    dataset = dataset.drop(['T_Seco', 'Tipo_de_Ca'], axis=1)
    dataset = dataset.drop_duplicates(['X', 'Y'])
    dataset.to_csv(os.path.join(config.path['curated_data'], 'salinity_curated.csv'), index=0)
    return dataset

def process_data():
    """Execute the full data processing pipeline for the salinity dataset.
    This function orchestrates the entire data processing workflow, which includes:
    - Fetching the raw salinity dataset from the specified URL.
    - Generating a profiling report for the raw dataset and saving it.
    - Selecting and cleaning the relevant columns from the raw dataset, and generating a profiling report for the pre-curated dataset.
    - Imputing missing values in the numeric columns of the pre-curated dataset.
    - Building the final curated dataset by combining the imputed numeric data with categorical data and hydrogeologic classifications, and generating a profiling report for the final curated dataset.
    Args:
        None
    Returns:
        None
    """
    salinity = get_salinity()
    _ = profile_dataset(salinity, name='raw-salinity_report', save=True)
    salinity_ = select_salinity_cols(salinity)
    _ = profile_dataset(salinity_, name='precurated-salinity_report', save=True)
    numeric_inputted_set = input_numeric_cols(salinity_)
    dataset = build_dataset(numeric_inputted_set, salinity_)
    _ = profile_dataset(dataset, name='curated-salinity_report.html', save=True)