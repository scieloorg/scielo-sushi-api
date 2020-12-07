DELIMITER $$
CREATE PROCEDURE TR_J1_MONTHLY(IN beginDate date, IN endDate date)
BEGIN
    SELECT journal_id,
           SUBSTR(year_month_day, 1, 7) AS yearMonth,
           min(year_month_day) AS beginDate,
           max(year_month_day) AS endDate,
           cj.online_issn AS onlineISSN,
           cj.print_issn AS printISSN,
           cjc.title,
           cjc.publisher_name AS publisherName,
           cjc.uri,
           sum(total_item_requests) AS totalItemRequests,
           sum(unique_item_requests) As uniqueItemRequests
    FROM counter_article_metric
             JOIN counter_article ca ON counter_article_metric.fk_article_id = ca.article_id
             JOIN counter_journal cj ON cj.journal_id = ca.fk_art_journal_id
             JOIN counter_journal_collection cjc ON cj.journal_id = cjc.fk_col_journal_id
    WHERE year_month_day >= beginDate AND year_month_day <= endDate AND cjc.name = 'scl'
    GROUP BY journal_id, yearMonth;
END $$
DELIMITER ;