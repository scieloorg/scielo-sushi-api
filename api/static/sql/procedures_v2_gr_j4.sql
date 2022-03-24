DELIMITER $$
CREATE PROCEDURE V2_GR_J4_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		ajgyymm.`year_month` as yearMonth,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		yearMonth,
		countryCode,
		yop
	ORDER BY
		journalID,
		yearMonth,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		MIN(ajgyymm.`year_month`) AS beginDate,
		MAX(ajgyymm.`year_month`) AS endDate,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		countryCode,
		yop
	ORDER BY
		journalID,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_JOURNAL_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		ajgyymm.`year_month` as yearMonth,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	yearMonth,
		countryCode,
		yop
	ORDER BY
		journalID,
		yearMonth,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_JOURNAL_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		MIN(ajgyymm.`year_month`) AS beginDate,
        MAX(ajgyymm.`year_month`) AS endDate,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	countryCode,
		yop
	ORDER BY
		journalID,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_YOP_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), IN collection_extra varchar(3), IN yop varchar(4))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		ajgyymm.`year_month` as yearMonth,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.yop = yop AND
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		yearMonth,
		countryCode,
		yop
	ORDER BY
		journalID,
		yearMonth,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_YOP_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN collection varchar(3), IN collection_extra varchar(3), IN yop varchar(4))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		MIN(ajgyymm.`year_month`) AS beginDate,
		MAX(ajgyymm.`year_month`) AS endDate,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.yop = yop AND
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate
	GROUP BY
		journalID,
		countryCode,
		yop
	ORDER BY
		journalID,
		countryCode,
		yop
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_GR_J4_JOURNAL_YOP_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), IN collection_extra varchar(3), IN yop varchar(4))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		ajgyymm.`year_month` as yearMonth,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.yop = yop AND
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	yearMonth,
		countryCode,
		yop
	ORDER BY
		journalID,
		yearMonth,
		countryCode,
		yop
	;
END $$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE V2_GR_J4_JOURNAL_YOP_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collection varchar(3), IN collection_extra varchar(3), IN yop varchar(4))
BEGIN
	SELECT
		ajgyymm.journal_id as journalID,
		cj.print_issn as printISSN,
		cj.online_issn as onlineISSN,
		cjc.title as title,
		cjc.uri as uri,
		cjc.publisher_name as publisherName,
		ajgyymm.country_code as countryCode,
		ajgyymm.yop as yop,
		MIN(ajgyymm.`year_month`) AS beginDate,
        MAX(ajgyymm.`year_month`) AS endDate,
		sum(ajgyymm.total_item_requests) as totalItemRequests,
		sum(ajgyymm.unique_item_requests) as uniqueItemRequests
	FROM
		aggr_journal_geolocation_yop_year_month_metric ajgyymm
	JOIN
		counter_journal cj ON cj.id = ajgyymm.journal_id
	JOIN
		counter_journal_collection cjc ON cjc.idjournal_jc = cj.id
	WHERE
		ajgyymm.yop = yop AND
		ajgyymm.collection in (collection, collection_extra) AND
		ajgyymm.collection = cjc.collection AND
		`year_month` BETWEEN beginDate AND endDate AND
	    (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
	    (online_issn <> '' OR print_issn <> '')
	GROUP BY
	 	journalID,
	 	countryCode,
		yop
	ORDER BY
		journalID,
		countryCode,
		yop
	;
END $$
DELIMITER ;
