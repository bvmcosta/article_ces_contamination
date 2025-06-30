#Libraries
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------
st.set_page_config(layout = 'wide')
#-----------------------------------------------------------------------------
#Functions
def load_data(path1, path2):

    ww_production = pd.read_csv(path1)
    ww_production['WWuc_million_m3_yr'] = ww_production['WWp_million_m3_yr'] - ww_production['WWc_million_m3_yr']
    ww_10producers = ww_production.sort_values('WWp_million_m3_yr', ascending = False).head(10)
    ww_production['Economic_Classification'] = pd.Categorical(ww_production['Economic_Classification'], 
                                                              categories = ['Low income', 'Lower middle income', 'Upper middle income', 'High income'])
    ww_production = ww_production.sort_values('Economic_Classification').reset_index(drop=True)

    ww_stations = pd.read_csv(path2, encoding='latin-1')

    return ww_production, ww_10producers, ww_stations
#-----------------------------------------------------------------------------
def groups_economic_classification(dataframe):

    groups_economic_classification = dataframe[['Economic_Classification', 'WWp_million_m3_yr']].groupby('Economic_Classification').median().reset_index()

    return groups_economic_classification
#-----------------------------------------------------------------------------
def bar_graph_countries(dataframe):
    
    fig1, ax1 = plt.subplots(figsize = (6,4))

    collected = dataframe['WWc_million_m3_yr']
    uncollected = dataframe['WWuc_million_m3_yr']
    
    ax1.bar(dataframe['Country'], collected, color = 'blue')
    ax1.bar(dataframe['Country'], uncollected, color = 'red', bottom = collected)
    ax1.set_ylabel('WWp (million m3/year)', fontsize = 11)
    ax1.set_xlabel('Country', fontsize = 11)
    ax1.legend(['Collected', 'Uncollected'], frameon = False, title = 'Quality of wastewater')
    ax1.tick_params(axis = 'x', labelrotation = 90)
    st.pyplot(fig1, use_container_width = True)
#-----------------------------------------------------------------------------
def boxplot_economic_classification(dataframe):

    fig2, ax2 = plt.subplots(figsize = (6,4))

    sns.boxplot(dataframe, 
                x = dataframe['Economic_Classification'], 
                y = dataframe['WWp_million_m3_yr'], fill = True, color = 'white', linecolor = 'black', log_scale = True, ax = ax2)
    sns.swarmplot(dataframe, 
                  x = dataframe['Economic_Classification'], 
                  y = dataframe['WWp_million_m3_yr'], size = 4, edgecolor = 'red', hue = 'Region', ax = ax2)
    
    ax2.set_ylabel('WWp (million m3/year)', fontsize=11)
    ax2.set_xlabel('Country economic classification', fontsize=11)
    ax2.tick_params(axis = 'both', pad = 7)
    ax2.set_xticklabels(labels = ['Low income', 'Lower middle income', 'Upper middle income', 'High income'], rotation = 90)
    ax2.yaxis.labelpad = 15
    ax2.legend(frameon = False)
    sns.move_legend(ax2, 'upper left', bbox_to_anchor=(1, 1.02))
    st.pyplot(fig2, use_container_width = True)
#-----------------------------------------------------------------------------
def wastewater_plants_count(dataframe1, dataframe2):

    df1 = dataframe1.loc[dataframe1['COAST_10KM'] == 1, ['COUNTRY', 'WASTE_ID']]

    contagem_ww_plants = []

    countries = list(dataframe2['Country'])
    countries[7] = 'Russia'
    
    for country in countries:

        df2 = df1.loc[df1['COUNTRY'] == country, ['COUNTRY', 'WASTE_ID']]
        lista = [df2['COUNTRY'].unique()[0], df2['WASTE_ID'].count()]
        contagem_ww_plants.append(lista)

    contagem_ww_plants = pd.DataFrame(contagem_ww_plants, columns =['Country', 'Quantity'])
    coastline = [19924, 14500, 7000, 7491, 54716, 29751, 2450, 37653, 9330, 2389] #Reference: https://www.cia.gov/the-world-factbook/field/coastline/
    population = [341963408, 1416043270, 1409128296 ,  220051512, 281562465, 123201945, 111247248, 140820810, 130739927, 84119100]  
                                                                                  #https://www.cia.gov/theworld-factbook/field/population/
    contagem_ww_plants['Coastline (km)'] = coastline
    contagem_ww_plants['Population'] = population

    return contagem_ww_plants
