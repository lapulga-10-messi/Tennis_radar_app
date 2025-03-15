pip install mysql.connector
pip install pandas
pip install streamlit


import mysql.connector

def fetch_data(sql_query):
    leo_streamlit = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vikas@1997',
            auth_plugin='mysql_native_password')

    cursor = leo_streamlit.cursor()

    cursor.execute("USE project_guvi")

    cursor.execute(sql_query)

    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]

    cursor.close()
    leo_streamlit.close()

    df = pd.DataFrame(rows, columns=columns)
    return df

import streamlit as st
import pandas as pd

st.title("Tennis Data Analysis App")

st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a Page", ["Home", "Competitions", "Venues", "Doubles Competitor Rankings"])

# home
if options == "Home":
    st.header("Homepage Dashboard")
    st.write("Welcome to the Tennis Data Analysis App!")

    #search name#
    st.subheader("Search Player Data")
    search_name = st.text_input("Enter player name:")

    if search_name:

        search_terms = search_name.split()
        where_clause = " OR ".join([f"LOWER(name) LIKE LOWER('%{term}%')" for term in search_terms])
        query = f"""
                select  *
                from (
                select 
                        comp_rank.`rank` as `Rank`,
                        comp_rank.points as Points,
                        comp_table.`name` as `Name`,
                        comp_table.country as Country
                from  competitors_table as comp_table
                inner join  competitor_rankings_table as comp_rank
                on   comp_table.competitor_id = comp_rank.competitor_id
                )t WHERE {where_clause};
                """
        player_data = fetch_data(query)

        if not player_data.empty:
            st.write(f"Search results for '{search_name}':")
            st.dataframe(player_data)
        else:
            st.warning(f"No player found with the name '{search_name}'.")

    st.image("C:/Users/asus/Desktop/py/python guvi/view-tennis-equipment.jpg")

    st.subheader("Summary Statistics")
    total_competitors = fetch_data("select  COUNT(competitor_id) from competitors_table;").iloc[0, 0]
    total_countries = fetch_data("select  COUNT(DISTINCT country) from competitors_table;").iloc[0, 0]
    highest_points = fetch_data("select  MAX(points) from competitor_rankings_table;").iloc[0, 0]

    st.metric("Total Competitors", total_competitors)
    st.metric("Total Countries Represented", total_countries)
    st.metric("Highest Points Scored by a Competitor", highest_points)

    # rank filter#
    st.sidebar.subheader("Filter by Rank")
    min_rank, max_rank = st.sidebar.slider(
        "Select range:",
        min_value=1, max_value=500, value=(1, 500)
    )

    query = f"""
      select *
      from(
      select 
                comp_rank.`rank` as `Rank`,
                comp_rank.points as Points,
                comp_table.`name` as `Name`,
                comp_table.country as Country
      from  competitors_table as comp_table
      inner join  competitor_rankings_table as comp_rank
      on   comp_table.competitor_id = comp_rank.competitor_id         
      )t WHERE `Rank` BETWEEN {min_rank} AND {max_rank}
      ORDER BY `Rank`
      """
    rankings_data = fetch_data(query)

    if not rankings_data.empty:
        st.write(f"Players ranked between {min_rank} and {max_rank}:")
        st.dataframe(rankings_data)
    else:
        st.warning(f"No players found in the rank range {min_rank} to {max_rank}.")


