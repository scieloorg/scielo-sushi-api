DELIMITER $$
CREATE PROCEDURE V2_GR_J1_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajgymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgymm.country_code as countryCode,
		ajgymm.`year_month` as yearMonth,
		sum(ajgymm.total_item_requests) as totalItemRequests,
		sum(ajgymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_year_month_metric ajgymm
	JOIN
		counter_journal cj ON cj.id = ajgymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgymm.collection in (collection, collection_extra) AND
		ajgymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		yearMonth,
		countryCode
	ORDER BY
		journalID,
		yearMonth,
		countryCode
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J1_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajgymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgymm.country_code as countryCode,
		MIN(ajgymm.`year_month`) AS beginDate,
		MAX(ajgymm.`year_month`) AS endDate,
		sum(ajgymm.total_item_requests) as totalItemRequests,
		sum(ajgymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_year_month_metric ajgymm
	JOIN
		counter_journal cj ON cj.id = ajgymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgymm.collection in (collection, collection_extra) AND
		ajgymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		countryCode
	ORDER BY
		journalID,
		countryCode
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J1_JOURNAL_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajgymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgymm.country_code as countryCode,
		ajgymm.`year_month` as yearMonth,
		sum(ajgymm.total_item_requests) as totalItemRequests,
		sum(ajgymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_year_month_metric ajgymm
	JOIN
		counter_journal cj ON cj.id = ajgymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgymm.collection in (collection, collection_extra) AND
		ajgymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	yearMonth,
		countryCode
	ORDER BY
		journalID,
		yearMonth,
		countryCode
	;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE V2_GR_J1_JOURNAL_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), collection_extra varchar(3))
BEGIN
	SELECT
		ajgymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgymm.country_code as countryCode,
		MIN(ajgymm.`year_month`) AS beginDate,
        MAX(ajgymm.`year_month`) AS endDate,
		sum(ajgymm.total_item_requests) as totalItemRequests,
		sum(ajgymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_year_month_metric ajgymm
	JOIN
		counter_journal cj ON cj.id = ajgymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgymm.collection in (collection, collection_extra) AND
		ajgymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	countryCode
	ORDER BY
		journalID,
		countryCode
	;
END $$
DELIMITER ;
