DELIMITER $$
CREATE PROCEDURE V2_IR_A1_ARTICLE_MONTHLY(IN beginDate varchar(7), IN endDate varchar(7), IN pidOrDoi varchar(255), IN collectionAcronym varchar(3), IN collectionAcronymExtra varchar(3))
BEGIN
	SELECT 
		GROUP_CONCAT(DISTINCT cjc.collection) AS articleCollection,
		cjc.title AS journalTitle,
		cjc.uri AS journalURI,
		cjc.publisher_name AS journalPublisher,
		cj.print_issn AS printISSN,
		cj.online_issn AS onlineISSN,
		GROUP_CONCAT(DISTINCT T3.doi) as articleDOI,
		GROUP_CONCAT(DISTINCT ca.pid) AS articlePID,
		GROUP_CONCAT(DISTINCT ca.yop) AS articleYOP,
		yearMonth,
		SUM(totalItemRequests) AS totalItemRequests,
		SUM(uniqueItemRequests) AS uniqueItemRequests	
	FROM (
		SELECT
			aajymm.collection AS collection,
			aajymm.article_id AS aid,
			doi,
			aajymm.`year_month` AS yearMonth,
			sum(aajymm.total_item_requests) AS totalItemRequests,
			sum(aajymm.unique_item_requests) AS uniqueItemRequests
		FROM
			aggr_article_journal_year_month_metric aajymm
		RIGHT JOIN
			(	
				SELECT 
					id,
					doi
				FROM 
					counter_article ca 
				RIGHT JOIN (
					SELECT
						cac.pid_v2 AS pid,
						cac.doi as doi
					FROM
						counter_article_code cac
					WHERE 
						cac.pid_v2 = pidOrDoi OR
						cac.pid_v3 = pidOrDoi OR
						cac.doi = pidOrDoi
					UNION
					SELECT
						cac.pid_v3 AS pid,
						cac.doi as doi
					FROM
						counter_article_code cac
					WHERE 
						cac.pid_v2 = pidOrDoi OR
						cac.pid_v3 = pidOrDoi OR
						cac.doi = pidOrDoi
				) AS T1 ON T1.pid = ca.pid	
			) AS T2 ON T2.id = aajymm.article_id
		WHERE
			(aajymm.collection IN (collectionAcronym, collectionAcronymExtra)) AND
			(`year_month` BETWEEN beginDate AND endDate)
		GROUP BY
			aajymm.collection,
			aajymm.article_id,
			aajymm.`year_month`
	) AS T3
	LEFT JOIN counter_article ca ON ca.id = T3.aid
	LEFT JOIN counter_journal_collection cjc ON (cjc.idjournal_jc = ca.idjournal_a AND cjc.collection = ca.collection)
	LEFT JOIN counter_journal cj ON cj.id = ca.idjournal_a
	GROUP BY
		yearMonth;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE V2_IR_A1_ARTICLE_TOTALS(IN beginDate varchar(7), IN endDate varchar(7), IN pidOrDoi varchar(255), IN collectionAcronym varchar(3), IN collectionAcronymExtra varchar(3))
BEGIN
	SELECT 
	    GROUP_CONCAT(DISTINCT cjc.collection) AS articleCollection,
	    cjc.title AS journalTitle,
	    cjc.uri AS journalURI,
	    cjc.publisher_name AS journalPublisher,
	    cj.print_issn AS printISSN,
	    cj.online_issn AS onlineISSN,
	    GROUP_CONCAT(DISTINCT T3.doi) as articleDOI,
	    GROUP_CONCAT(DISTINCT ca.pid) AS articlePID,
	    GROUP_CONCAT(DISTINCT ca.yop) AS articleYOP,
		MIN(T3.yearMonth) AS beginDate,
		MAX(T3.yearMonth) AS endDate,
	    SUM(totalItemRequests) AS totalItemRequests,
	    SUM(uniqueItemRequests) AS uniqueItemRequests	
	FROM (
	    SELECT
	        aajymm.collection AS collection,
	        aajymm.article_id AS aid,
	        doi,
	        aajymm.`year_month` AS yearMonth,
	        sum(aajymm.total_item_requests) AS totalItemRequests,
	        sum(aajymm.unique_item_requests) AS uniqueItemRequests
	    FROM
	        aggr_article_journal_year_month_metric aajymm
	    RIGHT JOIN
	        (	
	            SELECT 
	                id,
	                doi
	            FROM 
	                counter_article ca 
	            RIGHT JOIN (
	                SELECT
	                    cac.pid_v2 AS pid,
	                    cac.doi AS doi
	                FROM
	                    counter_article_code cac
	                WHERE 
	                    cac.pid_v2 = pidOrDoi OR
	                    cac.pid_v3 = pidOrDoi OR
	                    cac.doi = pidOrDoi
	                UNION
	                SELECT
	                    cac.pid_v3 AS pid,
	                    cac.doi AS doi
	                FROM
	                    counter_article_code cac
	                WHERE 
	                    cac.pid_v2 = pidOrDoi OR
	                    cac.pid_v3 = pidOrDoi OR
	                    cac.doi = pidOrDoi
	            ) AS T1 ON T1.pid = ca.pid	
	        ) AS T2 ON T2.id = aajymm.article_id
	    WHERE
	        (aajymm.collection IN (collectionAcronym, collectionAcronymExtra)) AND
	        (`year_month` BETWEEN beginDate AND endDate)
	    GROUP BY
	        aajymm.collection,
	        aajymm.article_id,
	        aajymm.`year_month`
	) AS T3
	LEFT JOIN counter_article ca ON ca.id = T3.aid
	LEFT JOIN counter_journal_collection cjc ON (cjc.idjournal_jc = ca.idjournal_a AND cjc.collection = ca.collection)
	LEFT JOIN counter_journal cj ON cj.id = ca.idjournal_a;
END $$
DELIMITER ;
