#!/usr/bin/env python
# coding: utf-8

# # Student Performance Analysis Using Python
# ## Assignment: Exploratory Data Analysis with NumPy, Pandas, and Matplotlib

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---
# ## Part A – Loading and Exploring Data

# In[2]:


df = pd.read_csv('StudentsPerformance.csv')


# In[3]:


print("=== First 5 rows ===")
df.head()


# In[4]:


print("=== Last 5 rows ===")
df.tail()


# In[5]:


print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")


# In[6]:


print("=== All Column Names ===")
for col in df.columns:
    print(f"  - {col}")


# In[7]:


print("=== Data Types ===")
print(df.dtypes)


# ---
# ## Part B – Data Cleaning

# In[8]:


print("=== Missing Values ===")
print(df.isnull().sum())
print(f"\nTotal missing values: {df.isnull().sum().sum()}")


# In[9]:


print(f"Rows before removing duplicates: {len(df)}")
df.drop_duplicates(inplace=True)
print(f"Rows after removing duplicates: {len(df)}")


# In[10]:


print("=== Verification: Missing Values ===")
print(df.isnull().sum().sum())
print(f"\nDuplicate rows remaining: {df.duplicated().sum()}")
print("\nDataset is clean!")


# ---
# ## Part C – NumPy Analysis

# In[11]:


math_arr = df['math score'].to_numpy()
reading_arr = df['reading score'].to_numpy()
writing_arr = df['writing score'].to_numpy()

print("NumPy arrays created successfully!")
print(f"math_arr shape: {math_arr.shape}")
print(f"reading_arr shape: {reading_arr.shape}")
print(f"writing_arr shape: {writing_arr.shape}")


# In[12]:


print("=" * 50)
print(f"{'Statistic':<25} {'Math':>10} {'Reading':>10} {'Writing':>10}")
print("=" * 50)
print(f"{'Mean':<25} {np.mean(math_arr):>10.2f} {np.mean(reading_arr):>10.2f} {np.mean(writing_arr):>10.2f}")
print(f"{'Median':<25} {np.median(math_arr):>10.2f} {np.median(reading_arr):>10.2f} {np.median(writing_arr):>10.2f}")
print(f"{'Maximum':<25} {np.max(math_arr):>10} {np.max(reading_arr):>10} {np.max(writing_arr):>10}")
print(f"{'Minimum':<25} {np.min(math_arr):>10} {np.min(reading_arr):>10} {np.min(writing_arr):>10}")
print(f"{'Standard Deviation':<25} {np.std(math_arr):>10.2f} {np.std(reading_arr):>10.2f} {np.std(writing_arr):>10.2f}")
print("=" * 50)


# In[13]:


df['Average Score'] = np.mean([math_arr, reading_arr, writing_arr], axis=0)
print("New column 'Average Score' created!")
df[['math score', 'reading score', 'writing score', 'Average Score']].head(10)


# ---
# ## Part D – Data Analysis with Pandas

# ### 1. Which student achieved the highest average score?

# In[14]:


top_student = df.loc[df['Average Score'].idxmax()]
print(f"Student with highest average score:")
print(f"  Index: {df['Average Score'].idxmax()}")
print(f"  Gender: {top_student['gender']}")
print(f"  Race/Ethnicity: {top_student['race/ethnicity']}")
print(f"  Parental Education: {top_student['parental level of education']}")
print(f"  Math: {top_student['math score']}, Reading: {top_student['reading score']}, Writing: {top_student['writing score']}")
print(f"  Average Score: {top_student['Average Score']:.2f}")


# ### 2. Which subject has the highest average marks?

# In[15]:


subject_avg = {
    'Math': df['math score'].mean(),
    'Reading': df['reading score'].mean(),
    'Writing': df['writing score'].mean()
}
print("Average marks by subject:")
for subject, avg in subject_avg.items():
    print(f"  {subject}: {avg:.2f}")
print(f"\nHighest average subject: {max(subject_avg, key=subject_avg.get)} ({max(subject_avg.values()):.2f})")


# ### 3. How many students scored above 90 in Mathematics?

# In[16]:


above_90_math = df[df['math score'] > 90].shape[0]
print(f"Students who scored above 90 in Mathematics: {above_90_math}")


# ### 4. Average score grouped by Gender

# In[17]:


gender_avg = df.groupby('gender')[['math score', 'reading score', 'writing score', 'Average Score']].mean()
print("Average scores grouped by Gender:")
print(gender_avg.round(2))


# ### 5. Average score grouped by Parental Level of Education

# In[18]:


parental_avg = df.groupby('parental level of education')[['math score', 'reading score', 'writing score', 'Average Score']].mean()
print("Average scores grouped by Parental Level of Education:")
print(parental_avg.round(2))


# ### 6. Which lunch type resulted in higher average marks?

# In[19]:


lunch_avg = df.groupby('lunch')[['math score', 'reading score', 'writing score', 'Average Score']].mean()
print("Average scores grouped by Lunch type:")
print(lunch_avg.round(2))
print(f"\nHigher average marks: '{lunch_avg['Average Score'].idxmax()}' lunch type ({lunch_avg['Average Score'].max():.2f})")


