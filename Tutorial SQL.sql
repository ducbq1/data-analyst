IF NOT EXISTS (
  SELECT * 
  FROM   sys.columns 
  WHERE  object_id = OBJECT_ID(N'[dbo].[NH_NhuCauChiQuy]') 
         AND name = 'iID_KHTongTheID'
)
ALTER TABLE [dbo].[NH_NhuCauChiQuy]
ADD [iID_KHTongTheID] [uniqueidentifier] NULL;

------------------------------------------

SELECT * FROM TABLE_TEST a
WHERE id < (
  SELECT TOP 1 * FROM TABLE_TEST b
  WHERE a.name = b.name
  AND b.code = '104'
  ORDER BY b.id
)

------------------------------------------

DECLARE @COUNTER INT = 0;
DECLARE @MAX INT = (SELECT COUNT(DISTINCT Ten) FROM __TEST)
DECLARE @VALUE VARCHAR(50);
DROP TABLE #TempTable
CREATE TABLE #TempTable(
Ten nvarchar(50),
Ma nvarchar(50),
ID int)

WHILE @COUNTER < @MAX
BEGIN

SET @VALUE = (SELECT DISTINCT(Ten) FROM __TEST
			ORDER BY Ten
			OFFSET @COUNTER ROWS
			FETCH NEXT 1 ROWS ONLY)
      
PRINT @VALUE

insert into #TempTable
SELECT * FROM __TEST
WHERE Ten = @VALUE
AND ID <= (SELECT TOP 1 ID FROM __TEST WHERE Ten = @VALUE AND Ma = 104 ORDER BY ID DESC)

SET @COUNTER = @COUNTER + 1

END

select * from #TempTable

------------------------------------------
