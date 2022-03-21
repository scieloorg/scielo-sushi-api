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
        aalymm.article_id as articleID,
        aalymm.language_id as languageCode,
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
        articleID,
        languageCode,
        yearMonth
    ORDER BY
        articleID,
        languageCode,
        yearMonth;
END $$
DELIMITER ;
