SciELO SUSHI API

## Setting up Database
- Create the procedures indicated in api/static/sql/procedures.sql

## Instalation and Running
_Build_
```shell script
docker build --tag scielo-sushi-api:latest .
```

_Run_
```
docker run -d -p 6543:6543 --name scielo-sushi-api --env MARIADB_STRING_CONNECTION="mysql://user:pass@localhost:port/database" --env APPLICATION_URL="http://127.0.0.1:6543" scielo-sushi-api
```

## Routes

URL | Description |
|----|----|
| `/status` or `/` | Current status of the SciELO SUSHI API service. |
| `/reports` | Returns a list of reports supported by the SciELO SUSHI API service. |
| `/members` | Returns the list of members. |
| `/reports/tr_j1` | Returns COUNTER 'Journal Requests (Excluding OA_Gold)' [TR_J1], a Standard View of Title Master Report. Reports on usage of non-Gold Open Access journal content as “Total_Item_Requests” and “Unique_Item_Requests”. |
| `/reports/tr_j4` | This resource returns "Journal Requests by YOP (Excluding OA_Gold)" [TR_J4], a Standard View of Title Master Report. Breaks down the usage of non-Gold Open Access journal content by year of publication (YOP) providing counts for the metric types "Total_Item_Requests" and "Unique_Item_Requests". |


### Parameters (for `tr` reports only)
| Name | Description | 
|------|-------------|
| `begin_date` | Usage start date in the form o YYYY-MM or YYYY-MM-DD. |
| `end_date` | Usage end date in the form o YYYY-MM or YYYY-MM-DD. |
| `granularity` | Optional Report Attribute. Include this parameter to allow usage to be retrieved with a granularity of 'month' (default if omitted) or 'totals'. |
| `issn` | ISSN of a Journal. | 
