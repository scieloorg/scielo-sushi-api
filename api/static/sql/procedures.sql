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
    SELECT sushi_journal_metric.id as journalID,
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
        (sushi_journal_metric.collection = collection AND)
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
CREATE PROCEDURE IR_A1_JOURNAL_TOTALS(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection_acronym varchar(3))
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
          (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
    GROUP BY ca.pid;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_JOURNAL_MONTHLY(IN beginDate date, IN endDate date, IN issn varchar(9), IN collection_acronym varchar(3))
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
          (issn = online_issn OR issn = print_issn OR issn = pid_issn) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
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
          (pid = ca.pid) AND
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
    GROUP BY yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_MONTHLY(IN beginDate date, IN endDate date, IN collection_acronym varchar(3))
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
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
    GROUP BY ca.pid, yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE IR_A1_TOTALS(IN beginDate date, IN endDate date, IN collection_acronym varchar(3))
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
          (year_month_day between beginDate AND endDate) AND
          (online_issn <> '' OR print_issn <> '')
    GROUP BY ca.pid;
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
	WHERE cjc.collection = collection;
END $$
DELIMITER ;
