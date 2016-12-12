CREATE TABLE MODULAR_REQUEST
(ID NUMBER(11,0) NOT NULL ENABLE,
    MSISDN VARCHAR2(20),
    PACKAGE VARCHAR2(20),
    ACTION VARCHAR2(10),
    RENEW VARCHAR2(10),
    CHANNEL VARCHAR2(10),
    CREATED_AT TIMESTAMP (6),
    RESPONSE VARCHAR2(200),
    COMPLETED_AT TIMESTAMP (6))
PARTITION BY RANGE(ID)
INTERVAL (6000000)
(PARTITION MODULAR_REQUEST_P1 VALUES LESS THAN (6000000),
PARTITION MODULAR_REQUEST_P2 VALUES LESS THAN (12000000),
PARTITION MODULAR_REQUEST_P3 VALUES LESS THAN (18000000),
PARTITION MODULAR_REQUEST_P4 VALUES LESS THAN (24000000),
PARTITION MODULAR_REQUEST_P5 VALUES LESS THAN (30000000),
PARTITION MODULAR_REQUEST_P6 VALUES LESS THAN (36000000),
PARTITION MODULAR_REQUEST_P7 VALUES LESS THAN (42000000),
PARTITION MODULAR_REQUEST_P8 VALUES LESS THAN (48000000),
PARTITION MODULAR_REQUEST_P9 VALUES LESS THAN (54000000),
PARTITION MODULAR_REQUEST_P10 VALUES LESS THAN (60000000),
PARTITION MODULAR_REQUEST_P11 VALUES LESS THAN (66000000),
PARTITION MODULAR_REQUEST_P12 VALUES LESS THAN (72000000))
/