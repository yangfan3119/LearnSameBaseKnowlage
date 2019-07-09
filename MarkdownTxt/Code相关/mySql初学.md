### $Start$：

```sh
C:\Users\admin>mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.17 MySQL Community Server (GPL)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

##### 1. mysql 查看编码方式的命名

```mysql
mysql> show variables like 'character%';
+--------------------------+----------------------------------------+
| Variable_name            | Value                                  |
+--------------------------+----------------------------------------+
| character_set_client     | gbk                                    |
| character_set_connection | gbk                                    |
| character_set_database   | utf8                                   |
| character_set_filesystem | binary                                 |
| character_set_results    | gbk                                    |
| character_set_server     | utf8                                   |
| character_set_system     | utf8                                   |
| character_sets_dir       | D:\mysql-5.7.17-winx64\share\charsets\ |
+--------------------------+----------------------------------------+
8 rows in set, 1 warning (0.00 sec)
```

##### 2. 创建指定编码格式的数据库

```mysql
mysql> CREATE DATABASE IF NOT EXISTS learn CHARACTER SET utf8;
Query OK, 1 row affected (0.00 sec)

mysql> SHOW CREATE DATABASE learn;
+----------+----------------------------------------------------------------+
| Database | Create Database                                                |
+----------+----------------------------------------------------------------+
| learn    | CREATE DATABASE `learn` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+----------+----------------------------------------------------------------+
1 row in set (0.00 sec)
```

##### 3. 删除指定数据库

```mysql
mysql> DROP DATABASE mysql_learn;
```

##### 4. 修改编码格式

```mysql
mysql> ALTER DATABASE learn CHARACTER SET = gbk;
Query OK, 1 row affected (0.00 sec)

mysql> SHOW CREATE DATABASE learn;
+----------+---------------------------------------------------------------+
| Database | Create Database                                               |
+----------+---------------------------------------------------------------+
| learn    | CREATE DATABASE `learn` /*!40100 DEFAULT CHARACTER SET gbk */ |
+----------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

##### 5. 创建表

```mysql
mysql> CREATE TABLE tb2(
 -> id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -> username VARCHAR(20) NOT NULL UNIQUE KEY,
 -> sex ENUM('男','女','保密') DEFAULT '保密',
 -> age TINYINT UNSIGNED);
Query OK, 0 rows affected (0.02 sec)
```

> UNSIGNED 					无符号型数据
> AUTO_INCREMENT       唯一自动编号+1，正数序列，可做索引
> PRIMARY KEY				主键  (默认非空、一张表只能有一个主键)
> NOT NULL					 非空
> UNIQUE KEY 				唯一键	(可为空值、一张表可以有多个唯一键)
> ENUM 						   枚举
> DEFAULT 					  默认参数

##### 6. 查询表结构

```mysql
mysql> SHOW COLUMNS FROM tb2;
+----------+------------------------+------+-----+---------+----------------+
| Field    | Type                   | Null | Key | Default | Extra          |
+----------+------------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned   | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)            | NO   | UNI | NULL    |                |
| sex      | enum('男','女','保密')  | YES  |     | 保密    |                |
| age      | tinyint(3) unsigned    | YES  |     | NULL    |                |
+----------+------------------------+------+-----+---------+----------------+
4 rows in set (0.01 sec)
```

总结：
数据类型：	整型、浮点型、字符型、日期时间型
数据表操作：如何创建数据表（PRIMARY KEY(主键约束)UNIQUE KEY(唯一约束)DEFAULT(默认约束)NOT NULL(非空约束)）、记录插入、记录查询

约束：

1. 约束保证数据的完整性和一致性

2. 约束分为表级约束和列级约束

