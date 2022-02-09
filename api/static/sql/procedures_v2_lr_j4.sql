DELIMITER $$
CREATE PROCEDURE V2_LR_J4_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		ajlyymm.`year_month` as yearMonth,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id,
		yop,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yop,
		yearMonth
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J4_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		MIN(ajlyymm.`year_month`) AS beginDate,
        MAX(ajlyymm.`year_month`) AS endDate,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id,
		yop
	ORDER BY
		journalID,
		articlesLanguage,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J4_JOURNAL_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		ajlyymm.`year_month` as yearMonth,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id,
		yop,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yop,
		yearMonth
	;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE V2_LR_J4_JOURNAL_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		MIN(ajlyymm.`year_month`) AS beginDate,
        MAX(ajlyymm.`year_month`) AS endDate,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id,
		yop
	ORDER BY
		journalID,
		articlesLanguage,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J4_YOP_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3), yop varchar(4))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		ajlyymm.`year_month` as yearMonth,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.yop = yop AND
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id,
		yop,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yop,
		yearMonth
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J4_YOP_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3), yop varchar(4))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		MIN(ajlyymm.`year_month`) AS beginDate,
        MAX(ajlyymm.`year_month`) AS endDate,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.yop = yop AND
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
	 	journalID,
	 	language_id,
		yop
	ORDER BY
		journalID,
		articlesLanguage,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_LR_J4_JOURNAL_YOP_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3), yop varchar(4))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		ajlyymm.`year_month` as yearMonth,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.yop = yop AND
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id,
		yop,
	 	yearMonth
	ORDER BY
		journalID,
		articlesLanguage,
		yop,
		yearMonth
	;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE V2_LR_J4_JOURNAL_YOP_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3), yop varchar(4))
BEGIN
	SELECT
		ajlyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		cal.`language` as articlesLanguage,
		ajlyymm.yop,
		MIN(ajlyymm.`year_month`) AS beginDate,
        MAX(ajlyymm.`year_month`) AS endDate,
		sum(ajlyymm.total_item_requests) as totalItemRequests,
		sum(ajlyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_language_yop_year_month_metric ajlyymm
	JOIN
		counter_journal cj ON cj.id = ajlyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	JOIN
		counter_article_language cal ON cal.id = ajlyymm.language_id
	WHERE
		ajlyymm.yop = yop AND
		ajlyymm.collection in (collection, collection_extra) AND
		ajlyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	language_id,
		yop
	ORDER BY
		journalID,
		articlesLanguage,
		yop
	;
END $$
DELIMITER ;
