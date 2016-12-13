CREATE  TABLE NEW_PACKAGES
(   "ID" NUMBER(11,0) NOT NULL ENABLE,
    "PROVISIONING_PACKAGES_ID" NUMBER NOT NULL ENABLE,
    "PACKAGE_NAME" VARCHAR2(20) NOT NULL ENABLE,
    "CREATED_AT" DATE,
    "MODIFIED_AT" DATE,
    "PACKAGE_COST" NUMBER(11,0) NOT NULL ENABLE,
    "REFILL_ID" VARCHAR2(20) NOT NULL ENABLE,
    "TRANS_AMOUNT" VARCHAR2(20),
     CONSTRAINT "NEW_PACKAGES_PK" PRIMARY KEY ("ID")
)
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('1','1', 'MyMeg 5', sysdate, sysdate, '500','MB01', '500')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('2','2', 'MyMeg 10', sysdate, sysdate, '1200','MB02','1200')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('3','3', 'MyMeg 20', sysdate, sysdate, '2000','MB03','2000')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('4','4', 'MyMeg 50', sysdate, sysdate, '3000','MB04','3000')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('5','5', 'MyMeg 60', sysdate, sysdate, '4000','MB05','4000')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('6','6', 'MyMeg 100', sysdate, sysdate, '5700','MB06','5700')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('7','7', 'MyMeg 200', sysdate, sysdate, '11400','MB07','11400')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('8','8', 'MyMeg 250', sysdate, sysdate, '13500','MB08','13500')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('9','9', 'MyMeg 500', sysdate, sysdate, '25500','MB09','25500')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('10','10', 'MyMeg 750', sysdate, sysdate, '38250','MB10','38250')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('11','11', 'MyGig 1', sysdate, sysdate, '45000','MB11','45000')
/
INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('12','12', 'MyGig 2', sysdate, sysdate, '67500','MB12','67500')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('13','13', 'MyGig 3', sysdate, sysdate, '72500','MB13','72500')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('14','14', 'MyGig 5', sysdate, sysdate, '90000','MB14','90000')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('15','15', 'MyGig 10', sysdate, sysdate, '135000','MB15','135000')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('16','16', 'MyGig 30', sysdate, sysdate, '180000','MB16','180000')
/