3. 约束类型包括：

   NOT NULL		非空约束  -->  列级约束	
   PRIMARY KEY		主键约束  -->  列级约束	
   UNIQUE KEY		唯一约束  -->  列级约束	
   DEFAULT			默认约束  -->  列级约束

   FOREIGN KEY		外键约束  -->  表级约束	实现表的一对一或一对多

   > ​	外键约束的要求：
   >
   > 1. 父表和子表必须使用相同的存储引擎，而且禁止使用临时表
   > 2. 数据表的存储引擎只能为InnoDB
   > 3. 外键列和参照列必须具有相似的数据类型。其中数字的长度和是否有符号位必须相同;而字符的长度则可以不同。
   > 4. 外键列和参照列必须创建索引。如果外键列不存在索引的话，MySQL将自动创建索引。

引申：存储引擎的查询

```mysql
mysql> show engines;
# 输出下表
9 rows in set (0.00 sec)
```

| Engine             | Support | Comment                                                      | Transactions | XA   | Savepoints |
| ------------------ | ------- | ------------------------------------------------------------ | ------------ | ---- | ---------- |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys   | YES          | YES  | YES        |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                        | NO           | NO   | NO         |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables    | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                        | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                           | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                       | NO           | NO   | NO         |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                           | NO           | NO   | NO         |
| FEDERATED          | NO      | Federated MySQL storage engine                               | NULL         | NULL | NULL       |

```mysql
mysql> show variables like '%storage_engine%'
-> ;
+----------------------------------+--------+
| Variable_name                    | Value  |
+----------------------------------+--------+
| default_storage_engine           | InnoDB |
| default_tmp_storage_engine       | InnoDB |
| disabled_storage_engines         |        |
| internal_tmp_disk_storage_engine | InnoDB |
+----------------------------------+--------+
4 rows in set, 1 warning (0.01 sec)
```
##### 7. 创建一个外键

```mysql
mysql> CREATE TABLE provinces(
 -> id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 -> pname VARCHAR(20) NOT NULL);
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE users(
    -> id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -> username VARCHAR(20) UNIQUE KEY,
    -> pid SMALLINT UNSIGNED,
    -> FOREIGN KEY (pid) REFERENCES provinces(id)
    -> );
Query OK, 0 rows affected (0.01 sec)
```

##### 8. 查询外键表的创建

```mysql
mysql> SHOW CREATE TABLE users;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                                                                     |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| users | CREATE TABLE `users` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `pid` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `pid` (`pid`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `provinces` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```


物理性外键约束的参考操作：
1. CASCADE: 从父表删除或更新且自动删除或更新子表中匹配的行
2. SET NULL: 从父表删除或更新行，并设置子表中的外键列为NULL。如果使用该选项，必须保障子表咧没有指定NOT NULL
3. RESTRICT: 拒绝对父表的删除或更新操作
4. NO ACTION:标准SQL的关键字，在MySQL中与RESTRICT相同

```mysql
mysql> CREATE TABLE users1(
    -> id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -> username VARCHAR(20) NOT NULL UNIQUE KEY,
    -> pid SMALLINT UNSIGNED,
    -> FOREIGN KEY (pid) REFERENCES provinces(id) ON DELETE CASCADE);	%此处用ON DELETE
Query OK, 0 rows affected (0.02 sec)
```

##### 9. 常用语句实例：

- 父表中的数据:

```mysql
mysql> select * from provinces;
		+----+-------+
		| id | pname |
		+----+-------+
		|  1 | A     |
		|  2 | B     |
		|  3 | C     |
		+----+-------+
		3 rows in set (0.00 sec)
```

- 子表中的数据：

```mysql
mysql> SELECT * FROM users1;
		+----+----------+------+
		| id | username | pid  |
		+----+----------+------+
		|  1 | tom      |    3 |
		|  3 | Ann      |    1 |
		|  4 | John     |    2 |
		+----+----------+------+
		3 rows in set (0.00 sec)
```

- 当对父表进行删除操作时则有：

```mysql
mysql> DELETE FROM provinces WHERE id=2;
		Query OK, 1 row affected (0.01 sec)
```

- 删除后的父表数据：

```mysql
mysql> select * from provinces;
		+----+-------+
		| id | pname |
		+----+-------+
		|  1 | A     |
		|  3 | C     |
		+----+-------+
	2 rows in set (0.00 sec)
```

- 删除后的子表数据：

