import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

import seaborn as sns

import  mpld3
import streamlit.components.v1 as components


# Title of the app

st.title('Most used language in github')

# Loading data with cache
# 1weeEsrDneR8AZ-wDeOJ2kKp74JqVXhl2

@st.cache_data
def load_data():
    #df = pd.read_csv("preprocessed_dataset.csv")
    df = pd.read_csv("https://huggingface.co/datasets/Racsgo/PreprocessedDataset/resolve/main/preprocessed_dataset_redux.csv")

    print(df.shape)
    

    df["createdAt"] = pd.to_datetime(df["createdAt"])

    return df

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')




###########################################

languages_pr = list(data["primaryLanguage"].unique())






top_n_languages = gr = (
        data
        .groupby("primaryLanguage")
        .agg(count_langs=("primaryLanguage", "count"))
        .reset_index()
)

#top_20_langs = top_n_languages.sort_values("count_langs", ascending=False).head(n = 20)["primaryLanguage"].tolist()

##############################################




#################################
# Computing barplot memory
################################

st.subheader("Quin llenguatge de programació s'utilitza en proyected de molta y poca memòria?")

boxplot_load_state = st.text('Loading Barplot...')


# Divideix dades per memoria

def classify_mem(m):
    mb = m/1000
    if mb < 50:
        return "Menor a 50 mb"
    
    if mb <= 500:
        return "Entre 50 y 500 mb"
    
    if mb <= 1000:
        return "Entre 500 y 1 gb"
    
    if mb > 1000:
        return "Més de 1 gb"

data["memory_classification"] = data["diskUsageKb"].apply(classify_mem)


data_gr = data.groupby(["primaryLanguage","memory_classification"]).agg(count = ("memory_classification", "count"))

memory_group = (
    data
    .groupby(["primaryLanguage", "memory_classification"])
    .agg(count=("memory_classification", "count"))
    .reset_index()
)


def Create_Barplots_Memory(clasific, title, colour = "blue"):
    mem = memory_group[memory_group["memory_classification"] == clasific].sort_values("count", ascending=False)

    #memory_50 = Create_Barplots_Memory("Menor a 50 mb")

    fig_50 = px.bar(mem.head(n=20).sort_values("count", ascending=True), x = "count", y="primaryLanguage",
                    color_discrete_sequence=[colour])

    fig_50.update_layout(
        title=dict(
            text=title
        ),
        
        xaxis=dict(
            title=dict(
                text="Número de Repositoris"
            )
        ),

        yaxis=dict(
            title=dict(
                text="Llenguatge de programació"
            )
        ),
        xaxis_range=[0,21000],
        showlegend=False)
    
    return fig_50


tab1, tab2, tab3, tab4 = st.tabs(["Menor a 50 mb", "Entre 50 y 500 mb","Entre 500 y 1 gb", "Més de 1 gb"])


with tab1:

    st.plotly_chart(Create_Barplots_Memory(
        "Menor a 50 mb",
        "Els 20 llenguatges de programació amb més repositoris de menys de 50 Megabytes", "blue"
                                           ))
with tab2:

    st.plotly_chart(Create_Barplots_Memory(
        "Entre 50 y 500 mb",
        "Els 20 llenguatges de programació amb més repositoris d'entre 50 y 500 Megabytes", "green"
                                           ))
with tab3:

    st.plotly_chart(Create_Barplots_Memory(
        "Entre 500 y 1 gb",
        "Els 20 llenguatges de programació amb més repositoris d'entre 500 Megabytes y 1 Gigabyte", "orange"
                                           ))
with tab4:

    st.plotly_chart(Create_Barplots_Memory(
        "Més de 1 gb",
        "Els 20 llenguatges de programació amb més repositoris de més d'1 Gigabyte", "pink"
                                           ))

boxplot_load_state.text('Loading Barplot... Done!')


################################
## Counts
################################

st.subheader("Quin llenguatge de programació té més forks, issues, watchers, stars, i pull requests?")

Counts_load_state = st.text('Loading Barplots...')

#data_forks = data.groupby("primaryLanguage").agg(fork_count=("forks", "count"))



def graph_git_metrics(metric, metric_name, color="blue"):

    mmm = "sum"

    met = "Quantitat"
    met2 = "Número"

    if metric == "stars":
        mmm = "mean"
        met = "Mitjana"
        met2 = "Mitjana"


    data_forks = (
        data
        .groupby("primaryLanguage")
        .agg(sum_op=(metric, mmm))
        .reset_index()
    )

    d_forks = data_forks.sort_values("sum_op", ascending=False)


    fig = px.bar(d_forks.head(n=20).sort_values("sum_op", ascending=True), y="primaryLanguage", x="sum_op", color_discrete_sequence=[color])



    fig.update_layout(
            title=dict(
                text=f"{met} de {metric_name}"
            ),
            
            xaxis=dict(
                title=dict(
                    text=f"{met2} de {metric_name}"
                )
            ),

            yaxis=dict(
                title=dict(
                    text="Llenguatge de programació"
                )
            ),

            showlegend=False)

    return st.plotly_chart(fig)


