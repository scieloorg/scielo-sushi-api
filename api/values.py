COLLECTION_ACRONYM_TO_COLLECTION_NAME = {
    'arg': 'Argentina',
    'chl': 'Chile',
    'col': 'Colômbia',
    'cub': 'Cuba',
    'esp': 'Espanha',
    'mex': 'México',
    'prt': 'Portugal',
    'boo': 'Livros',
    'scl': 'Brasil',
    'ssp': 'Saúde Pública',
    'sss': 'Social Sciences',
    'sza': 'África do Sul',
    'ven': 'Venezuela',
    'bio': 'Biodiversity Heritage Library',
    'bol': 'Bolívia',
    'cri': 'Costa Rica',
    'per': 'Peru',
    'pro': 'Proceedings',
    'pry': 'Paraguai',
    'ury': 'Uruguai',
    'wid': 'Índias Ocidentais',
    'cci': 'ComCiência',
    'cic': 'Ciência e Cultura',
    'inv': 'Conhecimento & Inovação',
    'pef': 'Pesquisa FAPESP',
    'edc': 'Educa',
    'ppg': 'Portal de Periódicos Eletrônicos em Geociências',
    'psi': 'Periódicos Eletrônicos em Psicologia',
    'rve': 'Revista de Enfermagem',
    'rvo': 'RevOdonto',
    'ses': 'Portal de Revistas - SES',
    'ecu': 'Equador',
    'rvt': 'RevTur',
    'pre': 'Preprints',
    'dat': 'Data',
    'nbr': 'SciELO Brasil'
}

URI_REQUIRED_PARAMETERS = set(['begin_date', 'customer', 'end_date',])
URI_OPTIONAL_PARAMETERS = set(['api', 'collection', 'customer', 'fmt', 'granularity', 'issn', 'pid',])
URI_SUPPORTED_PARAMETERS = URI_REQUIRED_PARAMETERS.union(URI_OPTIONAL_PARAMETERS)

REGEX_DATE_FORMAT = r'\d{4}\-\d{2}($|\-\d{2}$)'
REGEX_ISSN = r'[0-9]{4}-[0-9]{3}[0-9xX]$'

DB_CALL_TR_J1_TOTALS = 'CALL TR_J1_TOTALS("%s", "%s", "%s")'
DB_CALL_TR_J1_MONTHLY = 'CALL TR_J1_MONTHLY("%s", "%s", "%s")'

DB_CALL_TR_J1_JOURNAL_TOTALS = 'CALL TR_J1_JOURNAL_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_TR_J1_JOURNAL_MONTHLY = 'CALL TR_J1_JOURNAL_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_TR_J4_TOTALS = 'CALL TR_J4_TOTALS("%s", "%s", "%s")'
DB_CALL_TR_J4_MONTHLY = 'CALL TR_J4_MONTHLY("%s", "%s", "%s")'

DB_CALL_TR_J4_JOURNAL_TOTALS = 'CALL TR_J4_JOURNAL_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_TR_J4_JOURNAL_MONTHLY = 'CALL TR_J4_JOURNAL_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_IR_A1_ARTICLE_TOTALS = 'CALL IR_A1_ARTICLE_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_IR_A1_ARTICLE_MONTHLY = 'CALL IR_A1_ARTICLE_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_IR_A1_JOURNAL_TOTALS = 'CALL IR_A1_JOURNAL_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_IR_A1_JOURNAL_MONTHLY = 'CALL IR_A1_JOURNAL_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_IR_A1_TOTALS = 'CALL IR_A1_TOTALS("%s", "%s", "%s")'
DB_CALL_IR_A1_MONTHLY = 'CALL IR_A1_MONTHLY("%s", "%s", "%s")'

DB_CALL_V2_TR_J1_JOURNAL_TOTALS = 'CALL V2_TR_J1_JOURNAL_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_V2_TR_J1_JOURNAL_MONTHLY = 'CALL V2_TR_J1_JOURNAL_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_V2_LR_J1_JOURNAL_TOTALS = 'CALL V2_LR_J1_JOURNAL_TOTALS("%s", "%s", "%s", "%s", "%s")'
DB_CALL_V2_LR_J1_JOURNAL_MONTHLY = 'CALL V2_LR_J1_JOURNAL_MONTHLY("%s", "%s", "%s", "%s", "%s")'

DB_CALL_V2_TR_J1_TOTALS = 'CALL V2_TR_J1_TOTALS("%s", "%s", "%s")'
DB_CALL_V2_TR_J1_MONTHLY = 'CALL V2_TR_J1_MONTHLY("%s", "%s", "%s")'

DB_CALL_V2_LR_J1_TOTALS = 'CALL V2_LR_J1_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_V2_LR_J1_MONTHLY = 'CALL V2_LR_J1_MONTHLY("%s", "%s", "%s", "%s")'

DB_CALL_V2_CR_J1_TOTALS = 'CALL V2_CR_J1_TOTALS("%s", "%s", "%s", "%s")'
DB_CALL_V2_CR_J1_MONTHLY = 'CALL V2_CR_J1_MONTHLY("%s", "%s", "%s", "%s")'

REPORT_ID_TO_COLUMN_STATUS = {
    'cr_j1': 'status_sushi_journal_metric',
    'ir_a1': 'status_sushi_article_metric',
    'tr_j1': 'status_sushi_journal_metric',
    'tr_j4': 'status_sushi_journal_yop_metric',
    'lr_j1': 'status_aggr_journal_language_year_month_metric',
}

