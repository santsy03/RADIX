 CREATE OR REPLACE FUNCTION BALANCE_REQ_PROC (p_msisdn IN VARCHAR2,p_session in varchar2, p_channel in varchar2) 
RETURN NUMBER AS transactionId NUMBER(11)
/
 BEGIN select balance_SQC.nextval into transactionId from dual
/
insert into balance_requests (id,msisdn,session_id,channel,created_at)
VALUES (transactionId,p_msisdn,p_session,p_channel,systimestamp)
RETURN transactionId END balance_req_proc 
/ 