#-----------------------------------------------------------------------------
def boxplot_spm_water(path3):

    water_samples = pd.read_csv('./datasets/water_samples.csv')
    spm_mediana = water_samples[['site', 'season', 'spm']].groupby(['season', 'site']).median().reset_index()
    poc_mediana = water_samples[['site', 'season', 'oc_percent']].groupby(['season', 'site']).median().reset_index()

    fig3, ax = plt.subplots(1, 2, figsize = (8,4), gridspec_kw ={'width_ratios': [7, 6]})
    fig3.tight_layout(pad = 2)

    sns.boxplot(data = water_samples, 
                x = water_samples['season'], 
                y = water_samples['spm'],  fill = True, color = 'white', linecolor = 'black',
                #hue = 'season', 
                #palette = my_palette, 
                widths = 0.5,
                ax = ax[0],
                #boxprops=dict(alpha=1),
                fliersize = 4.2,
                whis = 1.5) #Default
    
    sns.swarmplot(data = spm_mediana, 
                  x = spm_mediana['season'], 
                  y = spm_mediana['spm'], 
                  hue = spm_mediana['site'], 
                  legend = False, 
                  size = 5,
                  ax = ax[0])
    
    sns.boxplot(data = water_samples, 
                x = water_samples['season'], 
                y = water_samples['oc_percent'], fill = True, color = 'white', linecolor = 'black', 
                #hue = 'season', 
                #palette = my_palette, 
                widths = 0.5,
                ax = ax[1],
                #boxprops=dict(alpha= 1)),
                fliersize = 4.2,
                whis = 1.5) #Default
    
    sns.swarmplot(data = poc_mediana, 
                  x = poc_mediana['season'], 
                  y = poc_mediana['oc_percent'], 
                  hue = poc_mediana['site'], 
                  legend = True, 
                  size = 5,
                  ax = ax[1])

    ax[0].set_xticklabels(labels = ['Dry', 'Wet'])
    ax[0].set_ylabel('[SPM, mg/L]', fontsize=11, labelpad = 12)
    ax[0].set_xlabel('Season', fontsize=11, labelpad = 7)
    ax[0].tick_params(axis = 'x', pad = 5)
    ax[1].legend(frameon = False, bbox_to_anchor = (1.05, 1), loc = 'upper left')
    ax[1].set_xticklabels(labels = ['Dry', 'Wet'])
    ax[1].set_ylabel('POC content (%)', fontsize=11, labelpad = 12)
    ax[1].set_xlabel('Season', fontsize=11, labelpad = 7)
    st.pyplot(fig3, use_container_width = True)
#-----------------------------------------------------------------------------
path1 = 'datasets/global_wastewater_production.csv'
path2 = 'datasets/hydrowaste_database.csv'
path3 = 'datasets/water_samples.csv'

df1, df2, df3 = load_data(path1, path2)

df4 = groups_economic_classification(df1)
df5 = wastewater_plants_count(df3, df2)


#-----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;font-weight: bold'>Data visualization for the scientific manuscript:</h1>", unsafe_allow_html=True)

