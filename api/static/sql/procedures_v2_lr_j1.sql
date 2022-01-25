DELIMITER $$
CREATE PROCEDURE V2_LR_J1_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlymm.`year_month` as yearMonth,
		sum(ajlymm.total_item_requests) as totalItemRequests,
		sum(ajlymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_year_month_metric ajlymm
	JOIN
		counter_journal cj ON cj.id = ajlymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlymm.language_id
	WHERE
		ajlymm.collection in (collection, collection_extra) AND
		ajlymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yearMonth
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J1_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		MIN(ajlymm.`year_month`) AS beginDate,
        MAX(ajlymm.`year_month`) AS endDate,
		sum(ajlymm.total_item_requests) as totalItemRequests,
		sum(ajlymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_year_month_metric ajlymm
	JOIN
		counter_journal cj ON cj.id = ajlymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlymm.language_id
	WHERE
		ajlymm.collection in (collection, collection_extra) AND
		ajlymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id
	ORDER BY
		journalID,
		articlesLanguage
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J1_JOURNAL_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlymm.`year_month` as yearMonth,
		sum(ajlymm.total_item_requests) as totalItemRequests,
		sum(ajlymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_year_month_metric ajlymm
	JOIN
		counter_journal cj ON cj.id = ajlymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlymm.language_id
	WHERE
		ajlymm.collection in (collection, collection_extra) AND
		ajlymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yearMonth
	;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE V2_LR_J1_JOURNAL_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		MIN(ajlymm.`year_month`) AS beginDate,
        MAX(ajlymm.`year_month`) AS endDate,
		sum(ajlymm.total_item_requests) as totalItemRequests,
		sum(ajlymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_year_month_metric ajlymm
	JOIN
		counter_journal cj ON cj.id = ajlymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlymm.language_id
	WHERE
		ajlymm.collection in (collection, collection_extra) AND
		ajlymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id
	ORDER BY
		journalID,
		articlesLanguage
	;
END $$
DELIMITER ;
