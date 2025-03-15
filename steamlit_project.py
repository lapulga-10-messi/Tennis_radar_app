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

    st.image("data:image/jpeg;base64,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")

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

