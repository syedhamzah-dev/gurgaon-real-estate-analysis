import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('raw_data.csv')


# Data Cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")
df=df.drop_duplicates()

# Numeric columns cleaning
df['price']=df['price'].astype(str).str.replace(",","").astype(float)
df['area']=df['area'].astype(str).str.replace(",","").astype(int)
df['rate_per_sqft']=df['rate_per_sqft'].astype(str).str.replace(",","").astype(int)

# Categories Column cleaning
df['status']= df['status'].str.strip().str.lower()
df['rera_approval']=df['rera_approval'].str.strip().str.lower().map({"approved by rera": True, 'not approved by rera': False})
df['flat_type']=df['flat_type'].str.strip().str.lower()

df=df.drop_duplicates()

print(df)
print(df.info())


#? Question 1: Which is the costliest flat in the dataset? 
costliest_flat=df.loc[df['price'].idxmax()]
print(costliest_flat)

#? Question 2: Which locality has the highest average price?
highest_avg_price_locality=df.groupby('locality')['price'].mean().idxmax()
print(f'''
The locality with highest average price is {highest_avg_price_locality}''')

#? Question 3: Which locality has the highest rate per square foot?
highest_rate_per_sqft_locality = df.groupby('locality')['rate_per_sqft'].mean().sort_values(ascending=False).head()
print(f"the locality with the highest rate per square foot is {highest_rate_per_sqft_locality}")

#? Question 4: Do ready-to-move properties cost more than under-construction properties?
ready_to_move_avg_price = df[df['status']=="ready to move"]['price'].mean()
under_construction_avg_price = df[df['status']=="under construction"]['price'].mean()

if ready_to_move_avg_price > under_construction_avg_price:
    print("Ready-to-move properties cost more than under-construction properties.")
else:
    print("Under-construction properties cost more than ready-to-move properties.")

#? Question 5: Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval']==True]['price'].mean()
not_rera_approved_avg_price = df[df['rera_approval']==False]['price'].mean()

if rera_approved_avg_price > not_rera_approved_avg_price:
    print("RERA-approved properties command a price premium.")
else:
    print("RERA-approved properties do not command a price premium.")

#? Question 6: How does area (sqft) impact property price?

sns.scatterplot(x='area',y='price',data=df)
plt.show()
print("The area is not impacting the property price")

#? Question 7: Which BHK configuration is the most expensive on average?
most_expensive_bhk_config = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
print(f"The most expensive BHK configuration is {most_expensive_bhk_config} BHK.")

#? Question 8: Which property type (Apartment, Floor, Plot) is the costliest? 
costliest_property_type=df.groupby('flat_type')['rate_per_sqft'].mean().idxmax()
print(f"The costliest property type is {costliest_property_type}.")

#? Question 9: Do certain builders or companies consistently price higher?
print("These 5 builders price higher are:", end=" " )

top_5_builder=df.groupby('company_name')['rate_per_sqft'].mean().sort_values(ascending=False).head(5)

for builder in top_5_builder.index:
    print(builder, end=", ")


#? Question 10: Are larger homes always more expensive per square foot?
sns.scatterplot(x='area',y='rate_per_sqft', data=df)
plt.show()

