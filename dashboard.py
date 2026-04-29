day_2011 = day[day['yr'] == 2011] # 0 = 2011, 1 = 2012
plt.figure(figsize=(12,6))
sns.scatterplot(data=day_2011, x='temp', y='cnt', hue='mnth', palette='viridis', alpha=0.7)

plt.title('Pengaruh Suhu terhadap Penyewaan Sepeda per Bulan (2011)')
plt.xlabel('Temperature')
plt.ylabel('Total Rentals')
plt.legend(title='Month')
plt.show()

plt.figure(figsize=(10,5))
sns.regplot(data=day_2011, x='temp', y='cnt',
            scatter_kws={'alpha':0.3},
            line_kws={'color':'red'})

plt.title('Korelasi Suhu vs Penyewaan (2011)')
plt.show()

monthly_data = day_2011.groupby('mnth').agg({
    'temp': 'mean',
    'cnt': 'sum'
}).reset_index()

plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_data, x='mnth', y='cnt', marker='o', label='Total Rentals')
sns.lineplot(data=monthly_data, x='mnth', y='temp', marker='o', label='Avg Temp')

plt.title('Tren Suhu dan Penyewaan per Bulan (2011)')
plt.xlabel('Month')
plt.legend()
plt.show()


plt.figure(figsize=(8,5))
sns.barplot(data=day, x='yr', y='cnt', palette='viridis')

plt.title('Total Penyewaan Sepeda: 2011 vs 2012')
plt.xlabel('Tahun')
plt.ylabel('Total Rentals')
plt.show()