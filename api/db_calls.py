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

PROCEDURE_DETECTOR_DICT = {
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