elif options == "Competitions":
    Competitions_Analysis_options = st.sidebar.radio("Competitions", ["All Competitions with Category Names", "Number of Competitions per Category","All doubles competitions","All competitions of category : ITF Men","Parent competitions and their sub-competitions","Distribution of competition types by category","All competitions with no parent competitions"])
    st.header("Competitions Analysis")
    if Competitions_Analysis_options == "All Competitions with Category Names":
        # query 1
        st.subheader("All Competitions with Category Names")
        competitions_query = """
        select *
        from(
        select
            com.comp_name as `Competition Name`,
            cat.cat_name as `Category Name`
        from competitions_table as com
        join category_table as cat
        ON com.cat_id = cat.cat_id)t;
        """
        competitions_data = fetch_data(competitions_query)
        st.dataframe(competitions_data)

    elif Competitions_Analysis_options == "Number of Competitions per Category":
        # query 2
        st.subheader("Number of Competitions per Category")
        competitions_query = """
        select distinct
            `Category Name`,
            count(*) over(partition by `Category Name`) `No of Competitions in each category`  
        from 
        (select
           com.comp_name as competition_name,
           cat.cat_name as `Category Name`
         from competitions_table as com
         join category_table as cat
         on com.cat_id = cat.cat_id 
        ) t
        """
        competitions_count_data = fetch_data(competitions_query)
        st.dataframe(competitions_count_data)

    elif Competitions_Analysis_options == "All doubles competitions":
        # query 3
        st.subheader("All doubles competitions")
        competitions_query = """
        select 
            comp_name as `Doubles Competitions`
        from competitions_table
        where comp_type = 'doubles';
        """
        doubles_competitions_data = fetch_data(competitions_query)
        st.dataframe(doubles_competitions_data)

    elif Competitions_Analysis_options == "All competitions of category : ITF Men":
        # query 4
        st.subheader("All competitions of category : ITF Men")
        competitions_query = """
        select `Competition Name`
        from
        (select
            com.comp_name as `Competition Name`,
            cat.cat_name as `Category Name`
        from competitions_table as com		
        join category_table as cat		
        ON com.cat_id = cat.cat_id	
        )t	where `Category Name` = 'ITF Men'

        """
        ITF_category_data = fetch_data(competitions_query)
        st.dataframe(ITF_category_data)

    elif Competitions_Analysis_options == "Parent competitions and their sub-competitions":
        # query 5
        st.subheader("Parent competitions and their sub-competitions")
        competitions_query = """
        select
            parent.comp_name AS `Parent Competition`,
            child.comp_name AS `Sub-Competition`
        from competitions_table AS parent    
        join competitions_table AS child
        on parent.comp_id = child.comp_parent_id;

        """
        Parent_child_data = fetch_data(competitions_query)
        st.dataframe(Parent_child_data)

    elif Competitions_Analysis_options == "Distribution of competition types by category":
        # query 6
        st.subheader("Distribution of competition types by category")
        competitions_query = """
        select distinct
            cat.cat_name as `Category Name`, 
            com.comp_type as `Competition type`, 
            count(*) over(partition by cat.cat_name, com.comp_type ) as` Number of competitions`
        from 
            competitions_table as com
        inner join 
            category_table as cat
        on
            com.cat_id = cat.cat_id

        """
        distribution_competition_category_data = fetch_data(competitions_query)
        st.dataframe(distribution_competition_category_data)

    elif Competitions_Analysis_options == "All competitions with no parent competitions":
        # query 7
        st.subheader("All competitions with no parent competitions")
        competitions_query = """
        select 
          comp_name as `Competition Name`
        from competitions_table
        where comp_parent_id ='0';

        """
        no_Parent_data = fetch_data(competitions_query)
        st.dataframe(no_Parent_data)


elif options == "Venues":
    Venues_Analysis_options = st.sidebar.radio("Venues", ["All venues along with their associated complex name","Number of venues in each complex","Number of venues in a specific country:chile","All venues and their timezones","Complexes with more than one venue","Venues grouped by country","All venues for a specific complex: Nacional"])
    st.header("Venues Analysis")
    if Venues_Analysis_options == "All venues along with their associated complex name":
        # query 1
        st.subheader("All venues along with their associated complex name")
        venues_query = """
                select
                    ven.venue_name AS `Venue Name`, 
                    com.complex_name AS `Complex Name`
                from venues_table AS ven
                join complexes_table AS com
                on ven.complex_id = com.complex_id
                order by ven.venue_name DESC;
        """
        venues_complex_data = fetch_data(venues_query)
        st.dataframe(venues_complex_data)

    elif Venues_Analysis_options == "Number of venues in each complex":
        # query 2
        st.subheader("Number of venues in each complex")
        venues_query = """
        select distinct 
            Complex,
            count(*)over(partition by Complex ) as `Number of venues`
        from(
        select 
            ven.venue_name as Venue, 
            com.complex_name as Complex
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id
        )t       
        """
        no_venues_data = fetch_data(venues_query)
        st.dataframe(no_venues_data)

    elif Venues_Analysis_options == "Number of venues in a specific country:chile":
        # query 3
        st.subheader("No of venues in a specific country:chile")
        venues_query = """
        select 
            Country,
            Venue,
            Complex,
            count(*)over(partition by Country) `Number of venues`
        from(
        select 
            ven.country_name as Country,
            ven.venue_name as Venue, 
            com.complex_name as Complex
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id
        )t where Country = 'chile';
        """
        chile_venues_data = fetch_data(venues_query)
        st.dataframe(chile_venues_data)

    elif Venues_Analysis_options == "All venues and their timezones":
        # query 4
        st.subheader("All venues and their timezones")
        venues_query = """
        select 
            ven.venue_name as Venue, 
            com.complex_name as Complex,
            ven.timezone as Timezone,
            ven.country_name as Country
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id
        order by Timezone;
        """
        timezones_venues_data = fetch_data(venues_query)
        st.dataframe(timezones_venues_data)

    elif Venues_Analysis_options == "Complexes with more than one venue":
        # query 5
        st.subheader("Complexes with more than one venue")
        venues_query = """
        select
           Complex,
           `Number of venues`
        from(
        select distinct 
            Complex,
            count(*)over(partition by complex ) as `Number of venues`
        from(
        select 
            ven.venue_name as venue, 
            com.complex_name as Complex
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id
        )t
        )t1
        where `Number of venues` > 1 
        order by `Number of venues`
        """
        more_than_one_complex_data = fetch_data(venues_query)
        st.dataframe(more_than_one_complex_data)


    elif Venues_Analysis_options == "Venues grouped by country":
        # query 6
        st.subheader("Venues grouped by country")
        venues_query = """
        select 
             Country ,
             Venue,
             Complex,
             count(*)over(partition by Country) `Number of venues in this country`
        from (
        select 
            ven.venue_name as Venue, 
            com.complex_name as Complex,
            ven.country_name as Country
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id)t
        """
        country_venues_data = fetch_data(venues_query)
        st.dataframe(country_venues_data)

    elif Venues_Analysis_options == "All venues for a specific complex: Nacional":
        # query 7
        st.subheader("All venues for a specific complex: Nacional")
        venues_query = """
        select  
            Complex,
            venue
        from(
        select 
            ven.venue_name as Venue, 
            com.complex_name as Complex
        from venues_table as ven
        join complexes_table as com
        on ven.complex_id = com.complex_id
        )t
        where complex ='Nacional'  
            """
        Nacional_venues_data = fetch_data(venues_query)
        st.dataframe(Nacional_venues_data)

