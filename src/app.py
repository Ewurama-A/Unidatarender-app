# import libraries
import numpy as np

from dash import Dash,html,dcc,Input,Output,callback,State

import plotly.express as px

import pandas as pd


# save dataset in variable 'df'
df = pd.read_csv("https://github.com/Ewurama-A/Unidatarender-app/blob/main/merged_Uniersity_data.csv")


# Creating graph of international students per location using plotly
location_graph = px.scatter(df.query("scores_teaching>50"),x= 'stats_number_students',y= 'stats_pc_intl_students',size = 'stats_number_students',color='location',hover_name='name',title = 'Percentage of International students',color_discrete_sequence=px.colors.qualitative.Set1)

# Updating layouts and axes
location_graph.update_layout(title_font_color='#4a044e',plot_bgcolor="#e4e4e7",paper_bgcolor='#e4e4e7',margin=dict(l=10, r=10, t=60, b=30),legend_title_text='Location')

location_graph.update_xaxes(title_text='Student Population',showgrid = False)

location_graph.update_yaxes(title_text='International Students (Percentage)')


# Creating graph about gender population of top univsersities.
gender_graph = px.bar(df.query('scores_teaching>80'), x=["male_population","female_population"], y='name', title="Gender Population of Major Universities",hover_name='location',color_discrete_sequence=px.colors.qualitative.Pastel1,text ='name')

# Updating axes and layout of the graph
gender_graph.update_layout(title_font_color='#4a044e',plot_bgcolor="#e4e4e7",paper_bgcolor='#e4e4e7',margin=dict(l=10, r=10, t=40, b=30),legend_title_text='Gender')

gender_graph.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)

gender_graph.update_yaxes(title_text = 'University name',color='black',autorange = 'reversed',showticklabels= False,showgrid = False)

gender_graph.update_xaxes(title_text = 'Gender population',showgrid=False)


# New dataframe containing ISO numbers for location on a world map graph
df1 = px.data.gapminder().query("year==2007")

# changing column name and preparing it for merge with original dataframe (df).
df1['location'] = df1['country']

# Grouping columns needed for merge and storing it in a new variable.
df2 = df1[['location','iso_alpha','iso_num','continent']]

# Merging new dataframe (df2) with original (df) and storing under new name df3
df3 = df.merge(df2, how = 'left', on ='location')

df3.query('scores_teaching>80')

# Checking if new dataframe contains right information.
df3.loc[df3['name'] == 'The University of Tokyo', 'location'].item()


# Creating world map with new datafram df3 using location, continent, iso_numbers and university name with plotly scatter_geo.
world_map = px.scatter_geo(df3.query('scores_teaching>30'), locations="iso_alpha", color="continent",hover_name='name', size = 'scores_international_outlook',
                     projection="equirectangular",title = "Universities with best international outlook")

world_map.update_layout(title_font_color='#4a044e',plot_bgcolor="#e4e4e7",paper_bgcolor='#e4e4e7',height =600, margin=dict(l=5, r=5, t=60,b=5),legend_title_text='Continent', legend_orientation= 'h')

# Creating variables for mean students, number of locations, and number of universities available. Use for dashboard.
uni_num = df.name.nunique() 

location_num = df.location.nunique() 

stu_mean = np.mean(df['stats_number_students'])
stu_mean = np.around(stu_mean,0)




# Tailwind CSS is set as the default css style.DASH is used to create an html page.
# The dashboard has four main layouts: the h1 heading, the div containing the graphs,callbacks and KPI's, the content side bar and the bottom part acknowledging the copyright.
# The main html and Dash components here are h1, Div,Span, Dcc and callbacks. Callbacks are linked to dropdown menus and sliders to show locations from the university provided and selected and provide a google search on the school as well.
# Tailwind CSS used in each Div is classified as 'ClassName'.

external_script = ["https://tailwindcss.com/", {"src":"https://cdn.tailwindcss.com"}]

app = Dash(__name__, external_scripts=external_script)
server = app.server
app.scripts.config.serve_locally = True


