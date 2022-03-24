DELIMITER $$
CREATE PROCEDURE V2_IR_A4_JOURNAL_YOP_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collectionAcronym varchar(3), IN collectionAcronymExtra varchar(3), IN yearOfPublication varchar(4))
BEGIN
	SELECT 
		GROUP_CONCAT(DISTINCT journalCollection) AS journalCollection,
		GROUP_CONCAT(DISTINCT journalTitle) AS journalTitle,
		GROUP_CONCAT(DISTINCT journalURI) AS journalURI,
		GROUP_CONCAT(DISTINCT journalPublisher) AS journalPublisher,
		cj2.print_issn AS printISSN,
		cj2.online_issn AS onlineISSN,
		GROUP_CONCAT(DISTINCT articlePID) AS articlePID,
		articleDOI,
        articleYOP,
		yearMonth,
		SUM(total_item_requests) AS totalItemRequests,
		SUM(unique_item_requests) AS uniqueItemRequests
	FROM
		(
		SELECT 
			cjc.collection AS journalCollection,
            cjc.idjournal_jc,
			cjc.title AS journalTitle,
			cjc.uri AS journalURI,
			cjc.publisher_name AS journalPublisher,
            ca.yop as articleYOP,
			ca.pid AS articlePID,
			cac.doi AS articleDOI,
			aajymm.`year_month` AS yearMonth,
			total_item_requests,
			unique_item_requests
		FROM
			aggr_article_journal_year_month_metric aajymm
		JOIN
			counter_article ca ON ca.id = aajymm.article_id
		JOIN
			counter_journal_collection cjc ON cjc.idjournal_jc = aajymm.journal_id
		JOIN 
			counter_article_code cac ON ca.pid = cac.pid_v3
		WHERE 
			aajymm.journal_id = (
				SELECT 
					id
				FROM
					counter_journal cj 
				WHERE
					cj.print_issn = issn OR
					cj.online_issn = issn OR
					cj.pid_issn = issn
				LIMIT 1
			) AND
			cjc.collection = ca.collection AND
			cjc.collection in (collectionAcronym, collectionAcronymExtra) AND
			ca.yop = yearOfPublication
		UNION
		SELECT 
			cjc.collection AS journalCollection,
            cjc.idjournal_jc,
			cjc.title AS journalTitle,
			cjc.uri AS journalURI,
			cjc.publisher_name AS journalPublisher,
            ca.yop as articleYOP,
			ca.pid AS articlePID,
			cac.doi AS articleDOI,
			aajymm.`year_month` AS yearMonth,
			total_item_requests,
			unique_item_requests
		FROM
			aggr_article_journal_year_month_metric aajymm
		JOIN
			counter_article ca ON ca.id = aajymm.article_id
		JOIN
			counter_journal_collection cjc ON cjc.idjournal_jc = aajymm.journal_id
		JOIN 
			counter_article_code cac ON ca.pid = cac.pid_v2
		WHERE 
			aajymm.journal_id = (
				SELECT 
					id
				FROM
					counter_journal cj 
				WHERE
					cj.print_issn = issn OR
					cj.online_issn = issn OR
					cj.pid_issn = issn
				LIMIT 1
			) AND
			cjc.collection = ca.collection AND
			cjc.collection in (collectionAcronym, collectionAcronymExtra) AND
			ca.yop = yearOfPublication
	) AS T1
	JOIN counter_journal cj2 ON cj2.id = idjournal_jc
	GROUP BY
		articleDOI,
		yearMonth
	;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_IR_A4_JOURNAL_YOP_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN issn varchar(9), IN collectionAcronym varchar(3), IN collectionAcronymExtra varchar(3), IN yearOfPublication varchar(4))
BEGIN
	SELECT 
		GROUP_CONCAT(DISTINCT journalCollection) AS journalCollection,
		GROUP_CONCAT(DISTINCT journalTitle) AS journalTitle,
		GROUP_CONCAT(DISTINCT journalURI) AS journalURI,
		GROUP_CONCAT(DISTINCT journalPublisher) AS journalPublisher,
		cj2.print_issn AS printISSN,
		cj2.online_issn AS onlineISSN,
		GROUP_CONCAT(DISTINCT articlePID) AS articlePID,
		articleDOI,
        articleYOP,
		MIN(T1.yearMonth) AS beginDate,
		MAX(T1.yearMonth) AS endDate,
		SUM(total_item_requests) AS totalItemRequests,
		SUM(unique_item_requests) AS uniqueItemRequests
	FROM
		(
		SELECT 
			cjc.collection AS journalCollection,
            cjc.idjournal_jc,
			cjc.title AS journalTitle,
			cjc.uri AS journalURI,
			cjc.publisher_name AS journalPublisher,
            ca.yop as articleYOP,
			ca.pid AS articlePID,
			cac.doi AS articleDOI,
			aajymm.`year_month` AS yearMonth,
			total_item_requests,
			unique_item_requests
		FROM
			aggr_article_journal_year_month_metric aajymm
		JOIN
			counter_article ca ON ca.id = aajymm.article_id
		JOIN
			counter_journal_collection cjc ON cjc.idjournal_jc = aajymm.journal_id
		JOIN 
			counter_article_code cac ON ca.pid = cac.pid_v3
		WHERE 
			aajymm.journal_id = (
				SELECT 
					id
				FROM
					counter_journal cj 
				WHERE
					cj.print_issn = issn OR
					cj.online_issn = issn OR
					cj.pid_issn = issn
				LIMIT 1
			) AND
			cjc.collection = ca.collection AND
			cjc.collection in (collectionAcronym, collectionAcronymExtra) AND
			ca.yop = yearOfPublication
		UNION
		SELECT 
			cjc.collection AS journalCollection,
            cjc.idjournal_jc,
			cjc.title AS journalTitle,
			cjc.uri AS journalURI,
			cjc.publisher_name AS journalPublisher,
            ca.yop as articleYOP,
			ca.pid AS articlePID,
			cac.doi AS articleDOI,
			aajymm.`year_month` AS yearMonth,
			total_item_requests,
			unique_item_requests
		FROM
			aggr_article_journal_year_month_metric aajymm
		JOIN
			counter_article ca ON ca.id = aajymm.article_id
		JOIN
			counter_journal_collection cjc ON cjc.idjournal_jc = aajymm.journal_id
		JOIN 
			counter_article_code cac ON ca.pid = cac.pid_v2
		WHERE 
			aajymm.journal_id = (
				SELECT 
					id
				FROM
					counter_journal cj 
				WHERE
					cj.print_issn = issn OR
					cj.online_issn = issn OR
					cj.pid_issn = issn
				LIMIT 1
			) AND
			cjc.collection = ca.collection AND
			cjc.collection in (collectionAcronym, collectionAcronymExtra) AND
			ca.yop = yearOfPublication
	) AS T1
	JOIN counter_journal cj2 ON cj2.id = idjournal_jc
	GROUP BY
		articleDOI
	;
END $$
DELIMITER ;