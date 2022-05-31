--------------------------------------------------------\
--  DDL for Sequence SEQ_ENTRY_ID\
--------------------------------------------------------\
\
   CREATE SEQUENCE  "SENSOR_DATALAKE1"."SEQ_ENTRY_ID"  MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 133022 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  GLOBAL ;\
--------------------------------------------------------\
--  DDL for Table META_DATA\
--------------------------------------------------------\
\
  CREATE TABLE "SENSOR_DATALAKE1"."META_DATA" \
   (	"ID" NUMBER, \
	"SENSOR_NAME" VARCHAR2(50 BYTE) COLLATE "USING_NLS_COMP"\
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION DEFERRED \
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 \
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING\
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Table ROOM\
--------------------------------------------------------\
\
  CREATE TABLE "SENSOR_DATALAKE1"."ROOM" \
   (	"ROOM_NUMBER" NUMBER, \
	"LOCATION" VARCHAR2(50 BYTE) COLLATE "USING_NLS_COMP", \
	"SENSOR_ID" NUMBER\
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION DEFERRED \
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 \
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING\
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Table SENSOR_DATA\
--------------------------------------------------------\
\
  CREATE TABLE "SENSOR_DATALAKE1"."SENSOR_DATA" \
   (	"ENTRY_ID" NUMBER, \
	"INSERT_TIME" TIMESTAMP (6), \
	"SENSOR_ID" VARCHAR2(50 BYTE) COLLATE "USING_NLS_COMP", \
	"VALUE1" NUMBER, \
	"UNIT1" VARCHAR2(20 BYTE) COLLATE "USING_NLS_COMP"\
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE \
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 \
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING\
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645\
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1\
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)\
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Index SENSOR_DATA_PK\
--------------------------------------------------------\
\
  CREATE UNIQUE INDEX "SENSOR_DATALAKE1"."SENSOR_DATA_PK" ON "SENSOR_DATALAKE1"."SENSOR_DATA" ("ENTRY_ID") \
  PCTFREE 10 INITRANS 20 MAXTRANS 255 COMPUTE STATISTICS \
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645\
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1\
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)\
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Index META_DATA_PK\
--------------------------------------------------------\
\
  CREATE UNIQUE INDEX "SENSOR_DATALAKE1"."META_DATA_PK" ON "SENSOR_DATALAKE1"."META_DATA" ("ID") \
  PCTFREE 10 INITRANS 20 MAXTRANS 255 \
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Index ROOM_PK\
--------------------------------------------------------\
\
  CREATE UNIQUE INDEX "SENSOR_DATALAKE1"."ROOM_PK" ON "SENSOR_DATALAKE1"."ROOM" ("SENSOR_ID", "ROOM_NUMBER") \
  PCTFREE 10 INITRANS 20 MAXTRANS 255 \
  TABLESPACE "DATA" ;\
--------------------------------------------------------\
--  DDL for Procedure CREATE_ONE_SENSOR_DATA\
--------------------------------------------------------\
set define off;\
\
  CREATE OR REPLACE EDITIONABLE PROCEDURE "SENSOR_DATALAKE1"."CREATE_ONE_SENSOR_DATA" ( \
\
  p_sensor_id    IN  any_sensor_data_entry.sensor_id%TYPE, \
\
  p_sensor_name    IN  any_sensor_data_entry.sensor_name%TYPE, \
\
  p_sensor_type    IN  any_sensor_data_entry.sensor_type%TYPE, \
\
  p_value1       IN  any_sensor_data_entry.value1%TYPE, \
\
  p_scale1       IN  any_sensor_data_entry.scale1%TYPE, \
\
  p_unit1       IN  any_sensor_data_entry.unit1%TYPE, \
\
  p_entry_document       IN  any_sensor_data_entry.entry_document%TYPE \
\
) \
\
AS \
\
BEGIN \
\
  INSERT INTO any_sensor_data_entry (entry_id, insert_time, sensor_id, sensor_name, sensor_type, value1, scale1, unit1, entry_document) \
\
  VALUES (seq_entry_id.nextval, systimestamp, p_sensor_id, p_sensor_name, p_sensor_type, p_value1, p_scale1, p_unit1, p_entry_document); \
\
EXCEPTION \
\
  WHEN OTHERS THEN \
\
    HTP.print(SQLERRM); \
    \
END;\
\
/\
--------------------------------------------------------\
--  DDL for Procedure INSERT_SENSOR_DATA\
--------------------------------------------------------\
set define off;\
\
  CREATE OR REPLACE EDITIONABLE PROCEDURE "SENSOR_DATALAKE1"."INSERT_SENSOR_DATA" ( \
\
  p_sensor_id    IN  sensor_data.sensor_id%TYPE, \
\
  p_value1       IN  sensor_data.value1%TYPE, \
\
  p_unit1       IN  sensor_data.unit1%TYPE\
\
) \
\
AS \
\
BEGIN \
\
  INSERT INTO sensor_data (entry_id, insert_time, sensor_id, value1, unit1) \
\
  VALUES (seq_entry_id.nextval, systimestamp, p_sensor_id, p_value1, p_unit1); \
\
EXCEPTION \
\
  WHEN OTHERS THEN \
\
    HTP.print(SQLERRM); \
\
END;\
\
/\
--------------------------------------------------------\
--  Constraints for Table SENSOR_DATA\
--------------------------------------------------------\
\
  ALTER TABLE "SENSOR_DATALAKE1"."SENSOR_DATA" MODIFY ("ENTRY_ID" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."SENSOR_DATA" ADD CONSTRAINT "SENSOR_DATA_PK" PRIMARY KEY ("ENTRY_ID")\
  USING INDEX PCTFREE 10 INITRANS 20 MAXTRANS 255 COMPUTE STATISTICS \
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645\
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1\
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)\
  TABLESPACE "DATA"  ENABLE;\
--------------------------------------------------------\
--  Constraints for Table ROOM\
--------------------------------------------------------\
\
  ALTER TABLE "SENSOR_DATALAKE1"."ROOM" MODIFY ("ROOM_NUMBER" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."ROOM" MODIFY ("LOCATION" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."ROOM" MODIFY ("SENSOR_ID" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."ROOM" ADD CONSTRAINT "ROOM_PK" PRIMARY KEY ("SENSOR_ID", "ROOM_NUMBER")\
  USING INDEX PCTFREE 10 INITRANS 20 MAXTRANS 255 \
  TABLESPACE "DATA"  ENABLE;\
--------------------------------------------------------\
--  Constraints for Table META_DATA\
--------------------------------------------------------\
\
  ALTER TABLE "SENSOR_DATALAKE1"."META_DATA" MODIFY ("ID" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."META_DATA" MODIFY ("SENSOR_NAME" NOT NULL ENABLE);\
  ALTER TABLE "SENSOR_DATALAKE1"."META_DATA" ADD CONSTRAINT "META_DATA_PK" PRIMARY KEY ("ID")\
  USING INDEX PCTFREE 10 INITRANS 20 MAXTRANS 255 \
  TABLESPACE "DATA"  ENABLE;\
