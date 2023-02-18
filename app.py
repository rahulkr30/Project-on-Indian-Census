import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')
st.header('INDIA')
# data frame
df=pd.read_csv('india.csv')
list=['Geopolitics analysis','Religious Population','LITERACY RATE']
# first selectbox
ana=st.sidebar.selectbox('Select Analysis',list)

list_of_states=df['State'].unique().tolist()
list_of_states.insert(0,'Oveall India')



if ana=='Geopolitics analysis':
   selected_state = st.sidebar.selectbox('Select a state',list_of_states)
   primary = st.sidebar.selectbox('Select Primary Parameter',df.columns[[7,37,38]])
   secondary = st.sidebar.selectbox('Select Secondary Parameter',df.columns[[7,37,38]])
   plot = st.sidebar.button('Plot Graph')
   if plot:

       st.text('Size represent primary parameter')
       st.text('Color represents secondary parameter')
       if selected_state == 'Oveall India':
        # plot for india
           temp_df=df[['District code','Latitude','Longitude','District name','Population','literacy_rate','sex_ratio']]
           fig = px.scatter_mapbox(temp_df, lat="Latitude", lon="Longitude", size='Population', color = 'literacy_rate', zoom=4,size_max=35,
                                mapbox_style="carto-positron",width=1200,height=700,hover_name='District name')

           st.plotly_chart(fig,use_container_width=True)
       else:
        # plot for state
            state_df = df[df['State'] == selected_state]

            fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size= primary, color= secondary, zoom=6, size_max=35,
                                mapbox_style="carto-positron", width=1200, height=700,hover_name='District')

            st.plotly_chart(fig, use_container_width=True)


if ana == 'Religious Population':
    selected_state = st.sidebar.selectbox('Select a state',list_of_states)
    list_of_district=df[df['State']==selected_state].District.unique().tolist()
    list_of_district.insert(0,'choose district')
    selected_District = st.sidebar.selectbox('Select a district',list_of_district)
    plot = st.sidebar.button('Plot Graph')
    if plot:
      if selected_state == 'Oveall India':
          temp_df=df.groupby('State')[['Hindus', 'Muslims', 'Christians', 'Sikhs',
              'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].sum()
          st.write('Data Frame of State {} on the basis of Religiion'.format(selected_state))    
          st.dataframe(temp_df)
          st.write("Visualization ".format(selected_state))
          fig=px.imshow(temp_df, text_auto=True, aspect="auto")
          st.plotly_chart(fig, use_container_width=True)
      
      elif (selected_state != 'Oveall India')&(selected_District =='choose district'):
          temp_df=df[df['State']==selected_state][['District','Hindus', 'Muslims', 'Christians', 'Sikhs',
              'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].set_index('District')
          st.write('Data Frame of State {} on the basis of Religiion'.format(selected_state))    
          st.dataframe(temp_df) 
          st.write("Visualization ".format(selected_state))  
          fig=px.imshow(temp_df, text_auto=True, aspect="auto")
          st.plotly_chart(fig, use_container_width=True)    
      elif selected_District !='choose district':
         st.write('Population based on Religion in {}'.format(selected_District))
         temp_df=df[(df['State']==selected_state)& (df['District']==selected_District)][['Hindus', 'Muslims', 'Christians', 'Sikhs',
              'Buddhists', 'Jains', 'Others_Religions', 'Religion_Not_Stated']].melt()
         fig=px.pie(temp_df,names='variable',values='value')
         st.plotly_chart(fig, use_container_width=True) 

if ana == 'LITERACY RATE':
    selected_state = st.sidebar.selectbox('Select a state',list_of_states)
    list_of_district=df[df['State']==selected_state].District.unique().tolist()
    list_of_district.insert(0,'choose district')
    selected_District = st.sidebar.selectbox('Select a district',list_of_district)
    plot = st.sidebar.button('Plot Graph') 

    # adiiding colm
    df['Male leteracy ratio']=df['Male_Literate']/df['Male']*100
    df['Female leteracy ratio']=df['Female_Literate']/df['Female']*100
    if plot:
      if (selected_state != 'Oveall India')&(selected_District =='choose district'):
          temp_df=df[df['State']==selected_state][['District','Population','sex_ratio', 'literacy_rate', 'Male leteracy ratio',
       'Female leteracy ratio']].set_index('District')
          st.write('Data Frame of State {} on the letaracy ratio by district'.format(selected_state))    
          st.dataframe(temp_df) 
          st.write("Visualization {} ".format(selected_state))  
          # viz
          grid=temp_df[['literacy_rate', 'Male leteracy ratio',
          'Female leteracy ratio']]
          fig=px.imshow(grid,text_auto=True, aspect="auto")
          st.plotly_chart(fig, use_container_width=True) 
      # distric literacy        
      elif selected_District !='choose district':
         st.write('literacy rate of women and in  {} district'.format(selected_District))
         temp_df=df[(df['State']==selected_state)& (df['District']==selected_District)][['literacy_rate', 'Male leteracy ratio',
       'Female leteracy ratio']].melt('literacy_rate')
        #viz
         fig=px.sunburst(temp_df,path=['variable'],values='value')
         st.plotly_chart(fig, use_container_width=True) 