# Dash Script
app.layout = html.Div([
  html.H1("Unidata: Universities of the world", id ='home', className=" shadow-lg w-auto text-white text-4xl italic p-6 m-2 rounded-md text-center bg-[#3b0764] shadow-lg"),
 
  html.Div([  
    
    html.Div([
        html.A( href ='#home', id = 'home', children = 'Home', className = 'shadow-md transition-colors duration-500 ease-in-out hover:bg-[#4f46e5] hover:opacity-75 transform hover:-translate-y-1 hover:scale-100 rounded-lg p-4 font-semibold cursor-pointer block italic  bg-[#cbd5e1] shadow-md'),
        html.A( href ='#graph', id = 'graph', children = 'Graphs', className = 'shadow-md transition-colors duration-500  ease-in-out hover:bg-[#4f46e5] underline hover:opacity-75 transform hover:-translate-y-1 hover:scale-100 rounded-lg p-4 font-semibold cursor-pointer block italic bg-[#cbd5e1] shadow-md'),
        html.A( href ='#info', id = 'info', children = 'University Information', className = 'shadow-md transition-colors  duration-500 ease-in-out hover:bg-[#4f46e5] hover:opacity-75 transform hover:-translate-y-1 hover:scale-100 rounded-lg p-4 font-semibold cursor-pointer block italic  bg-[#cbd5e1] shadow-md')],
        className = 'shadow-md p-2 m-2 bg-[#312e81]  opacity-75 space-y-12  w-auto mb-2 rounded-md shadow-md'),
    
    html.Div([
      html.Div([
        
        html.Div(children=[
             html.Span(uni_num, className="text-5xl text-center my-2 font-bold"),
             html.Span("Universities available", className="text-lg fontmedium m-4 text-center"),
         ],className=" shadow-lg flex flex-col justify-center p-4  text-white itemscenter rounded-md bg-[#4c1d95] shadow-lg"),
         
           html.Div(children=[
             html.Span(location_num, className="text-5xl text-center my-2 font-bold"),
             html.Span("Total locations available", className="text-lg fontmedium ml-4 text-center"),
         ],className=" shadow-lg flex flex-col justify-center p-4  text-white itemscenter rounded-md  bg-[#6d28d9] shadow-lg"),
        
            html.Div(children=[
              html.Span(stu_mean, className="text-5xl text-center my-2 font-bold"),
              html.Span("Average students in a University", className="text-lg fontmedium ml-1 text-center"),
         ],className=" shadow-lg flex flex-col justify-center p-4 text-white itemscenter rounded-md bg-[#4c1d95] shadow-lg")],className="flex flex-row justify-center rounded-md w-auto p-4 m-4 space-x-6 bg-[#e4e4e7] ",id = 'homebar'),
    
       html.Div([
         html.Div(dcc.Graph(id='location_graph',figure =location_graph),className="shadow-lg  rounded-md row-span-2 shadow-lg"),
         html.Div(dcc.Graph(figure=world_map),className="shadow-lg row-span-2 rounded-md  shadow-lg"),
         html.Div(dcc.Graph(id = 'gender_graph', figure = gender_graph),className="shadow-lg  rounded-md row-span-2 shadow-lg"),
         html.Div([
             html.P("Find your dream School.\n Select a University!",className="flex flex-col p-2 justify-center text-black itemscenter font-semibold text-base rounded-sm italic w-full bg-[#6d28d9]"),
             html.Div(dcc.Dropdown(options = df3['name'].unique(), value = 'name',id = 'school'),className='col-span-2 p-2 justify-center italic text-black itemscenter rounded-md w-full bg-[#6d28d9]'),
             html.P(children = "Many Universities are available. Choose one to learn more about it.", id = 'output',className = "shadow-lg p-2 col-span-2 m-2 p-2 italic font-semibold justify-center text-base text-left whitespace-pre-line bg-[#e4e4e7] shadow-lg"),
         ],className="shadow-lg grid grid-cols-2 grid-row-3 gap-2 p-2 space-y-2 justify-center text-black itemscenter rounded-md bg-[#6d28d9] row-span-2 shadow-lg ")
           
           ],id= 'graphbar', className='grid grid-cols-2 grid-rows-4 rounded-md  gap-4 m-2 px-4 py-8 bg-[#e4e4e7]')
        
    ],className = 'col-span-3'),
        
   ],className = 'flex flex-row grid grid-cols-4 gap-2'),
    
   html.Div(children = "Ama Assiamah. Data Copyright: Kaggle. @2023", className =" w-full text-white text-md italic p-4 text-center bg-[#4c1d95]")],
   className="flex flex-col w-full bg-[#e4e4e7] max-w-full")


@app.callback(
        Output(component_id = 'output',component_property = 'children'),
        Input(component_id = 'school', component_property = 'value'))

def unidata(g):
    dff = df3[['name','location','continent','stats_number_students','scores_teaching','scores_international_outlook','subjects_offered','male_population','female_population']]
    
    l = dff.loc[dff['name'] == g,'location'].item()
    c = dff.loc[dff['name'] == g,'continent'].item()
    s = dff.loc[dff['name'] == g,'stats_number_students'].item()
    t = dff.loc[dff['name'] == g,'scores_teaching'].item()
    i = dff.loc[dff['name'] == g,'scores_international_outlook'].item()
    
    o = dff.loc[dff['name'] == g,'subjects_offered'].item().split(',')[:7]
    o1 = "{},{},{},\n{},{} and {}, amongst others.".format(*o)
    
    m = dff.loc[dff['name'] == g,'male_population'].item()
    f = dff.loc[dff['name'] == g,'female_population'].item()
    
    return '''        {0} is located in {1}. 
        Continent: {2}. 
        Number of Students (2022): {3}.  
        Overall Teaching Score in % (2022): {4}.
        Overal international score in % (2022): {5}.
        
        Subjects Offered:
        {6}
        
        Male Population (2022): {7}.
        Female Population (2022):{8}.'''.format(g,l,c,s,t,i,o1,m,f)
   
    
if __name__ == "__main__":
     app.run_server()
