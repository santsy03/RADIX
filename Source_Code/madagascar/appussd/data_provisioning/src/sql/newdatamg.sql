INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('17','17', 'Kozy Kozy', sysdate, sysdate, '750','MB63','750')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('18','18', 'Bundles Universite', sysdate, sysdate, '0','MB71','0')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('19','19', 'Facebook', sysdate, sysdate, '1000','MB72','1000')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('20','20', 'Twitter', sysdate, sysdate, '1000','MB73','1000')
/

INSERT INTO NEW_PACKAGES (ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('21','21', 'Whatsapp', sysdate, sysdate, '1000','MB74','1000')
/

UPDATE NEW_PACKAGES SET PACKAGE_NAME='MyMeg 15', PACKAGE_COST = '100',  REFILL_ID = 'MB01', TRANS_AMOUNT = '10000' WHERE ID = 1

(ID, PROVISIONING_PACKAGES_ID, PACKAGE_NAME, CREATED_AT, MODIFIED_AT, PACKAGE_COST, REFILL_ID, TRANS_AMOUNT)
VALUES ('55','55', 'Bundles Routeurs', sysdate, sysdate, '0','MB62','0')

UPDATE NEW_PROVISIONING_PACKAGES SET VOLUME = '15',VALIDITY='1', OFFER_ID = '1011' where id = 1;

(ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('55', '5','10240', '365', '1072')





INSERT INTO NEW_PROVISIONING_PACKAGES (ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('17', '1','30', '1', '1073')

/
INSERT INTO NEW_PROVISIONING_PACKAGES (ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('18', '1','51200', '720', '1081')

/
INSERT INTO NEW_PROVISIONING_PACKAGES (ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('19', '1','75', '1', '1082')

/
INSERT INTO NEW_PROVISIONING_PACKAGES (ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('20', '1','75', '1', '1083')

/
INSERT INTO NEW_PROVISIONING_PACKAGES (ID, PACKAGE_CATEGORY_ID,VOLUME,VALIDITY,OFFER_ID)
VALUES('21', '1','75', '1', '1084')

/