st.markdown("""<h2 style='text-align: center; color: black;font-weight: bold'>
             Temporal variation of sewage contamination of a tropical and highly urbanized estuary in Northeastern Brazil</h1>""",
            unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: center; color: black;'>
             Roxanny Helen de Arruda-Santosa<sup>a</sup>, Bruno Varella Motta da Costa<sup>a</sup>, Célio Freire Mariz Jr.<sup>b</sup>, Paulo Sérgio Martins de Carvalho<sup>b</sup>, Eliete Zanardi-
             Lamardo<sup>a</sup></h5>""",
            unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: left; color: black;'>
             <sup>a</sup>Departmento de Oceanografia da Universidade Federal de Pernambuco, Av. Arquitetura s/n, Recife, PE. CEP: 50740-550, Brazil.</h5>""",
            unsafe_allow_html=True)

st.markdown("""<h5 style='text-align: left; color: black;'>
             <sup>b</sup>Departmento de Zoologia da Universidade Federal de Pernambuco, Rua Prof. Nelson Chaves, s/n, Recife, PE. CEP: 50670-420, Brazil.
             </h5>""",
            unsafe_allow_html=True)

with st.container(border=True):

    st.markdown("<h3 style='text-align: center; color: black;font-weight: bold'>Introduction</h3>", unsafe_allow_html=True)

with st.container():

    st.markdown("<h3 style='text-align: center; color: black;font-weight: bold'>Figures</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([0.6, 0.4], vertical_alignment = "top", border = True)

    with col1:

        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Figure 1</h4>", unsafe_allow_html=True)
        bar_graph_countries(df2)
    
    with col2:
        
        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Legend 1</h4>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
        Wastewater production (WWp) of 10 countries based on the dataset published by Jones et al. (2020).
        WWp is the sum of collected and uncollected wastewater and it is equivalent to return flows from domestic and manufacturing sources 
        (Jones et al., 2021). Uncollected WWp is the total WWp minus collected WWp.</h6>""",
                    unsafe_allow_html=True)
        st.markdown("""<h5 style='text-align: justify; color: black;'>
        <u>References:</u></h5>""",
                    unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
        1. Jones, ER; van Vliet, MTH; Qadir, M; B, MFP. 2020. Country-level and gridded wastewater production, collection, treatment and re-use [dataset]. PANGAEA. <a href="https://doi.pangaea.de/10.1594/PANGAEA.918731">https://doi.pangaea.de/10.1594/PANGAEA.918731</a></h6>""",
                    unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
        2. Jones, ER, van Vliet, MTH, Qadir, M, Bierkens, MFP. 2021. Country-level and gridded estimates of wastewater production, collection, treatment and reuse. Earth Syst. Sci. Data 13, 237-254. <a href="https://doi.org/10.5194/essd-13-237-2021">https://doi.org/10.5194/essd-13-237-2021</a></h6>""",
                    unsafe_allow_html=True)
        
    col3, col4 = st.columns([0.6, 0.4], vertical_alignment = "top", border = True)

    with col3:
        
        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Figure 2</h4>", unsafe_allow_html=True)
        boxplot_economic_classification(df1)
        
    with col4:
        
        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Legend 2</h4>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
        Boxplot of wastewater production (WWp) of countries grouped by economic classification (Jones et al., 2020).
        </h6>""",
                    unsafe_allow_html=True)
        
    col5, col6 = st.columns([0.6, 0.4], vertical_alignment = "top", border = True)

    with col5:

        st.markdown("<h4 style='text-align: center; color: black;'>DataFrame 1</h4>", unsafe_allow_html=True)
        st.dataframe(df5)

    with col6:

        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Legend 3</h4>", unsafe_allow_html=True)

    col7, col8 = st.columns([0.6, 0.4], vertical_alignment = "top", border = True)

    with col7:

        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Figure 3</h4>", unsafe_allow_html=True)
        boxplot_spm_water(path3)

    with col8:

        st.markdown("<h4 style='text-align: center; color: black;font-weight: bold'>Legend 4</h4>", unsafe_allow_html=True)
        

    
        
    
    
        
    

        
    