elif options == "Doubles Competitor Rankings":
    doubles_Competitor_Rankings = st.sidebar.radio("Doubles Competitor Rankings", ["All competitors with their rank and points","Competitors ranked in the top 5","Competitors with no rank movement","Total points of competitors from a specific country : Croatia","Number of competitors per country","Competitors with the highest points in the current week"])
    st.header(" Doubles Competitor Rankings Analysis")

    if doubles_Competitor_Rankings == "All competitors with their rank and points":
        # query 1
        st.subheader("All competitors with their rank and points")
        doubles_query = """
        select 
                comp_rank.`rank` as `Rank`,
                comp_table.`name` as `Name`,
                comp_rank.points as Points
        from  competitors_table as comp_table
        inner join  competitor_rankings_table as comp_rank
        on   comp_table.competitor_id = comp_rank.competitor_id;              
        """
        rank_points_data = fetch_data(doubles_query)
        st.dataframe(rank_points_data)


    if doubles_Competitor_Rankings == "Competitors ranked in the top 5":
        # query 2
        st.subheader("Competitors ranked in the top 5")
        doubles_query = """
        select 
                com_rank as` Rank`,
                com_name as `Name`
        from(
        select 
                comp_rank.`rank` as com_rank,
                comp_table.`name` as com_name
         from  competitors_table as comp_table
        inner join  competitor_rankings_table as comp_rank
        on   comp_table.competitor_id = comp_rank.competitor_id
        )t 
        where com_rank < '6';             
        """
        top_5_data = fetch_data(doubles_query)
        st.dataframe(top_5_data)

    if doubles_Competitor_Rankings == "Competitors with no rank movement":
        # query 3
        st.subheader("Competitors with no rank movement")
        st.write("ordered by rank of the competitor")
        doubles_query = """
        select 
                com_name as `Name`
        from(
        select 
                comp_rank.movement as com_movement,
                comp_table.`name` as com_name,
                comp_rank.`rank` as com_rank
        from  competitors_table as comp_table
        inner join  competitor_rankings_table as comp_rank
        on   comp_table.competitor_id = comp_rank.competitor_id
        )t 
        where com_movement = '0'
        order by com_rank;
        """
        no_rank_movement_data = fetch_data(doubles_query)
        st.dataframe(no_rank_movement_data)

    if doubles_Competitor_Rankings == "Total points of competitors from a specific country : Croatia":
        # query 4
        st.subheader("Total points of competitors from a specific country : Croatia")
        st.write("ordered by rank of the competitor")
        doubles_query = """
        select 
                `Name`,
                `Total points` ,
                 `Rank`
        from(
        select 
                comp_table.`name` as `Name`,
                comp_rank.points as `Total points`,
                comp_table.country as Country,
                comp_rank.`rank` as `Rank`
        from  competitors_table as comp_table
        join  competitor_rankings_table as comp_rank
        on    comp_table.competitor_id = comp_rank.competitor_id
        )t 
        where Country = 'croatia'
        order by `Rank`;
        """
        croatia_data = fetch_data(doubles_query)
        st.dataframe(croatia_data)

    if doubles_Competitor_Rankings == "Number of competitors per country":
        # query 5
        st.subheader("Number of competitors per country")
        doubles_query = """
        select distinct
             country as Country,
             count(*)over(partition by country order by country) `Number of competitors`
        from 
             competitors_table;
        """
        no_of_competitors_data = fetch_data(doubles_query)
        st.dataframe(no_of_competitors_data)

    if doubles_Competitor_Rankings == "Competitors with the highest points in the current week":
        # query 6
        st.subheader("Competitors with the highest points in the current week")
        st.write("Displaying Competitors from both ATP and WTA")
        doubles_query = """
        select *
        from
        (select 
                comp_rank.`rank` as `Rank` ,
                comp_table.`name` as `Name`,
                comp_rank.points as `Total Points`,
                comp_table.country as Country
        from  competitors_table as comp_table
        join  competitor_rankings_table as comp_rank
        on    comp_table.competitor_id = comp_rank.competitor_id
        )t  where `Rank`= 1 ;
        """
        highest_data = fetch_data(doubles_query)
        st.dataframe(highest_data)

