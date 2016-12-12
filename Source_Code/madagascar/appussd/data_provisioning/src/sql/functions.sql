create or replace FUNCTION GENERATE_TRANSACTIONID
(p_user_id IN VARCHAR2,p_request_id IN NUMBER,p_msisdn IN VARCHAR2, p_package_id IN NUMBER, p_status IN NUMBER, p_callback IN VARCHAR2, p_b_msisdn IN VARCHAR2, p_transaction_type IN VARCHAR2, p_channel IN VARCHAR2, p_params IN VARCHAR2)
RETURN NUMBER AS transactionId NUMBER(11);
BEGIN
  select requests_seq.nextval into transactionId from dual;
  insert into REQUESTS(id,user_id,request_id,msisdn,package_Id,status,created_at,callback,b_msisdn,Transaction_type,channel,params) 
  VALUES(requests_seq.currval,p_user_id,p_request_id,p_msisdn,p_package_id,p_status,systimestamp,p_callback, p_b_msisdn, p_transaction_type, p_channel, p_params);
RETURN transactionId;
END generate_TransactionId;
/
