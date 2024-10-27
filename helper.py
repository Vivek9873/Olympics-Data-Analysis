def medal_tally1(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    # medal_tally = medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index
    medal_tally = medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver']+ medal_tally['Bronze'] 
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['total'] = medal_tally['total'].astype(int)
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = df['region'].dropna()
    country = country.unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country


# Year wise and Country wise analysis
def fetch_data(df,years,country):
    medal_tally11 = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 1
    if years == 'Overall' and country == 'Overall':
        temp_data = medal_tally11
    if years != 'Overall' and country == 'Overall':
        
        temp_data = medal_tally11[medal_tally11['Year']==int(years)]
    if years == 'Overall' and country != 'Overall':
        flag = 0
        temp_data = medal_tally11[medal_tally11['region']==country]
    if years != 'Overall' and country != 'Overall':
        temp_data = medal_tally11[(medal_tally11['Year']==int(years)) & (medal_tally11['region']==country)]
    if flag==1:
        temp_data = temp_data.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    else:
        temp_data = temp_data.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending = True).reset_index()
    temp_data['total'] = temp_data['Gold'] + temp_data['Silver']+ temp_data['Bronze'] 
    
    return temp_data


def data_over_time(df,col):
    nation_over_time = df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time.rename(columns = {'count':col,'Year':'Editions'},inplace = True)
    return nation_over_time


def most_successful(df,sport):
    temp_df = df.dropna(subset=["Medal"])
    if sport!='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    x = temp_df[['Name','Sport','region']].value_counts().reset_index().drop_duplicates(subset=['Name']).head(15)
    x.rename(columns={'count':'Medals','region':'Nation'},inplace = True)
    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_analysis(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True)
    new_df = temp_df[temp_df['region']==country]
    pt = new_df.pivot_table(index = 'Sport',columns = 'Year',values= 'Medal',aggfunc='count').fillna(0).astype(int)
    return pt
    

def most_successful_athlete(df,country):
    temp_df = df.dropna(subset=["Medal"])
    if country!='Overall':
        temp_df = temp_df[temp_df['region']==country]
    x = temp_df[['Name','Sport','region']].value_counts().reset_index().drop_duplicates(subset=['Name']).head(15)
    x.rename(columns={'count':'Medals','region':'Nation'},inplace = True)
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final