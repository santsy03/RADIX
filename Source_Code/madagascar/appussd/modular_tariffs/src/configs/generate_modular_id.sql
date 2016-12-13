create or replace FUNCTION GENERATE_MODULAR_ID
(p_msisdn IN VARCHAR2, p_package IN VARCHAR2, p_action IN VARCHAR2, p_renew IN VARCHAR2, p_channel IN VARCHAR2)
RETURN NUMBER AS modular_id NUMBER(11);
BEGIN
  select modular_request_seq.nextval into modular_id from dual;
  insert into MODULAR_REQUEST(id, msisdn, package, action, renew, channel, created_at)
  VALUES(modular_request_seq.currval, p_msisdn, p_package, p_action, p_renew, p_channel, systimestamp);
RETURN modular_id;
END generate_modular_id;
/

