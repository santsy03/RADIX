CREATE TABLE ME2U_TRACKER
   (    ID NUMBER NOT NULL,
        MSISDN VARCHAR2(20) NOT NULL,
        COUNT NUMBER(5),
        REQUESTED_AT TIMESTAMP,
        COMPLETED_AT TIMESTAMP,
        STATUS_CODE NUMBER(10),
        CONSTRAINT ME2U_TRACKER_PK PRIMARY KEY (ID),
        CONSTRAINT ME2U_UK1 UNIQUE (MSISDN));


CREATE INDEX ME2U_TRACKER_INDEX ON ME2U_TRACKER (COMPLETED_AT);
/

CREATE SEQUENCE ME2U_TRACKER_SEQ START WITH 1 INCREMENT BY 1 NOMAXVALUE CACHE 20 NOCYCLE
/

CREATE OR REPLACE TRIGGER ME2U_TRACKER_TRG BEFORE INSERT ON ME2U_TRACKER
FOR EACH ROW
BEGIN
  <<COLUMN_SEQUENCES>>
  BEGIN
    IF :NEW.ID IS NULL THEN
      SELECT ME2U_TRACKER_SEQ.NEXTVAL INTO :NEW.ID FROM DUAL;
    END IF;
  END COLUMN_SEQUENCES;
END;
/
ALTER TRIGGER ME2U_TRACKER_TRG ENABLE;
/