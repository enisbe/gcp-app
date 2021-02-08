!pip install quandl

import quandl
import datetime
from google.cloud import bigquery
import pandas
import pytz
client = bigquery.Client()


quandl.ApiConfig.api_key = 'Ru9ai33t5ouuaETzyhZC'

regions = quandl.get_table('ZILLOW/REGIONS')
 
regions_city = regions[regions['region_type']=='city'] ['region_id'].tolist()
regions_city[0]

ZSFH = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH',  region_id=regions_city[10:20])


ZSFH = ZSFH.set_index('date')
job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField("indicator_id", bigquery.enums.SqlTypeNames.STRING),
            # Indexes are written if included in the schema by name.
#             bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
        ],
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        #write_disposition="WRITE_TRUNCATE",
    )
table_id = "my-project-434-301711.zillow_data.ZSFH"
job = client.load_table_from_dataframe(
        ZSFH, table_id, job_config=job_config
    )  # Make an API request.
job.result()  # Wait for the job to complete.


table = client.get_table(table_id)  # Make an API request.
print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    # [END bigquery_load_table_dataframe]