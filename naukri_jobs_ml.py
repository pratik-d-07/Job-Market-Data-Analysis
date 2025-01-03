import pandas as pd

def fill_salary(min_experience):
    if min_experience == 0:
        return 350000
    elif min_experience in [1, 2]:
        return 500000
    elif min_experience in [3, 4, 5]:
        return 900000
    elif min_experience in [6, 7, 8, 9]:
        return 1500000
    elif min_experience in [10, 11, 12, 13]:
        return 2000000
    else:  # 14 years and above
        return 3000000

# Load the CSV file
df = pd.read_csv('naukri_jobs_pp.csv')

# Filter rows where 'Avg Salary' is not empty or NaN
df['Avg Salary'] = df['Avg Salary'].fillna(df['Min Experience'].apply(fill_salary))

df.to_csv('naukri_jobs_ml.csv', index=False)
