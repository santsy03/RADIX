create or replace FUNCTION GEN_ME2U_TRANS_ID
(p_msisdn IN VARCHAR2,p_recipient IN VARCHAR2, p_amount IN VARCHAR2)
RETURN NUMBER AS transaction_id NUMBER(12);
BEGIN
  select ME2U_CDR_SEQ.nextval into transaction_id from dual;
  insert into ME2U_CDR (id,msisdn,recipient,amount,created_at) 
  VALUES(ME2U_CDR_SEQ.currval,p_msisdn,p_recipient,p_amount,systimestamp);
RETURN transaction_id;
END gen_me2u_trans_id;
/
