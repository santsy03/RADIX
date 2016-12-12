CREATE TABLE DEALER_ME2U_WHITELIST
   (    ID NUMBER NOT NULL,
        MSISDN VARCHAR2(20) NOT NULL,
        CREATED_AT TIMESTAMP(6),
        MODIFIED_AT TIMESTAMP(6),
        ACTIVE NUMBER(5) NOT NULL,
        CONSTRAINT DEALER_ME2U_WHITELIST_PK PRIMARY KEY (ID),
        CONSTRAINT DEALER_ME2U_WHITELIST_UK1 UNIQUE (MSISDN));

CREATE SEQUENCE DEALER_ME2U_WHITELIST_SEQ START WITH 1 INCREMENT BY 1 NOMAXVALUE CACHE 20 NOCYCLE
/

CREATE OR REPLACE TRIGGER DEALER_ME2U_WHITELIST_TRG BEFORE INSERT ON DEALER_ME2U_WHITELIST
FOR EACH ROW
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF :NEW.ID IS NULL THEN
      SELECT DEALER_ME2U_WHITELIST_SEQ.NEXTVAL INTO :NEW.ID FROM DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
/
ALTER TRIGGER DEALER_ME2U_WHITELIST_TRG ENABLE;
/