GRANULARITY_MODE_REPORT_TO_PROCEDURE_AND_PARAMETERS = {
    'totals': {
        'pid': {
            'tr_j1': ('', []),
            'tr_j4': ('', []),
            'ir_a1': (DB_CALL_IR_A1_ARTICLE_TOTALS, ['begin_date', 'end_date', 'pid', 'collection'])
        },
        'issn': {
            'tr_j1': (DB_CALL_TR_J1_JOURNAL_TOTALS, ['begin_date', 'end_date', 'issn', 'collection']),
            'tr_j4': (DB_CALL_TR_J4_JOURNAL_TOTALS, ['begin_date', 'end_date', 'issn', 'collection']),
            'ir_a1': (DB_CALL_IR_A1_JOURNAL_TOTALS, ['begin_date', 'end_date', 'issn', 'collection'])
        },
        'global': {
            'tr_j1': (DB_CALL_TR_J1_TOTALS, ['begin_date', 'end_date', 'collection']),
            'tr_j4': (DB_CALL_TR_J4_TOTALS, ['begin_date', 'end_date', 'collection']),
            'ir_a1': (DB_CALL_IR_A1_TOTALS, ['begin_date', 'end_date', 'collection'])
        }
    },
    'monthly': {
        'pid': {
            'tr_j1': ('', []),
            'tr_j4': ('', []),
            'ir_a1': (DB_CALL_IR_A1_ARTICLE_MONTHLY, ['begin_date', 'end_date', 'pid', 'collection'])
        },
        'issn': {
            'tr_j1': (DB_CALL_TR_J1_JOURNAL_MONTHLY, ['begin_date', 'end_date', 'issn', 'collection']),
            'tr_j4': (DB_CALL_TR_J4_JOURNAL_MONTHLY, ['begin_date', 'end_date', 'issn', 'collection']),
            'ir_a1': (DB_CALL_IR_A1_JOURNAL_MONTHLY, ['begin_date', 'end_date', 'issn', 'collection'])
        },
        'global': {
            'tr_j1': (DB_CALL_TR_J1_MONTHLY, ['begin_date', 'end_date', 'collection']),
            'tr_j4': (DB_CALL_TR_J4_MONTHLY, ['begin_date', 'end_date', 'collection']),
            'ir_a1': (DB_CALL_IR_A1_MONTHLY, ['begin_date', 'end_date', 'collection'])
        }
    }
}

V2_GRANULARITY_MODE_REPORT_TO_PROCEDURE_AND_PARAMETERS = {
    'totals': {
        'issn': {
            'lr_j1': (DB_CALL_V2_LR_J1_JOURNAL_TOTALS, ['begin_date', 'end_date', 'issn', 'collection', 'collection_extra']),
            'tr_j1': (DB_CALL_V2_TR_J1_JOURNAL_TOTALS, ['begin_date', 'end_date', 'issn', 'collection']),
        },
        'global': {
            'cr_j1': (DB_CALL_V2_CR_J1_TOTALS, ['begin_date', 'end_date', 'collection', 'collection_extra']),
            'lr_j1': (DB_CALL_V2_LR_J1_TOTALS, ['begin_date', 'end_date', 'collection', 'collection_extra']),
            'tr_j1': (DB_CALL_V2_TR_J1_TOTALS, ['begin_date', 'end_date', 'collection']),
        }
    },
    'monthly': {
        'issn': {
            'lr_j1': (DB_CALL_V2_LR_J1_JOURNAL_MONTHLY, ['begin_date', 'end_date', 'issn', 'collection', 'collection_extra']),
            'tr_j1': (DB_CALL_V2_TR_J1_JOURNAL_MONTHLY, ['begin_date', 'end_date', 'issn', 'collection']),

        },
        'global': {
            'cr_j1': (DB_CALL_V2_CR_J1_MONTHLY, ['begin_date', 'end_date', 'collection', 'collection_extra']),
            'lr_j1': (DB_CALL_V2_LR_J1_MONTHLY, ['begin_date', 'end_date', 'collection', 'collection_extra']),
            'tr_j1': (DB_CALL_V2_TR_J1_MONTHLY, ['begin_date', 'end_date', 'collection']),
        }
    }
}

TSV_REPORT_DEFAULT_HEADERS = [
    'Report_Name',
    'Report_ID',
    'Release',
    'Institution_Name',
    'Institution_ID',
    'Metric_Types',
    'Report_Filters',
    'Report_Attributes',
    'Exceptions',
    'Reporting_Period',
    'Created',
    'Created_By',
    '',
]

TSV_REPORT_DEFAULT_ROWS = [
    'Title',
    'Publisher',
    'Publisher_ID',
    'Platform',
    'DOI',
    'Proprietary_ID',
    'Print_ISSN',
    'Online_ISSN',
    'URI',
    'Metric_Type',
]

TSV_REPORT_TR_J4_ROWS = [
    'Title',
    'Publisher',
    'Publisher_ID',
    'Platform',
    'DOI',
    'Proprietary_ID',
    'Print_ISSN',
    'Online_ISSN',
    'URI',
    'YOP',
    'Metric_Type',
]

TSV_REPORT_LR_J1_ROWS = [
    'Title',
    'Publisher',
    'Publisher_ID',
    'Platform',
    'DOI',
    'Proprietary_ID',
    'Print_ISSN',
    'Online_ISSN',
    'URI',
    'Article_Language',
    'Metric_Type',
]

TSV_REPORT_IR_ROWS = [
    'Item',
    'Publisher',
    'Publisher_ID',
    'Platform',
    'Authors',
    'Publication_Date',
    'Article_Version',
    'DOI',
    'Proprietary_ID',
    'Print_ISSN',
    'Online_ISSN',
    'URI',
    'Parent_Title',
    'Parent_Authors',
    'Parent_Article_Version',
    'Parent_DOI',
    'Parent_Proprietary_ID',
    'Parent_Print_ISSN',
    'Parent_Online_ISSN',
    'Parent_URI',
    'Access_Type',
    'Metric_Type',
]