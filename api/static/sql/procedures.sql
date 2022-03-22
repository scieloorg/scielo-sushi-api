DELIMITER $$
CREATE PROCEDURE TR_J1_JOURNAL_TOTALS(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_metric
             JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
             JOIN counter_journal_collection cjc ON sushi_journal_metric.idjournal_sjm = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
        (online_issn <> '' OR print_issn <> '');
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J1_JOURNAL_MONTHLY(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           SUBSTR(sushi_journal_metric.year_month_day, 1, 7) AS yearMonth,
           MIN(sushi_journal_metric.year_month_day) AS beginDate,
           MAX(sushi_journal_metric.year_month_day) AS endDate,
           SUM(sushi_journal_metric.total_item_requests) AS totalItemRequests,
           SUM(sushi_journal_metric.unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_metric
             JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
             JOIN counter_journal_collection cjc ON sushi_journal_metric.idjournal_sjm = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J1_TOTALS(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_metric
             JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY cj.id;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J1_MONTHLY(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) As uniqueItemRequests
    FROM sushi_journal_metric
             JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY cj.id, yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J4_JOURNAL_TOTALS(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           min(year_month_day) AS beginDate,
           max(year_month_day) AS endDate,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           yop,
           sum(total_item_requests) AS totalItemRequests,
           sum(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_yop_metric
             JOIN counter_journal cj on sushi_journal_yop_metric.idjournal_sjym = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_yop_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY yop;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J4_JOURNAL_MONTHLY(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           cjc.collection AS collectionName,
           yop,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_yop_metric
             JOIN counter_journal cj on sushi_journal_yop_metric.idjournal_sjym = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_yop_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY yop,
             yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J4_TOTALS(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           yop,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_yop_metric
             JOIN counter_journal cj on sushi_journal_yop_metric.idjournal_sjym = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_yop_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY cj.id,
             yop;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE TR_J4_MONTHLY(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
    SELECT cj.id as journalID,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           min(year_month_day) AS beginDate,
           max(year_month_day) AS endDate,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           yop,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) As uniqueItemRequests
    FROM sushi_journal_yop_metric
             JOIN counter_journal cj on sushi_journal_yop_metric.idjournal_sjym = cj.id
             JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
    WHERE (cjc.collection = collection) AND
        (sushi_journal_yop_metric.collection = collection) AND
        (year_month_day between beginDate AND endDate) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY cj.id,
             yop,
             yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_JOURNAL_TOTALS(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection_acronym varchar(3), IN yop varchar(4))
BEGIN
    SELECT
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '') AND
          (ca.yop = yop)
    GROUP BY ca.pid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_JOURNAL_MONTHLY(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection_acronym varchar(3), IN yop varchar(4))
BEGIN
    SELECT
           cj.id as journalID,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '') AND
          (ca.yop = yop)
    GROUP BY ca.pid, yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_ARTICLE_TOTALS(IN beginDate date, IN endDate date, IN pid varchar(23), IN collection_acronym varchar(3))
BEGIN
    SELECT
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (pid = ca.pid) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '');
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_ARTICLE_MONTHLY(IN beginDate date, IN endDate date, IN pid varchar(23), IN collection_acronym varchar(3))
BEGIN
    SELECT
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (pid = ca.pid) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
    GROUP BY yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_MONTHLY(IN beginDate date, IN endDate date, IN collection_acronym varchar(3), IN yop varchar(3))
BEGIN
    SELECT
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '') AND
          (ca.yop = yop)
    GROUP BY ca.pid, yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_TOTALS(IN beginDate date, IN endDate date, IN collection_acronym varchar(3), IN yop varchar(3))
BEGIN
    SELECT
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           ca.collection,
           ca.pid,
           ca.yop,
           MIN(year_month_day) AS beginDate,
           MAX(year_month_day) AS endDate,
           SUM(total_item_requests) AS totalItemRequests,
           SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_article_metric
             JOIN counter_article ca on sushi_article_metric.idarticle_sam = ca.id
             JOIN counter_journal cj on ca.idjournal_a = cj.id
             JOIN counter_journal_collection cjc on cj.id = cjc.idjournal_jc
    WHERE (ca.collection = collection_acronym) AND
          (cjc.collection = collection_acronym) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '') AND
          (ca.yop = yop)
    GROUP BY ca.pid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE LR_A1_ARTICLE_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN pid varchar(23), IN collection varchar(3))
BEGIN
    SELECT
        cj.print_issn as printISSN,
        cj.online_issn as onlineISSN,
        cjc.title as journalTitle,
        cjc.uri as journalURI,
        cjc.publisher_name as journalPublisher,
        ca.collection as articleCollection,
        ca.pid as articlePID,
        cal.`language` as articleLanguage,
		MIN(aalymm.`year_month`) AS beginDate,
		MAX(aalymm.`year_month`) AS endDate,
        sum(aalymm.total_item_requests) as totalItemRequests,
        sum(aalymm.unique_item_requests) as uniqueItemRequests
    FROM
        aggr_article_language_year_month_metric aalymm
    JOIN
        counter_article ca ON ca.id = aalymm.article_id 
    JOIN
        counter_journal cj ON cj.id = ca.idjournal_a 
    JOIN
        counter_journal_collection cjc ON cjc.idjournal_jc = ca.idjournal_a 
    JOIN 
        counter_article_language cal ON cal.id = aalymm.language_id 
    WHERE
        aalymm.article_id in (
            select 
                id
            from 
                counter_article ca 
            where 
                ca.pid = pid AND 
                ca.collection = collection
        ) AND
        cjc.collection = collection AND
        aalymm.collection = collection AND
        `year_month` BETWEEN beginDate AND endDate
    GROUP BY
        articlePID,
        articleLanguage
    ORDER BY
        articlePID,
        articleLanguage;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE LR_A1_ARTICLE_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN pid varchar(23), IN collection varchar(3))
BEGIN
    SELECT
        cj.print_issn as printISSN,
        cj.online_issn as onlineISSN,
        cjc.title as journalTitle,
        cjc.uri as journalURI,
        cjc.publisher_name as journalPublisher,
        ca.collection as articleCollection,
        ca.pid as articlePID,
        cal.`language` as articleLanguage,
        aalymm.`year_month` as yearMonth,
        sum(aalymm.total_item_requests) as totalItemRequests,
        sum(aalymm.unique_item_requests) as uniqueItemRequests
    FROM
        aggr_article_language_year_month_metric aalymm
    JOIN
        counter_article ca ON ca.id = aalymm.article_id 
    JOIN
        counter_journal cj ON cj.id = ca.idjournal_a 
    JOIN
        counter_journal_collection cjc ON cjc.idjournal_jc = ca.idjournal_a 
    JOIN 
        counter_article_language cal ON cal.id = aalymm.language_id 
    WHERE
        aalymm.article_id in (
            select 
                id
            from 
                counter_article ca 
            where 
                ca.pid = pid AND 
                ca.collection = collection
        ) AND
        cjc.collection = collection AND
        aalymm.collection = collection AND
        `year_month` BETWEEN beginDate AND endDate
    GROUP BY
        articlePID,
        articleLanguage,
        yearMonth
    ORDER BY
        articlePID,
        articleLanguage,
        yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_TR_J1_JOURNAL_TOTALS(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
	SELECT
		T.journalID,
		T.onlineISSN,
		T.printISSN,
		cjc.title,
		cjc.publisher_name as publisherName,
		cjc.uri,
		T.beginDate,
		T.endDate,
		T.totalItemRequests,
		T.uniqueItemRequests,
		cjc.collection
		FROM (
            SELECT cj.id as journalID,
                cj.online_issn AS onlineISSN,
                cj.print_issn AS printISSN,
                MIN(year_month_day) AS beginDate,
                MAX(year_month_day) AS endDate,
                SUM(total_item_requests) AS totalItemRequests,
                SUM(unique_item_requests) AS uniqueItemRequests,
                sushi_journal_metric.collection
            FROM sushi_journal_metric
                JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
            WHERE
                (year_month_day between beginDate AND endDate) AND
                (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
                (online_issn <> '' OR print_issn <> '')
            GROUP BY
                journalID
	    ) AS T
	JOIN counter_journal cj ON cj.id = T.journalID
	JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
	WHERE cjc.collection = collection
    ORDER BY
        journalID ASC,
        beginDate ASC;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_TR_J1_JOURNAL_MONTHLY(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection varchar(3))
BEGIN
	SELECT
		T.journalID,
		T.onlineISSN,
		T.printISSN,
		cjc.title,
		cjc.publisher_name as publisherName,
		cjc.uri,
		T.yearMonth,
		T.beginDate,
		T.endDate,
		T.totalItemRequests,
		T.uniqueItemRequests,
		cjc.collection
		FROM (
            SELECT cj.id as journalID,
                cj.online_issn AS onlineISSN,
                cj.print_issn AS printISSN,
                SUBSTR(sushi_journal_metric.year_month_day, 1, 7) AS yearMonth,
                MIN(year_month_day) AS beginDate,
                MAX(year_month_day) AS endDate,
                SUM(total_item_requests) AS totalItemRequests,
                SUM(unique_item_requests) AS uniqueItemRequests,
                sushi_journal_metric.collection
            FROM sushi_journal_metric
                JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
            WHERE
                (year_month_day between beginDate AND endDate) AND
                (issn = cj.online_issn OR issn = cj.print_issn OR issn = cj.pid_issn) AND
                (online_issn <> '' OR print_issn <> '')
            GROUP BY
                journalID,
                yearMonth
	    ) AS T
	JOIN counter_journal cj ON cj.id = T.journalID
	JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
	WHERE cjc.collection = collection
    ORDER BY
        journalID ASC,
        yearMonth ASC;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_TR_J1_TOTALS(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
	SELECT
		T.journalID,
		T.onlineISSN,
		T.printISSN,
		cjc.title,
		cjc.publisher_name as publisherName,
		cjc.uri,
		T.beginDate,
		T.endDate,
		T.totalItemRequests,
		T.uniqueItemRequests,
		cjc.collection
		FROM (
            SELECT cj.id as journalID,
                cj.online_issn AS onlineISSN,
                cj.print_issn AS printISSN,
                MIN(year_month_day) AS beginDate,
                MAX(year_month_day) AS endDate,
                SUM(total_item_requests) AS totalItemRequests,
                SUM(unique_item_requests) AS uniqueItemRequests,
                sushi_journal_metric.collection
            FROM sushi_journal_metric
                JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
            WHERE
                (year_month_day between beginDate AND endDate) AND
                (online_issn <> '' OR print_issn <> '')
            GROUP BY
                journalID
	    ) AS T
	JOIN counter_journal cj ON cj.id = T.journalID
	JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
	WHERE cjc.collection = collection
    ORDER BY
        journalID ASC,
        beginDate ASC;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_TR_J1_MONTHLY(IN beginDate date, IN endDate date, IN collection varchar(3))
BEGIN
	SELECT
		T.journalID,
		T.onlineISSN,
		T.printISSN,
		cjc.title,
		cjc.publisher_name as publisherName,
		cjc.uri,
		T.yearMonth,
		T.beginDate,
		T.endDate,
		T.totalItemRequests,
		T.uniqueItemRequests,
		cjc.collection
		FROM (
            SELECT cj.id as journalID,
                cj.online_issn AS onlineISSN,
                cj.print_issn AS printISSN,
                SUBSTR(sushi_journal_metric.year_month_day, 1, 7) AS yearMonth,
                MIN(year_month_day) AS beginDate,
                MAX(year_month_day) AS endDate,
                SUM(total_item_requests) AS totalItemRequests,
                SUM(unique_item_requests) AS uniqueItemRequests,
                sushi_journal_metric.collection
            FROM sushi_journal_metric
                JOIN counter_journal cj on sushi_journal_metric.idjournal_sjm = cj.id
            WHERE
                (year_month_day between beginDate AND endDate) AND
                (online_issn <> '' OR print_issn <> '')
            GROUP BY
                journalID,
                yearMonth
	    ) AS T
	JOIN counter_journal cj ON cj.id = T.journalID
	JOIN counter_journal_collection cjc ON cj.id = cjc.idjournal_jc
	WHERE cjc.collection = collection
    ORDER BY
        journalID ASC,
        yearMonth ASC;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_CR_J1_TOTALS(IN beginDate date, IN endDate date, IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
    SELECT
        MIN(year_month_day) AS beginDate,
        MAX(year_month_day) AS endDate,
        SUM(total_item_requests) AS totalItemRequests,
        SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_metric sjm
        JOIN counter_journal cj on sjm.idjournal_sjm = cj.id
    WHERE
    	(sjm.collection in (collection , collection_extra)) AND
	    (year_month_day between beginDate AND endDate) AND
    	(cj.online_issn <> '' OR cj.print_issn <> '')
    ORDER BY
        beginDate ASC;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_CR_J1_MONTHLY(IN beginDate date, IN endDate date, IN collection varchar(3), IN collection_extra varchar(3))
BEGIN
    SELECT
        SUBSTR(sjm.year_month_day, 1, 7) AS yearMonth,
        MIN(year_month_day) AS beginDate,
        MAX(year_month_day) AS endDate,
        SUM(total_item_requests) AS totalItemRequests,
        SUM(unique_item_requests) AS uniqueItemRequests
    FROM sushi_journal_metric sjm
        JOIN counter_journal cj on sjm.idjournal_sjm = cj.id
    WHERE
    	(sjm.collection in (collection, collection_extra)) AND
        (year_month_day between beginDate AND endDate) AND
        (online_issn <> '' OR print_issn <> '')
    GROUP BY
    	yearMonth
    ORDER BY
        yearMonth ASC;
END $$
DELIMITER ;