# ### 7. Compare students who completed test preparation vs those who did not

# In[20]:


test_prep_avg = df.groupby('test preparation course')[['math score', 'reading score', 'writing score', 'Average Score']].mean()
print("Average scores grouped by Test Preparation Course:")
print(test_prep_avg.round(2))
print(f"\nStudents who completed test prep scored higher on average: {test_prep_avg.loc['completed', 'Average Score']:.2f} vs {test_prep_avg.loc['none', 'Average Score']:.2f}")


# ---
# ## Part E – Visualization

# ### 1. Histogram – Distribution of Math Scores

# In[21]:


plt.figure(figsize=(10, 6))
plt.hist(df['math score'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
plt.title('Distribution of Math Scores', fontsize=16, fontweight='bold')
plt.xlabel('Math Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['math score'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: {df['math score'].mean():.1f}")
plt.legend(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('histogram_math_scores.png', dpi=150)
plt.show()


# ### 2. Bar Chart – Average Score in Math, Reading, Writing

# In[22]:


subjects = ['Math', 'Reading', 'Writing']
averages = [df['math score'].mean(), df['reading score'].mean(), df['writing score'].mean()]
colors = ['#e74c3c', '#3498db', '#2ecc71']

plt.figure(figsize=(8, 6))
bars = plt.bar(subjects, averages, color=colors, edgecolor='black', width=0.5)
for bar, avg in zip(bars, averages):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{avg:.1f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.title('Average Score by Subject', fontsize=16, fontweight='bold')
plt.xlabel('Subject', fontsize=12)
plt.ylabel('Average Score', fontsize=12)
plt.ylim(0, max(averages) + 10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('bar_chart_avg_scores.png', dpi=150)
plt.show()


# ### 3. Scatter Plot – Reading Score vs Writing Score

# In[23]:


plt.figure(figsize=(10, 7))
plt.scatter(df['reading score'], df['writing score'], alpha=0.5, c='purple', edgecolors='black', s=40)
plt.title('Reading Score vs Writing Score', fontsize=16, fontweight='bold')
plt.xlabel('Reading Score', fontsize=12)
plt.ylabel('Writing Score', fontsize=12)

z = np.polyfit(df['reading score'], df['writing score'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['reading score'].min(), df['reading score'].max(), 100)
plt.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'Trend (slope={z[0]:.2f})')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_reading_vs_writing.png', dpi=150)
plt.show()


# ### 4. Pie Chart – Distribution of Students by Gender

# In[24]:


gender_counts = df['gender'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
        colors=['#ff6b6b', '#4ecdc4'], startangle=90, explode=[0.03, 0.03],
        textprops={'fontsize': 14})
plt.title('Distribution of Students by Gender', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('pie_chart_gender.png', dpi=150)
plt.show()


# ### 5. Line Plot – Average Score of Every Student (Sorted)

# In[25]:


sorted_avg = df['Average Score'].sort_values().reset_index(drop=True)

plt.figure(figsize=(12, 6))
plt.plot(sorted_avg, color='teal', linewidth=1.5)
plt.title('Average Score of Every Student (Sorted Lowest to Highest)', fontsize=16, fontweight='bold')
plt.xlabel('Student Rank', fontsize=12)
plt.ylabel('Average Score', fontsize=12)
plt.axhline(sorted_avg.mean(), color='red', linestyle='--', linewidth=1.5, label=f"Mean: {sorted_avg.mean():.1f}")
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('line_plot_sorted_avg.png', dpi=150)
plt.show()


# ---
# ## Part F – Interpretation
# 
# ### 1. Which subject appears easiest for students?
# 
# Reading has the highest average marks among all three subjects (approximately 69.8), followed closely by writing (approximately 68.4), and math has the lowest average (approximately 66.0). This suggests that reading appears to be the easiest subject for students overall, while math tends to be the most challenging. The higher standard deviation in math scores also indicates greater variability in student performance.
# 
# ### 2. Does test preparation improve performance?
# 
# Yes, students who completed the test preparation course scored consistently higher across all three subjects compared to those who did not. On average, students who completed test prep scored approximately 5-7 points higher in each subject. This indicates that test preparation has a positive impact on student performance, with the most noticeable improvement seen in writing scores.
# 
# ### 3. Which visualization provided the most useful insight?
# 
# The scatter plot of Reading Score vs Writing Score provided the most useful insight because it clearly shows a strong positive correlation between the two subjects. The tight clustering around the trend line suggests that students who perform well in reading also tend to perform well in writing, indicating these skills are closely related. This visualization makes it easy to identify patterns and outliers in the data.
# 
# ### 4. Suggest one improvement that schools could make based on the data
# 
# Based on the data, schools should implement mandatory test preparation programs for all students. The data clearly shows that students who completed the test preparation course performed significantly better than those who did not. Additionally, since math scores are consistently the lowest across all demographics, schools should allocate more resources to math tutoring and support programs, particularly for students from lower parental education backgrounds who tend to score lower overall.
