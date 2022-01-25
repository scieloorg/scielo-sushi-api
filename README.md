SciELO SUSHI API

## Setting up Database
- Create the procedures indicated in api/static/sql/procedures.sql

## Instalation and Running
_Build_
```shell script
docker build . --tag scieloorg/scielo-sushi-api
```

_Run_
```
docker run -d \
    -p 6543:6543 \
    --name scielo-sushi-api \
    --env STR_CONNECTION="mysql://user:pass@localhost:port/database" \
    --env APPLICATION_URL="http://127.0.0.1:6543" \
    scieloorg/scielo-sushi-api \
    pserve /app/config.ini
```

_Environment variables_
| Variable | Description |
|-------- | ----------- |
| `APPLICATION_URL` | Application address |
| `STR_CONNECTION` | Database string connection |


## Routes

URL | Description |
|----|----|
| `/status` or `/` | Current status of the SciELO SUSHI API service. |
| `/reports` | Returns a list of reports supported by the SciELO SUSHI API service. |
| `/members` | Returns the list of members. |
| `/reports/cr_j1` | Collection-level usage summarized by Metric_Type. |
| `/reports/ir_a1` | Item Reports provide a summary of activity related to content at the item level and provide a means of evaluating the impact an item has for an institution’s patrons. |
| `/reports/tr_j1` | Returns COUNTER 'Journal Requests (Excluding OA_Gold)' [TR_J1], a Standard View of Title Master Report. Reports on usage of non-Gold Open Access journal content as “Total_Item_Requests” and “Unique_Item_Requests”. |
| `/reports/tr_j4` | This resource returns "Journal Requests by YOP (Excluding OA_Gold)" [TR_J4], a Standard View of Title Master Report. Breaks down the usage of non-Gold Open Access journal content by year of publication (YOP) providing counts for the metric types "Total_Item_Requests" and "Unique_Item_Requests". |


### Parameters
| Name | Reports | Description |
|------|---------|-------------|
| `api` | `tr_j1`, and `cr_j1` | Version of the API. It could be `api=v2` for reports `tr_j1` and `cr_j1` or `v1` for all the reports. |
| `begin_date` | `all` | Usage start date in the form o YYYY-MM or YYYY-MM-DD. |
| `collection`  | `all` | Collection. |
| `fmt` | `all` | Output format: `tsv` or `json` (default). |
| `end_date` | `all` | Usage end date in the form o YYYY-MM or YYYY-MM-DD. |
| `granularity` | `all` | Optional Report Attribute. Include this parameter to allow usage to be retrieved with a granularity of 'month' (default if omitted) or 'totals'. |
| `issn` | `ir_a1`, `tr_j1`, and `tr_j4` | ISSN of a Journal. |
| `pid` | `ir_a1` | PID of an article. |