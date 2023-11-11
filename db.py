import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

# Подключение к базе
db = mysql.connector.connect(**config["client"])
db_act = db.cursor()
db.autocommit = True


def create_table():
    try:

        create_tab_area = "CREATE TABLE AREA_INFO (AR_ID INT NOT NULL AUTO_INCREMENT, AREA VARCHAR(255) NOT NULL, " \
                          "PRIMARY KEY (AR_ID));"
        db_act.execute(create_tab_area)

        create_tab_address = "CREATE TABLE ADDRESS_INFO (ADR_ID INT NOT NULL AUTO_INCREMENT, ADDRESS VARCHAR(255) NOT " \
                             "NULL, PRIMARY KEY (ADR_ID));"
        db_act.execute(create_tab_address)

        create_tab_ram_man = "CREATE TABLE RAM_MAN_INFO (RAM_MAN_ID INT NOT NULL AUTO_INCREMENT, RAM_MAN VARCHAR(255) " \
                             "NOT NULL, PRIMARY KEY (RAM_MAN_ID));"
        db_act.execute(create_tab_ram_man)

        create_tab_ram_freq = "CREATE TABLE RAM_FREQ_INFO (RAM_FREQ_ID INT NOT NULL AUTO_INCREMENT, RAM_FREQ VARCHAR(" \
                              "255) NOT NULL, PRIMARY KEY (RAM_FREQ_ID));"
        db_act.execute(create_tab_ram_freq)

        create_tab_ram_cap = "CREATE TABLE RAM_CAP_INFO (RAM_CAP_ID INT NOT NULL AUTO_INCREMENT, RAM_CAP VARCHAR(255) " \
                             "NOT NULL, PRIMARY KEY (RAM_CAP_ID));"
        db_act.execute(create_tab_ram_cap)

        create_tab_ram_type = "CREATE TABLE RAM_TYPE_INFO (RAM_TYPE_ID INT NOT NULL AUTO_INCREMENT, RAM_TYPE VARCHAR(" \
                              "255) NOT NULL, PRIMARY KEY (RAM_TYPE_ID));"
        db_act.execute(create_tab_ram_type)

        create_tab_monitor = "CREATE TABLE MONITOR_INFO (MON_ID INT NOT NULL AUTO_INCREMENT, MON_MODEL VARCHAR(255) " \
                             "NOT NULL, MON_SR VARCHAR(255) NOT NULL, PRIMARY KEY (MON_ID));"
        db_act.execute(create_tab_monitor)

        create_tab_cpu = "CREATE TABLE CPU_INFO (CPU_ID INT NOT NULL AUTO_INCREMENT, CPU_NAME VARCHAR(255) NOT NULL, " \
                         "PRIMARY KEY (CPU_ID));"
        db_act.execute(create_tab_cpu)

        create_tab_hdd = "CREATE TABLE HDD_INFO (HDD_ID INT NOT NULL AUTO_INCREMENT, HDD_NAME VARCHAR(255) NOT NULL, " \
                         "HDD_SERIAL VARCHAR(255) NOT NULL, HDD_SIZE VARCHAR(255) NOT NULL, HDD_NUMBER INT NOT NULL, " \
                         "PC_ID VARCHAR(255), PRIMARY KEY (HDD_ID));"
        db_act.execute(create_tab_hdd)

        create_tab_mb = "CREATE TABLE MB_INFO (MB_ID INT NOT NULL AUTO_INCREMENT, MB_MODEL VARCHAR(255) NOT NULL, " \
                        "PRIMARY KEY (MB_ID));"
        db_act.execute(create_tab_mb)

        create_tab_bp = "CREATE TABLE BP_INFO (BP_ID INT NOT NULL AUTO_INCREMENT, BP_MODEL VARCHAR(255) NOT NULL, " \
                        "PRIMARY KEY (BP_ID));"
        db_act.execute(create_tab_bp)

        create_tab_pc = "CREATE TABLE PC_INFO (PC_ID INT NOT NULL AUTO_INCREMENT, PC_NAME VARCHAR(255) NOT NULL," \
                        "AR_ID INT NOT NULL, USER_NAME VARCHAR(255) NOT NULL, MB_SERIAL VARCHAR(255) NOT NULL" \
                        "ADR_ID INT NOT NULL, USER_PHONE VARCHAR(255) NOT NULL," \
                        "RAM_MAN_ID INT  NOT NULL, RAM_FREQ_ID INT  NOT NULL, RAM_CAP_ID INT NOT NULL, RAM_TYPE_ID " \
                        "INT NOT NULL, MON_ID INT NOT NULL, CPU_ID INT NOT NULL, HDD_ID INT NOT NULL, MB_ID INT NOT " \
                        "NULL, BP_ID INT NOT NULL, PRIMARY KEY (PC_ID), " \
                        "FOREIGN KEY (AR_ID) REFERENCES AREA_INFO(AR_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (ADR_ID) REFERENCES ADDRESS_INFO(ADR_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (RAM_MAN_ID) REFERENCES RAM_MAN_INFO(RAM_MAN_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (RAM_FREQ_ID) REFERENCES RAM_FREQ_INFO(RAM_FREQ_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (RAM_CAP_ID) REFERENCES RAM_CAP_INFO(RAM_CAP_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (RAM_TYPE_ID) REFERENCES RAM_TYPE_INFO(RAM_TYPE_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (MON_ID) REFERENCES MONITOR_INFO(MON_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (CPU_ID) REFERENCES CPU_INFO(CPU_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (HDD_ID) REFERENCES HDD_INFO(HDD_ID) ON UPDATE CASCADE, " \
                        "FOREIGN KEY (MB_ID) REFERENCES MB_INFO(MB_ID) ON UPDATE CASCADE," \
                        "FOREIGN KEY (BP_ID) REFERENCES BP_INFO(BP_ID) ON UPDATE CASCADE) CHARACTER SET = utf8 , COLLATE = utf8_general_ci;"
        db_act.execute(create_tab_pc)

        db_act.close()
    # сохранение изменений
    except Exception as e:
        print(e)