```mysql
mysql> select * from users1;
		+----+----------+------+
		| id | username | pid  |
		+----+----------+------+
		|  1 | tom      |    3 |
		|  3 | Ann      |    1 |
		+----+----------+------+
		2 rows in set (0.00 sec)
```

- 数据表修改：

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)          | NO   | UNI | NULL    |                |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |                |
+----------+----------------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```

- 列的添加：

```mysql
mysql> ALTER TABLE users1 ADD sex ENUM('男','女','保密') DEFAULT '保密' AFTER username;
Query OK, 0 rows affected (0.08 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+------------------------+------+-----+---------+----------------+
| Field    | Type                   | Null | Key | Default | Extra          |
+----------+------------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned   | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)            | NO   | UNI | NULL    |                |
| sex      | enum('男','女','保密') | YES  |     | 保密    |                |
| pid      | smallint(5) unsigned   | YES  | MUL | NULL    |                |
| age      | smallint(5) unsigned   | YES  |     | 10      |                |	//未标注添加位置，默认为最后一个
+----------+------------------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)
```

- 列的删除

```mysql
mysql> ALTER TABLE users1 DROP age,DROP sex;
Query OK, 0 rows affected (0.08 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)          | NO   | UNI | NULL    |                |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |                |
+----------+----------------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```

- 默认约束的添加/删除

```mysql
mysql> ALTER TABLE users1 ALTER age SET DEFAULT 12;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)          | NO   | UNI | NULL    |                |
| age      | smallint(5) unsigned | YES  |     | 12      |                |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |                |
+----------+----------------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)
```

```mysql
mysql> ALTER TABLE users1 ALTER age DROP DEFAULT;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)          | NO   | UNI | NULL    |                |
| age      | smallint(5) unsigned | YES  |     | NULL    |                |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |                |
+----------+----------------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)
```

- 添加主键和唯一键

```mysql
mysql> ALTER TABLE users1 ADD UNIQUE (id);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

- 删除主键约束