tab5, tab6, tab7, tab8, tab9 = st.tabs(["Froks", "Watchers", "Stars", "Issues", "Pull Requests"])


with tab5:

    graph_git_metrics("forks", "Forks", "blue")
    
with tab6:

   graph_git_metrics("watchers", "Watchers", "green")

with tab7:

    graph_git_metrics("stars", "Stars", "orange")

with tab8:

    graph_git_metrics("issues", "Issues", "pink")

with tab9:

    graph_git_metrics("pullRequests", "Pull Requests", "purple")


Counts_load_state.text("Loading Barplots... Done!")



####################################
## License
####################################


st.subheader("Quin és el llenguatge de programació més utilitzat segons el tipus de llicència?")

# Crear grafic

def graph_counts(metric, metric_name):
    data_forks = (
        data[data["license"] == metric]
        .groupby("primaryLanguage")
        .agg(counts=("license", "count"))
        .reset_index()
    )

    d_forks = data_forks.sort_values("counts", ascending=False)


    fig = px.bar(d_forks.head(n=20).sort_values("counts", ascending=True), y="primaryLanguage", x="counts", color_discrete_sequence=["pink"])


    fig.update_layout(
            title=dict(
                text=f"Quantitat de {metric_name}"
            ),
            
            xaxis=dict(
                title=dict(
                    text=f"Número de {metric_name}"
                )
            ),

            yaxis=dict(
                title=dict(
                    text="Llenguatge de programació"
                )
            ),
            xaxis_range=[0,11000],
            showlegend=False)

    return st.plotly_chart(fig)


# Per a cada llicencia fer un dictionari de tabs

licenseTypes = list(data[data["license"].notna()]["license"].unique())

options = st.selectbox("Tria un tipus de llicència", licenseTypes, index=2)

graph_counts(options, options)



###################
## Temes
###################

topics_df = pd.read_csv("topics.csv")

def graph_counts_topic(metric, metric_name):

    t = topics_df[topics_df["primaryLanguage"] == metric]

    d_forks = t.sort_values("count", ascending=False)


    fig = px.bar(d_forks.head(n=3), y="topics_array", x="count", color="topics_array", color_discrete_sequence=["green"])


    fig.update_layout(
            title=dict(
                text=f"Quantitat de {metric_name}"
            ),
            
            xaxis=dict(
                title=dict(
                    text=f"Número de {metric_name}"
                )
            ),

            yaxis=dict(
                title=dict(
                    text="Llenguatge de programació"
                )
            ),

            xaxis_range=[0,70000],

            showlegend=False)

    return st.plotly_chart(fig)

st.subheader("Quins són els temes més populars per a cada llenguatge de programació?")

options_lang = st.selectbox("Tria un llenguatge", languages_pr)

graph_counts_topic(options_lang, options_lang)

# Seleccionant llenguatges més populars per millorar visibilitat

top_10_langs = top_n_languages.sort_values("count_langs", ascending=False).head(n = 10)["primaryLanguage"].tolist()

fig = px.bar(topics_df[topics_df["primaryLanguage"].isin(top_10_langs)], x = "primaryLanguage", y = "count", color="topics_array", barmode="stack")


fig.update_layout(
            title=dict(
                text="Els temes més freqüents al top 10 llenguatges més utilitzats"
            ),
            
            xaxis=dict(
                title=dict(
                    text=f"Llenguatge"
                )
            ),

            yaxis=dict(
                title=dict(
                    text="Quantitat de repositoris amb un tema"
                )
            ),

            showlegend=True)


st.plotly_chart(fig)


########################################################
# Grafics temporals
########################################################

st.subheader("Evolucó temporal de les 10 llengües més presents al dataset")

data["Year"] = data["createdAt"].dt.year


popular_data_langs = data[data["primaryLanguage"].isin(top_10_langs)]

def temp_evolution(metric, title):

    gr = (
        popular_data_langs
        .groupby(["Year", "primaryLanguage"])
        .agg(average=(metric, "mean"))
        .reset_index()
    )

    fig = px.line(gr, x = "Year", y="average", color="primaryLanguage", color_discrete_sequence=px.colors.qualitative.Set2)

    fig.update_layout(
            title=dict(
                text=f"Evolució de {title} a través dels anys."
            ),
            
            yaxis=dict(
                title=dict(
                    text=f"Mitjana de {title}"
                )
            ),

            xaxis=dict(
                title=dict(
                    text="Anys"
                )
            ),
            showlegend=True)

    return st.plotly_chart(fig)


tab10, tab11, tab12, tab13, tab14, tab15 = st.tabs(["Disk Usage Kb", "Forks", "Watchers", "Stars", "Issues", "Pull Requests"])


with tab10:

    temp_evolution("diskUsageKb", "l'espai en Kylobytes")
    
with tab11:

   temp_evolution("forks", "la quantitat de Forks")

with tab12:

    temp_evolution("watchers", "la quantitat de watchers")

with tab13:

    temp_evolution("stars", "Stars")

with tab14:

    temp_evolution("issues", "la quantitat d'issues")

with tab15:

    temp_evolution("pullRequests", "la quantitat de pull Requests")