```mysql
# 因为有AUTO_INCREMENT属性，所以先修改列属性，去掉这个
mysql> ALTER TABLE users1 CHANGE id id SMALLINT UNSIGNED;
Query OK, 2 rows affected (0.03 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+-------+
| Field    | Type                 | Null | Key | Default | Extra |
+----------+----------------------+------+-----+---------+-------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    |       |
| username | varchar(20)          | NO   | UNI | NULL    |       |
| age      | smallint(5) unsigned | YES  |     | NULL    |       |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |       |
+----------+----------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

- 再执行删除主键的约束

```mysql
mysql> ALTER TABLE users1 DROP PRIMARY KEY;
Query OK, 2 rows affected (0.04 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+-------+
| Field    | Type                 | Null | Key | Default | Extra |
+----------+----------------------+------+-----+---------+-------+
| id       | smallint(5) unsigned | NO   |     | NULL    |       |
| username | varchar(20)          | NO   | PRI | NULL    |       |
| age      | smallint(5) unsigned | YES  |     | NULL    |       |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |       |
+----------+----------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

- 删除唯一键的约束

```mysql
mysql> ALTER TABLE users1 DROP INDEX id;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

- 修改列定义

```mysql
# CHANGE 和 MODIFY 的应用
mysql> ALTER TABLE users1 CHANGE id id SMALLINT UNSIGNED AFTER username;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

```mysql
mysql> SHOW COLUMNS FROM users1;
+----------+----------------------+------+-----+---------+-------+
| Field    | Type                 | Null | Key | Default | Extra |
+----------+----------------------+------+-----+---------+-------+
| username | varchar(20)          | NO   | PRI | NULL    |       |
| id       | smallint(5) unsigned | YES  |     | NULL    |       |
| age      | smallint(5) unsigned | YES  |     | NULL    |       |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |       |
+----------+----------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)

mysql> ALTER TABLE users1 MODIFY id SMALLINT UNSIGNED FIRST;
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### 一、子查询与连接

#### 1. 子查询

**在条件语句中增加子查询，需要用(SELECT) 语句扩起来。**

```mysql
mysql> SELECT goods_name,goods_price FROM tdb_goods WHERE goods_price > (SELECT ROUND(AVG(goods_price),2) FROM tdb_goods) GROUP BY goods_price DESC;
+----------------------------------+-------------+
| goods_name                       | goods_price |
+----------------------------------+-------------+
| Mac Pro MD878CH/A 专业级台式电脑 |   28888.000 |
| iMac ME086CH/A 21.5英寸一体电脑  |    9188.000 |
| G150TH 15.6英寸游戏本            |    8499.000 |
| SVP13226SCB 13.3英寸触控超极本   |    7999.000 |
|  HMZ-T3W 头戴显示设备            |    6999.000 |
| X3250 M4机架式服务器 2583i14     |    6888.000 |
+----------------------------------+-------------+
```





2. 查询商品id、name、price列，按价格降序排列，条件是价格大于超级本所有和部分
mysql> SELECT goods_id,goods_name,goods_price FROM tdb_goods
    -> WHERE goods_price > SOME(SELECT goods_price FROM tdb_goods WHERE goods_cate = '超级本')
    -> ORDER BY goods_price DESC;
+----------+----------------------------------+-------------+
| goods_id | goods_name                       | goods_price |
+----------+----------------------------------+-------------+
|       17 | Mac Pro MD878CH/A 专业级台式电脑 |   28888.000 |
|       13 | iMac ME086CH/A 21.5英寸一体电脑  |    9188.000 |
|        3 | G150TH 15.6英寸游戏本            |    8499.000 |
|        7 | SVP13226SCB 13.3英寸触控超极本   |    7999.000 |
|       18 |  HMZ-T3W 头戴显示设备            |    6999.000 |
|       21 |  HMZ-T3W 头戴显示设备            |    6999.000 |
|       20 | X3250 M4机架式服务器 2583i14     |    6888.000 |
|       16 | PowerEdge T110 II服务器          |    5388.000 |
|        5 | X240(20ALA0EYCD) 12.5英寸超极本  |    4999.000 |
|        2 | Y400N 14.0英寸笔记本电脑         |    4899.000 |
+----------+----------------------------------+-------------+
10 rows in set (0.00 sec)

mysql> SELECT goods_id,goods_name,goods_price FROM tdb_goods
    ->
    -> WHERE goods_price > ALL(SELECT goods_price FROM tdb_goods WHERE goods_cate = '超级本')
    -> ORDER BY goods_price DESC;
+----------+----------------------------------+-------------+
| goods_id | goods_name                       | goods_price |
+----------+----------------------------------+-------------+
|       17 | Mac Pro MD878CH/A 专业级台式电脑 |   28888.000 |
|       13 | iMac ME086CH/A 21.5英寸一体电脑  |    9188.000 |
|        3 | G150TH 15.6英寸游戏本            |    8499.000 |
+----------+----------------------------------+-------------+
3 rows in set (0.00 sec)

3. 创建内连接，更新tdb_goods表中goods_cate的值，INNER JOIN tdb_goods_cates表，对ON goods_cate = cate_id条件下的改为SET goods_cate = cate_name;
mysql> UPDATE tdb_goods INNER JOIN tdb_goods_cates ON goods_cate = cate_id SET goods_cate = cate_name;
Query OK, 22 rows affected (0.00 sec)
Rows matched: 22  Changed: 22  Warnings: 0

4. 内连接查询---多表查询
mysql> SELECT goods_id,goods_name,cate_name,brand_name,goods_price FROM tdb_goods AS a
    -> INNER JOIN tdb_goods_cates AS b ON a.cate_id = b.cate_id
    -> ORDER BY goods_price DESC;
+----------+------------------------------------------------------------------------+---------------+------------+-------------+
| goods_id | goods_name                                                             | cate_name     | brand_name | goods_price |
+----------+------------------------------------------------------------------------+---------------+------------+-------------+
|       17 | Mac Pro MD878CH/A 专业级台式电脑                                       | 服务器/工作站 | 苹果       |   28888.000 |
|       13 | iMac ME086CH/A 21.5英寸一体电脑                                        | 台式机        | 苹果       |    9188.000 |
|        3 | G150TH 15.6英寸游戏本                                                  | 游戏本        | 雷神       |    8499.000 |
|        7 | SVP13226SCB 13.3英寸触控超极本                                         | 超级本        | 索尼       |    7999.000 |
|       18 |  HMZ-T3W 头戴显示设备                                                  | 笔记本配件    | 索尼       |    6999.000 |
|       21 |  HMZ-T3W 头戴显示设备                                                  | 笔记本配件    | 索尼       |    6999.000 |
|       20 | X3250 M4机架式服务器 2583i14                                           | 服务器/工作站 | IBM        |    6888.000 |
|       16 | PowerEdge T110 II服务器                                                | 服务器/工作站 | 戴尔       |    5388.000 |
|        5 | X240(20ALA0EYCD) 12.5英寸超极本                                        | 超级本        | 联想       |    4999.000 |
|        2 | Y400N 14.0英寸笔记本电脑                                               | 笔记本        | 联想       |    4899.000 |
|        6 | U330P 13.3英寸超极本                                                   | 超级本        | 联想       |    4299.000 |
|       15 | Z220SFF F4F06PA工作站                                                  | 服务器/工作站 | 惠普       |    4288.000 |
|       14 | AT7-7414LP 台式电脑 （i5-3450四核 4G 500G 2G独显 DVD 键鼠 Linux ）     | 台式机        | 宏碁       |    3699.000 |
|       11 | IdeaCentre C340 20英寸一体电脑                                         | 台式机        | 联想       |    3499.000 |
|        1 | R510VC 15.6英寸笔记本                                                  | 笔记本        | 华硕       |    3399.000 |
|        9 | iPad Air MD788CH/A 9.7英寸平板电脑 （16G WiFi版）                      | 平板电脑      | 苹果       |    3388.000 |
|       12 | Vostro 3800-R1206 台式电脑                                             | 台式机        | 戴尔       |    2899.000 |
|        4 | X550CC 15.6英寸笔记本                                                  | 笔记本        | 华硕       |    2799.000 |
|       10 |  iPad mini ME279CH/A 配备 Retina 显示屏 7.9英寸平板电脑 （16G WiFi版） | 平板电脑      | 苹果       |    2788.000 |
|        8 | iPad mini MD531CH/A 7.9英寸平板电脑                                    | 平板电脑      | 苹果       |    1998.000 |
|       19 | 商务双肩背包                                                           | 笔记本配件    | 索尼       |      99.000 |
|       22 | 商务双肩背包                                                           | 笔记本配件    | 索尼       |      99.000 |
+----------+------------------------------------------------------------------------+---------------+------------+-------------+
22 rows in set (0.00 sec)

第六章 函数与运算符
CONCAT_WS -- 用指定的字符连接字符串
mysql> SELECT CONCAT_WS(' ','YANG','FAN','PAN','BAO','PING');
+------------------------------------------------+
| CONCAT_WS(' ','YANG','FAN','PAN','BAO','PING') |
+------------------------------------------------+
| YANG FAN PAN BAO PING                          |
+------------------------------------------------+
1 row in set (0.00 sec)
FORMAT -- 格式化
mysql> SELECT FORMAT(12560.753621,2);
+------------------------+
| FORMAT(12560.753621,2) |
+------------------------+
| 12,560.75              |
+------------------------+
1 row in set (0.00 sec)
	也可以四舍五入
mysql> SELECT FORMAT(12560.756621,2);
+------------------------+
| FORMAT(12560.756621,2) |
+------------------------+
| 12,560.76              |
+------------------------+
1 row in set (0.00 sec)
LOWER -- 全改小写
mysql> SELECT LOWER('SDFAS');
+----------------+
| LOWER('SDFAS') |
+----------------+
| sdfas          |
+----------------+
1 row in set (0.00 sec)
UPPER -- 全改大写
mysql> SELECT UPPER('sdfwsdfe');
+-------------------+
| UPPER('sdfwsdfe') |
+-------------------+
| SDFWSDFE          |
+-------------------+
1 row in set (0.00 sec)
LEFT -- 取左侧指定位数的字符
mysql> SELECT LEFT('Yangfan',4);
+-------------------+
| LEFT('Yangfan',4) |
+-------------------+
| Yang              |
+-------------------+
1 row in set (0.00 sec)
RIGHT -- 取右侧指定位数的字符，从后往前数
mysql> SELECT RIGHT('Yangfan',4);
+--------------------+
| RIGHT('Yangfan',4) |
+--------------------+
| gfan               |
+--------------------+
1 row in set (0.00 sec)

例：
mysql> UPDATE tdb_test_six SET final_str = CONCAT_WS('_',LENGTH(test_str),REPLACE(REPLACE(REPLACE(REPLACE(test_str,'?',''),'_',''),'X',''),'!!',''));
Query OK, 4 rows affected (0.01 sec)
Rows matched: 4  Changed: 4  Warnings: 0

mysql>
mysql> SELECT * FROM tdb_test_six;
+---------+------------------------+-----------+
| test_id | test_str               | final_str |
+---------+------------------------+-----------+
|       1 | ??one??11              | 9_one11   |
|       2 | __???two__??11         | 14_two11  |
|       3 | XX__???twoXX__??11     | 18_two11  |
|       4 | !!XX__???two!!XX__??11 | 22_two11  |
+---------+------------------------+-----------+
4 rows in set (0.00 sec)

TRUNCATE 数值截取
mysql> SELECT TRUNCATE(123456.789,-5);
+-------------------------+
| TRUNCATE(123456.789,-5) |
+-------------------------+
|                  100000 |
+-------------------------+
1 row in set (0.00 sec)

POWER 求幂
mysql> SELECT POWER(3,10);
+-------------+
| POWER(3,10) |
+-------------+
|       59049 |
+-------------+
1 row in set (0.00 sec)
CEIL 进位截取
mysql> SELECT CEIL(12.123);
+--------------+
| CEIL(12.123) |
+--------------+
|           13 |
+--------------+
1 row in set (0.00 sec)
FLOOR 退位截取
mysql> SELECT FLOOR(12.123);
+---------------+
| FLOOR(12.123) |
+---------------+
|            12 |
+---------------+
1 row in set (0.00 sec)
ROUND 四舍五入
mysql> SELECT ROUND(12.123);
+---------------+
| ROUND(12.123) |
+---------------+
|            12 |
+---------------+
1 row in set (0.00 sec)
DATEDIFF 计算时间间隔的天数
mysql> SELECT DATEDIFF('2016-5-10','2013-2-4');
+----------------------------------+
| DATEDIFF('2016-5-10','2013-2-4') |
+----------------------------------+
|                             1191 |
+----------------------------------+
1 row in set (0.00 sec)
DATE_FORMAT 更改日期格式 此处注意M-月份 D-天数 的大小写问题
mysql> SELECT DATE_FORMAT('2017-6-2','%Y/%M/%D');
+------------------------------------+
| DATE_FORMAT('2017-6-2','%Y/%M/%D') |
+------------------------------------+
| 2017/June/2nd                      |
+------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT DATE_FORMAT('2017-6-2','%Y/%m/%d');
+------------------------------------+
| DATE_FORMAT('2017-6-2','%Y/%m/%d') |
+------------------------------------+
| 2017/06/02                         |
+------------------------------------+
1 row in set (0.00 sec)

以下为相关信息函数：	CONNECTION_ID 连接ID；
						DATABASE 当前操作数据库；
						USER当前操作用户；
						LAST_INSERT_ID最后一次插入的ID，必须含有AUTO_INCREMENT的字段；
						VERSION当前数据库的版本号。
mysql> SELECT CONNECTION_ID();
+-----------------+
| CONNECTION_ID() |
+-----------------+
|               3 |
+-----------------+
1 row in set (0.00 sec)

mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| learn      |
+------------+
1 row in set (0.00 sec)

mysql> SELECT USER();
+----------------+
| USER()         |
+----------------+
| root@localhost |
+----------------+
1 row in set (0.00 sec)

mysql> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                4 |
+------------------+
1 row in set (0.00 sec)

mysql> SELECT VERSION();
+-----------+
| VERSION() |
+-----------+
| 5.7.17    |
+-----------+
1 row in set (0.00 sec)

聚合函数：
AVG() 	平均值
COUNT()	计数
MAX()	最大值
MIN()	最小值
SUM()	求和

第七章：自定义函数
创建f1函数，用于日期的模式转换
mysql> CREATE FUNCTION f1() RETURNS VARCHAR(30)
    -> RETURN DATE_FORMAT(NOW(),'%Y年%m月%d日 %H点:%i分:%s秒');
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT f1();
+-------------------------------+
| f1()                          |
+-------------------------------+
| 2017年06月03日 10点:47分:13秒 |
+-------------------------------+
1 row in set (0.00 sec)
创建f2函数，用于求两个数的平均值
mysql> CREATE FUNCTION f2(a SMALLINT UNSIGNED,b SMALLINT UNSIGNED)
    -> RETURNS FLOAT(10,2) UNSIGNED
    -> RETURN (a+b)/2;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT f2(15,5);
+----------+
| f2(15,5) |
+----------+
|    10.00 |
+----------+
1 row in set (0.00 sec)
函数参数异常会报错。类型异常会强制转换，此处按四舍五入计算浮点型到SMALLINT型的转换
mysql> SELECT f2(15,);
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ')' at line 1
mysql> SELECT f2(15);
ERROR 1318 (42000): Incorrect number of arguments for FUNCTION learn.f2; expected 2, got 1
mysql> SELECT f2(15,2.5);
+------------+
| f2(15,2.5) |
+------------+
|       9.00 |
+------------+
1 row in set (0.00 sec)

创建一个函数自动插入表数据：属于复合结构函数
1. 查看表结构
mysql> DESC users;
+----------+----------------------+------+-----+---------+----------------+
| Field    | Type                 | Null | Key | Default | Extra          |
+----------+----------------------+------+-----+---------+----------------+
| id       | smallint(5) unsigned | NO   | PRI | NULL    | auto_increment |
| username | varchar(20)          | YES  | UNI | NULL    |                |
| pid      | smallint(5) unsigned | YES  | MUL | NULL    |                |
+----------+----------------------+------+-----+---------+----------------+
3 rows in set (0.01 sec)
2. 因函数中的SQL语句以;结束并执行，此处写函数主体时，最好先修改结束符号如下:
mysql> DELIMITER //
mysql> SELECT f1();
    -> //
+-------------------------------+
| f1()                          |
+-------------------------------+
| 2017年06月03日 11点:00分:45秒 |
+-------------------------------+
1 row in set (0.00 sec)
3. 更改后开始写程序主体：依然程序主体需要有return,否则报错
mysql> CREATE FUNCTION f3(uname VARCHAR(20))
    -> RETURNS INT
    -> BEGIN
    -> INSERT users(username) VALUES(uname);
    -> LAST_INSERT_ID();
    -> END//
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '();
END' at line 5
mysql> CREATE FUNCTION f3(uname VARCHAR(20))
    -> RETURNS INT UNSIGNED
    -> BEGIN
    -> INSERT users(username) VALUES(uname);
    -> RETURN LAST_INSERT_ID();
    -> END//
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM users;
    -> //
Empty set (0.00 sec)

mysql> DELIMITER ;
mysql> SELECT * FROM users;
Empty set (0.00 sec)
4. 可以成功实现需求功能。
mysql> SELECT f3(johe);
ERROR 1054 (42S22): Unknown column 'johe' in 'field list'

mysql> SELECT f3('johe');
+------------+
| f3('johe') |
+------------+
|          1 |
+------------+
1 row in set (0.01 sec)

mysql> SELECT f3('jo');
+----------+
| f3('jo') |
+----------+
|        2 |
+----------+
1 row in set (0.01 sec)

mysql> SELECT f3('hehe');
+------------+
| f3('hehe') |
+------------+
|          3 |
+------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+------+
| id | username | pid  |
+----+----------+------+
|  1 | johe     | NULL |
|  2 | jo       | NULL |
|  3 | hehe     | NULL |
+----+----------+------+
3 rows in set (0.00 sec)

创建一个存储过程：
mysql> DELIMITER //
mysql> CREATE PROCEDURE CleanPassword(IN psw VARCHAR(40),OUT chrows INT UNSIGNED)
    -> BEGIN
    -> UPDATE users SET password = psw;
    -> SELECT ROW_COUNT() INTO chrows;
    -> END
    -> //
Query OK, 0 rows affected (0.00 sec)

mysql> CALL CleanPassword('123',@Ch);
    -> //
Query OK, 1 row affected (0.00 sec)

mysql> SELECT @Ch;
    -> //
+------+
| @Ch  |
+------+
|   16 |
+------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
    -> //
+----+----------+----------+------+
| id | username | password | pid  |
+----+----------+----------+------+
|  2 | jo       | 123      | NULL |
|  3 | hehe     | 123      | NULL |
|  4 | tt       | 123      | NULL |
|  5 | bb       | 123      | NULL |
|  6 | aa       | 123      | NULL |
| 18 | A        | 123      | NULL |
| 19 | B        | 123      | NULL |
| 20 | C        | 123      | NULL |
| 21 | D        | 123      | NULL |
| 22 | E        | 123      | NULL |
| 23 | F        | 123      | NULL |
| 24 | G        | 123      | NULL |
| 25 | H        | 123      | NULL |
| 26 | I        | 123      | NULL |
| 27 | J        | 123      | NULL |
| 28 | K        | 123      | NULL |
+----+----------+----------+------+
16 rows in set (0.00 sec)

函数和存储过程：可以交替使用

存储过程中使用函数：
mysql> CREATE PROCEDURE Addtime(OUT rows INT UNSIGNED,OUT len INT UNSIGNED)
    -> BEGIN
    -> UPDATE users SET data = f1();
    -> SELECT ROW_COUNT() INTO rows;
    -> SELECT COUNT(id) FROM users INTO len;
    -> END
    -> //
Query OK, 0 rows affected (0.00 sec)

mysql> CALL Addtime(@Ch,@len);
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM users;
+----+----------+----------+------+-------------------------------+
| id | username | password | pid  | data                          |
+----+----------+----------+------+-------------------------------+
|  2 | jo       | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
|  3 | hehe     | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
|  4 | tt       | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
|  5 | bb       | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
|  6 | aa       | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 18 | A        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 19 | B        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 20 | C        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 21 | D        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 22 | E        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 23 | F        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 24 | G        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 25 | H        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 26 | I        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 27 | J        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
| 28 | K        | 123      | NULL | 2017年06月05日 15点:50分:01秒 |
+----+----------+----------+------+-------------------------------+
16 rows in set (0.00 sec)

函数中使用存储过程：
mysql> CREATE FUNCTION f4() RETURNS INT UNSIGNED
    -> BEGIN
    -> CALL Addtime(@Ch,@len);
    -> RETURN (SELECT COUNT(id) FROM users);
    -> END
    -> //
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT f4();
    -> //
+------+
| f4() |
+------+
|   16 |
+------+
1 row in set (0.00 sec)

mysql> SELECT @Ch,@len;
    -> //
+------+------+
| @Ch  | @len |
+------+------+
|   16 |   16 |
+------+------+
连接多个参数结果的用法可以用CONCAT_WS 或者CONCAT
mysql> CREATE FUNCTION f5() RETURNS VARCHAR(20)
    -> RETURN (SELECT CONCAT((SELECT COUNT(id) FROM users),'---',@Ch,' ',@len,''))//
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT f5()//
+------------+
| f5()       |
+------------+
| 16---16 16 |
+------------+
1 row in set (0.00 sec)


​	