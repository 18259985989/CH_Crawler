/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.68
Source Server Version : 50726
Source Host           : 192.168.1.68:3306
Source Database       : dataggregate

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2020-03-04 11:41:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for abnormal
-- ----------------------------
DROP TABLE IF EXISTS `abnormal`;
CREATE TABLE `abnormal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `put_date` datetime DEFAULT NULL,
  `put_reason` varchar(100) DEFAULT NULL,
  `put_department` varchar(50) DEFAULT NULL,
  `remove_date` datetime DEFAULT NULL,
  `remove_reason` text,
  `remove_department` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=26526 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for base_info
-- ----------------------------
DROP TABLE IF EXISTS `base_info`;
CREATE TABLE `base_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Enterprise_name` varchar(120) NOT NULL COMMENT '企业名称',
  `Enterprise_tyshxydm` varchar(32) DEFAULT NULL COMMENT '社会统一代码',
  `Legalrepresentative` varchar(120) DEFAULT NULL COMMENT '法人',
  `Enterprise_zzjgdm` varchar(32) DEFAULT NULL COMMENT '组织机构代码',
  `Enterprise_gszch` varchar(32) DEFAULT NULL COMMENT '工商注册号',
  `rtime` datetime DEFAULT NULL COMMENT '成立时间',
  `registered_address` varchar(255) DEFAULT NULL COMMENT '注册地址',
  `gslx` varchar(64) DEFAULT NULL COMMENT '企业类型',
  `jyzt` varchar(32) DEFAULT NULL COMMENT '经营状态',
  `op_from` datetime DEFAULT NULL COMMENT '经营起始',
  `op_to` datetime DEFAULT NULL COMMENT '经营至',
  `approval_date` datetime DEFAULT NULL COMMENT '核准日期',
  `djjg` varchar(126) DEFAULT NULL COMMENT '登记机关',
  `f_body` longtext COMMENT '经营范围',
  `cancel_date` datetime DEFAULT NULL COMMENT '注销原因',
  `reasons_cancel` longtext COMMENT '取消原因',
  `zczb` varchar(32) DEFAULT NULL COMMENT '注册资本',
  `paid_in_capital` varchar(32) DEFAULT '' COMMENT '实缴资本',
  `ygrs` varchar(32) DEFAULT NULL COMMENT '企业人数',
  `social_staff_num` varchar(32) DEFAULT NULL COMMENT '参保人数',
  `industry` varchar(32) DEFAULT NULL COMMENT '行业',
  `Contact_number` varchar(64) DEFAULT NULL COMMENT '联系电话',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `z_body` longtext COMMENT '企业简介',
  `source_update_time` datetime DEFAULT NULL,
  `local_update_time` datetime DEFAULT NULL,
  `score` varchar(64) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131140 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for bid_info
-- ----------------------------
DROP TABLE IF EXISTS `bid_info`;
CREATE TABLE `bid_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `title` text,
  `publish_date` datetime DEFAULT NULL,
  `purchaser` varchar(255) DEFAULT NULL,
  `proxy` varchar(100) DEFAULT NULL,
  `content` longtext,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1405917 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for branch
-- ----------------------------
DROP TABLE IF EXISTS `branch`;
CREATE TABLE `branch` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `branch_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '分支机构名称',
  `credit_code` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '社会统一代码',
  `Enterprise_gszch` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '工商注册号',
  `reg_authority` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '登记机关',
  `legal_person` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '法人',
  `industry` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '行业',
  `estiblish_date` datetime DEFAULT NULL COMMENT '成立时间',
  `business_state` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '经营状态',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=28501 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for change_info
-- ----------------------------
DROP TABLE IF EXISTS `change_info`;
CREATE TABLE `change_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `change_item` text COMMENT '变更项目',
  `before_change` text COMMENT '变更前',
  `after_change` text COMMENT '变更后',
  `change_date` datetime DEFAULT NULL COMMENT '变更时间',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=245912 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for check_info
-- ----------------------------
DROP TABLE IF EXISTS `check_info`;
CREATE TABLE `check_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `check_authority` varchar(64) DEFAULT NULL COMMENT '检查实施机关',
  `check_date` datetime DEFAULT NULL COMMENT '日期',
  `check_result` text COMMENT '结果',
  `check_type` varchar(64) DEFAULT NULL COMMENT '检查类型',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10470 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for company_mortgage
-- ----------------------------
DROP TABLE IF EXISTS `company_mortgage`;
CREATE TABLE `company_mortgage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `mortgage_name` varchar(64) DEFAULT NULL COMMENT '抵押人名称',
  `licence_type` varchar(64) DEFAULT NULL COMMENT '抵押人证件类型',
  `identify_number` varchar(64) DEFAULT NULL COMMENT '抵押人证件号',
  `mortgage_type` varchar(62) DEFAULT NULL COMMENT '抵押人类型',
  `address` varchar(255) DEFAULT NULL COMMENT '抵押人住址',
  `reg_number` varchar(50) DEFAULT NULL,
  `reg_date` datetime DEFAULT NULL,
  `reg_authority` varchar(50) DEFAULT NULL,
  `guaranteed_amount` varchar(50) DEFAULT NULL,
  `public_date` varchar(25) DEFAULT NULL,
  `currency` varchar(25) DEFAULT NULL,
  `cancel_date` varchar(25) DEFAULT NULL,
  `cancel_authority` varchar(255) DEFAULT NULL,
  `cancel_reason` varchar(80) DEFAULT NULL,
  `warrant_type` varchar(25) DEFAULT NULL,
  `term` varchar(25) DEFAULT NULL,
  `scope` varchar(255) DEFAULT NULL,
  `status` varchar(28) DEFAULT NULL COMMENT '状态',
  `note` text,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1229 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for company_mortgage_change
-- ----------------------------
DROP TABLE IF EXISTS `company_mortgage_change`;
CREATE TABLE `company_mortgage_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reg_id` varchar(32) DEFAULT NULL,
  `change_date` datetime DEFAULT NULL COMMENT '变更日期',
  `change_content` text COMMENT '变更内容',
  PRIMARY KEY (`id`),
  KEY `reg_id` (`reg_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for company_mortgage_collateral
-- ----------------------------
DROP TABLE IF EXISTS `company_mortgage_collateral`;
CREATE TABLE `company_mortgage_collateral` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reg_id` varchar(32) DEFAULT NULL,
  `collateral` varchar(255) DEFAULT NULL COMMENT '抵押物名称',
  `belong` varchar(120) DEFAULT NULL COMMENT '所有权或者使用权归属',
  `summary` longtext COMMENT '数量、状况等概况',
  PRIMARY KEY (`id`),
  KEY `reg_id` (`reg_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=24479 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for company_mortgage_pledgee
-- ----------------------------
DROP TABLE IF EXISTS `company_mortgage_pledgee`;
CREATE TABLE `company_mortgage_pledgee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reg_id` varchar(32) DEFAULT NULL,
  `people_name` varchar(64) DEFAULT NULL COMMENT '抵押权人名称',
  `licence_type` varchar(32) DEFAULT NULL COMMENT '抵押权人证件类型',
  `identify_number` varchar(32) DEFAULT NULL COMMENT '证件号',
  `address` varchar(255) DEFAULT NULL COMMENT '住所地',
  PRIMARY KEY (`id`),
  KEY `reg_id` (`reg_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1219 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for copyright_software
-- ----------------------------
DROP TABLE IF EXISTS `copyright_software`;
CREATE TABLE `copyright_software` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `software_name` varchar(162) DEFAULT NULL COMMENT '软件名称',
  `reg_number` varchar(32) DEFAULT NULL COMMENT '登记号',
  `work_type` varchar(32) DEFAULT NULL COMMENT '作品类别',
  `finish_date` varchar(32) DEFAULT NULL COMMENT '创作完成日期',
  `publish_date` datetime DEFAULT NULL COMMENT '首次发表日期',
  `reg_date` datetime DEFAULT NULL COMMENT '登记批准日期',
  `simple_name` varchar(162) DEFAULT NULL COMMENT '软件简称',
  `cat_number` varchar(64) DEFAULT NULL COMMENT '分类号',
  `version` varchar(24) DEFAULT NULL COMMENT '版本号',
  `author` text COMMENT '著作权人',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6368 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for copyright_work
-- ----------------------------
DROP TABLE IF EXISTS `copyright_work`;
CREATE TABLE `copyright_work` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `work_name` varchar(255) DEFAULT NULL,
  `reg_number` varchar(255) DEFAULT NULL,
  `work_type` varchar(255) DEFAULT NULL,
  `finish_date` datetime DEFAULT NULL,
  `publish_date` datetime DEFAULT NULL,
  `reg_date` datetime DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1046 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for court_auto
-- ----------------------------
DROP TABLE IF EXISTS `court_auto`;
CREATE TABLE `court_auto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `start_date` varchar(50) DEFAULT NULL COMMENT '开庭日期',
  `case_reason` text COMMENT '案由',
  `case_number` varchar(255) DEFAULT NULL COMMENT '案号',
  `litigant` text COMMENT '当事人',
  `plaintiff` text COMMENT '原告',
  `defendant` text COMMENT '被告',
  `court` varchar(255) DEFAULT NULL COMMENT '法院',
  `courtroom` varchar(255) DEFAULT NULL COMMENT '法庭',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=45827 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for court_notice
-- ----------------------------
DROP TABLE IF EXISTS `court_notice`;
CREATE TABLE `court_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `litigant` text COMMENT '当事人',
  `announce_type` longtext COMMENT '公告类型',
  `publish_date` datetime DEFAULT NULL COMMENT '公告日期',
  `publish_page` varchar(32) DEFAULT NULL COMMENT '刊登版面',
  `appellant` varchar(126) DEFAULT NULL COMMENT '上述方',
  `court` varchar(32) DEFAULT NULL COMMENT '法院',
  `content` longtext COMMENT '公告内容',
  `province` varchar(32) DEFAULT NULL COMMENT '省份',
  `announce_num` varchar(64) DEFAULT NULL COMMENT '公告号',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11456 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for dishonest_info
-- ----------------------------
DROP TABLE IF EXISTS `dishonest_info`;
CREATE TABLE `dishonest_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `ent_name` varchar(120) DEFAULT NULL COMMENT '公司名称',
  `card_number` varchar(32) DEFAULT NULL COMMENT '组织机构代码/身份证号',
  `area` varchar(64) DEFAULT NULL COMMENT '地区',
  `reg_date` datetime DEFAULT NULL COMMENT '立案时间',
  `publish_date` datetime DEFAULT NULL COMMENT '发布时间',
  `gist_unit` varchar(64) DEFAULT NULL COMMENT '执行依据单位',
  `court` varchar(64) DEFAULT NULL COMMENT '执行法院',
  `gist_num` varchar(86) DEFAULT NULL COMMENT '执行依据文号',
  `case_code` varchar(32) DEFAULT NULL COMMENT '案号',
  `duty` text COMMENT '法律生效文书确定的义务',
  `performance` text COMMENT '被执行人的履行情况',
  `disrupttype_name` text COMMENT '失信被执行人行为具体情形',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1877 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for equity_change
-- ----------------------------
DROP TABLE IF EXISTS `equity_change`;
CREATE TABLE `equity_change` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `shareholder` varchar(32) DEFAULT NULL COMMENT '股东',
  `alt_date` varchar(24) DEFAULT NULL COMMENT '股权变更日期',
  `trans_before` varchar(24) DEFAULT NULL COMMENT '变更前股权比例',
  `trans_after` varchar(24) DEFAULT NULL COMMENT '变更后股权比例',
  `publish_date` varchar(32) DEFAULT NULL COMMENT '公示日期',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for equity_pledge
-- ----------------------------
DROP TABLE IF EXISTS `equity_pledge`;
CREATE TABLE `equity_pledge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `reg_number` varchar(50) DEFAULT NULL,
  `reg_date` varchar(25) DEFAULT NULL,
  `pledgor` varchar(100) DEFAULT NULL,
  `pledge_equity` varchar(25) DEFAULT NULL,
  `pledgee` varchar(100) DEFAULT NULL,
  `pledgee_type` varchar(25) DEFAULT NULL,
  `state` varchar(25) DEFAULT NULL,
  `currency` varchar(25) DEFAULT NULL,
  `cancel_date` varchar(25) DEFAULT NULL,
  `cancel_reason` varchar(50) DEFAULT NULL,
  `certif_number_gor` varchar(50) DEFAULT NULL,
  `certif_number_gee` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3701 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for illegal_info
-- ----------------------------
DROP TABLE IF EXISTS `illegal_info`;
CREATE TABLE `illegal_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `put_date` datetime DEFAULT NULL COMMENT '列入日期',
  `put_reason` text COMMENT '列入原因',
  `put_department` varchar(64) DEFAULT NULL COMMENT '作出决定机关（列出）',
  `remove_date` datetime DEFAULT NULL COMMENT '移除日期',
  `remove_reason` text COMMENT '移除原因',
  `remove_department` varchar(64) DEFAULT NULL COMMENT '移除机关',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=757 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for im_export_base
-- ----------------------------
DROP TABLE IF EXISTS `im_export_base`;
CREATE TABLE `im_export_base` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `crcode` varchar(64) DEFAULT NULL COMMENT '海关注册编码',
  `record_date` datetime DEFAULT NULL COMMENT '注册日期',
  `customs_registered_address` varchar(64) DEFAULT NULL COMMENT '注册海关',
  `administrative_division` varchar(128) DEFAULT NULL COMMENT '行政区划',
  `economic_division` varchar(64) DEFAULT NULL COMMENT '经济区划',
  `management_category` varchar(64) DEFAULT NULL COMMENT '经营类别',
  `special_trade_area` varchar(64) DEFAULT NULL COMMENT '特殊贸易区域',
  `industry_category` varchar(64) DEFAULT NULL COMMENT '行业种类',
  `validity_date` datetime DEFAULT NULL COMMENT '报关有效时间',
  `status` varchar(64) DEFAULT NULL COMMENT '海关注销标识',
  `annual_report` varchar(64) DEFAULT NULL COMMENT '年报情况',
  `types` varchar(255) DEFAULT NULL COMMENT '跨境贸易电子商务类型',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1759 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for im_export_credit
-- ----------------------------
DROP TABLE IF EXISTS `im_export_credit`;
CREATE TABLE `im_export_credit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `credit_rating` varchar(48) DEFAULT NULL COMMENT '企业信用等级',
  `authentication_code` varchar(255) DEFAULT NULL COMMENT '认证证书编码',
  `identification_time` datetime DEFAULT NULL COMMENT '认定时间',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=800 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for im_export_punish
-- ----------------------------
DROP TABLE IF EXISTS `im_export_punish`;
CREATE TABLE `im_export_punish` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `decision_number` varchar(28) DEFAULT NULL COMMENT '处罚编号',
  `penalty_date` datetime DEFAULT NULL COMMENT '处罚日期',
  `party` varchar(255) DEFAULT NULL COMMENT '当事人',
  `nature_of_case` varchar(64) DEFAULT NULL COMMENT '案件性质',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for invest
-- ----------------------------
DROP TABLE IF EXISTS `invest`;
CREATE TABLE `invest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(20) DEFAULT NULL,
  `ent_name` varchar(50) DEFAULT NULL,
  `credit_code` varchar(50) DEFAULT NULL,
  `invest_amount` varchar(25) DEFAULT NULL,
  `invest_percent` varchar(25) DEFAULT NULL,
  `ent_type` varchar(255) DEFAULT NULL,
  `business_scope` text,
  `business_state` varchar(50) DEFAULT NULL,
  `alias` varchar(25) DEFAULT NULL,
  `estiblish_date` varchar(25) DEFAULT NULL,
  `legal_person` varchar(50) DEFAULT NULL,
  `industry` varchar(50) DEFAULT NULL,
  `reg_capital` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10260 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for judicial_assistance
-- ----------------------------
DROP TABLE IF EXISTS `judicial_assistance`;
CREATE TABLE `judicial_assistance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `public_date` datetime DEFAULT NULL COMMENT '公示时间',
  `executed` varchar(64) DEFAULT NULL COMMENT '被执行人',
  `equity_amount` varchar(32) DEFAULT NULL COMMENT '股权数额',
  `equity_state` varchar(16) DEFAULT NULL COMMENT '股权状态',
  `execute_notice` varchar(255) DEFAULT NULL COMMENT '执行通知文号',
  `execute_court` varchar(86) DEFAULT NULL COMMENT '执行法院',
  `execute_list` text COMMENT '执行事项',
  `execute_order` varchar(32) DEFAULT NULL COMMENT '执行裁定文书号',
  `license_type` varchar(32) DEFAULT NULL COMMENT '被执行人证照种类',
  `license_number` varchar(32) DEFAULT NULL COMMENT '被执行人证照号码',
  `from_date` datetime DEFAULT NULL COMMENT '冻结期限自',
  `to_date` datetime DEFAULT NULL COMMENT '冻结期限至',
  `period` varchar(64) DEFAULT NULL COMMENT '冻结期限',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1171 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for judicial_sale
-- ----------------------------
DROP TABLE IF EXISTS `judicial_sale`;
CREATE TABLE `judicial_sale` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `title_money` varchar(255) DEFAULT NULL,
  `court` varchar(255) DEFAULT NULL,
  `public_date` datetime DEFAULT NULL,
  `initial_price` varchar(25) DEFAULT NULL,
  `consult_price` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=525 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lawsuit_basic
-- ----------------------------
DROP TABLE IF EXISTS `lawsuit_basic`;
CREATE TABLE `lawsuit_basic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL COMMENT '案件名称',
  `case_type` varchar(64) DEFAULT NULL COMMENT '案件类型',
  `submittime` datetime DEFAULT NULL COMMENT '发布日期',
  `casereason` varchar(64) DEFAULT NULL COMMENT '案由',
  `plaintiff` text COMMENT '原告',
  `defendants` text COMMENT '被告',
  `caseno` varchar(255) DEFAULT NULL COMMENT '案号',
  `lawsuit_detail` longtext COMMENT '案件详情',
  `court` varchar(60) DEFAULT NULL,
  `decision_time` datetime DEFAULT NULL,
  `decide_reason` text,
  `result` text,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=79008 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for licence_info
-- ----------------------------
DROP TABLE IF EXISTS `licence_info`;
CREATE TABLE `licence_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `licence_number` varchar(255) DEFAULT NULL,
  `licence_name` varchar(255) DEFAULT NULL,
  `licence_anth` varchar(64) DEFAULT NULL,
  `from_date` datetime DEFAULT NULL,
  `to_date` datetime DEFAULT NULL,
  `licence_content` text,
  `legal_person` varchar(64) DEFAULT NULL,
  `audit_type` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=68577 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for members
-- ----------------------------
DROP TABLE IF EXISTS `members`;
CREATE TABLE `members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `person_name` varchar(64) DEFAULT NULL COMMENT '姓名',
  `position` varchar(64) DEFAULT NULL COMMENT '职位',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=272143 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for owing_tax
-- ----------------------------
DROP TABLE IF EXISTS `owing_tax`;
CREATE TABLE `owing_tax` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `tax_id_number` varchar(64) DEFAULT NULL COMMENT '纳税人识别号',
  `publish_date` datetime DEFAULT NULL COMMENT '发布时间',
  `tax_category` varchar(64) DEFAULT NULL COMMENT '欠税税种',
  `own_tax_balance` varchar(64) DEFAULT NULL COMMENT '欠税余额',
  `new_own_tax_balance` varchar(64) DEFAULT NULL COMMENT '当前新发生的欠税额',
  `department` varchar(128) DEFAULT NULL COMMENT '税务机关',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1704 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for patent
-- ----------------------------
DROP TABLE IF EXISTS `patent`;
CREATE TABLE `patent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `patent_name` text COMMENT '专利名称',
  `apply_number` varchar(50) DEFAULT NULL COMMENT '申请号',
  `pub_number` varchar(50) DEFAULT NULL COMMENT '公开号',
  `cat_number` varchar(50) DEFAULT NULL COMMENT '分类号',
  `apply_date` varchar(25) DEFAULT NULL COMMENT '申请日',
  `app_publish_date` varchar(25) DEFAULT NULL COMMENT '公开（公告）日',
  `applicant_name` varchar(128) DEFAULT NULL COMMENT '申请(专利权)人',
  `inventor` varchar(256) DEFAULT NULL COMMENT '发明人',
  `agent` varchar(64) DEFAULT NULL COMMENT '代理人',
  `agency` varchar(128) DEFAULT NULL COMMENT '代理机构',
  `address` text COMMENT '地址',
  `abstracts` text COMMENT '摘要',
  `img_url` varchar(128) DEFAULT NULL COMMENT '附图',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=60060 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pledgereg
-- ----------------------------
DROP TABLE IF EXISTS `pledgereg`;
CREATE TABLE `pledgereg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `reg_number` int(20) DEFAULT NULL COMMENT '知识产权登记号',
  `ent_name` varchar(255) DEFAULT NULL COMMENT '公司名称',
  `kinds` varchar(255) DEFAULT NULL COMMENT '种类',
  `pledgor_name` varchar(255) DEFAULT NULL COMMENT '出质人名称',
  `pledge_from` datetime DEFAULT NULL COMMENT '质权登记起始日期',
  `pledge_to` datetime DEFAULT NULL COMMENT '质权登记终止日期',
  `public_date` datetime DEFAULT NULL COMMENT '公示日期',
  `tm_name` varchar(255) DEFAULT NULL COMMENT '商标名称',
  `state` varchar(255) DEFAULT NULL COMMENT '状态',
  `pledgee_name` varchar(255) DEFAULT NULL COMMENT '质权人名称',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `app_name` varchar(50) DEFAULT NULL,
  `filter_name` varchar(25) DEFAULT NULL,
  `classes` varchar(25) DEFAULT NULL,
  `brief` text,
  `icon` varchar(255) DEFAULT NULL,
  `pro_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for punishment
-- ----------------------------
DROP TABLE IF EXISTS `punishment`;
CREATE TABLE `punishment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `penish_dec_num` text,
  `illeg_type` text,
  `punish_content` longtext,
  `punish_auth` varchar(100) DEFAULT NULL,
  `decision_date` datetime DEFAULT NULL,
  `punish_name` varchar(100) DEFAULT NULL,
  `punish_type` varchar(80) DEFAULT NULL,
  `punish_type_second` varchar(80) DEFAULT NULL,
  `evidence` text,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10521 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for qualification
-- ----------------------------
DROP TABLE IF EXISTS `qualification`;
CREATE TABLE `qualification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `certificate_name` varchar(50) DEFAULT NULL,
  `cert_number` varchar(50) DEFAULT NULL,
  `start_date` varchar(25) DEFAULT NULL,
  `end_date` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=32885 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for shareholder
-- ----------------------------
DROP TABLE IF EXISTS `shareholder`;
CREATE TABLE `shareholder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shareholder` varchar(86) DEFAULT NULL COMMENT '股东名称',
  `shareholder_type` varchar(32) DEFAULT NULL COMMENT '股东类型',
  `blic_type` varchar(32) DEFAULT NULL COMMENT '执照类型',
  `blic_number` varchar(32) DEFAULT NULL COMMENT '执照号',
  `ent_type` varchar(64) DEFAULT NULL COMMENT '企业类型',
  `con_capital` varchar(32) DEFAULT NULL COMMENT '认缴出资额',
  `con_capital_date` datetime DEFAULT NULL COMMENT '认缴出资时间',
  `con_paid_in_capital` varchar(32) DEFAULT NULL COMMENT '实缴出资额',
  `paid_in_capital_date` datetime DEFAULT NULL COMMENT '实缴出资时间',
  `share_ratio` varchar(32) DEFAULT NULL COMMENT '股权占比',
  `currency` varchar(255) DEFAULT NULL,
  `c_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=220268 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for taxcred
-- ----------------------------
DROP TABLE IF EXISTS `taxcred`;
CREATE TABLE `taxcred` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `id_number` varchar(50) DEFAULT NULL,
  `years` varchar(50) DEFAULT NULL,
  `eval_department` varchar(86) DEFAULT NULL,
  `grade` varchar(25) DEFAULT NULL,
  `eval_type` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4929 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tm_info
-- ----------------------------
DROP TABLE IF EXISTS `tm_info`;
CREATE TABLE `tm_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `tm_name` varchar(255) DEFAULT NULL,
  `reg_number` varchar(20) DEFAULT NULL,
  `tm_type` varchar(25) DEFAULT NULL,
  `reg_annc_date` varchar(255) DEFAULT NULL,
  `reg_annc_issue` varchar(255) DEFAULT NULL,
  `property_bgn_date` varchar(255) DEFAULT NULL,
  `property_end_date` varchar(255) DEFAULT NULL,
  `goods_name` text,
  `apply_date` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `applicant` varchar(255) DEFAULT NULL,
  `apply_process` text,
  `pic_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=59267 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for to_execute
-- ----------------------------
DROP TABLE IF EXISTS `to_execute`;
CREATE TABLE `to_execute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `executed` varchar(64) DEFAULT NULL COMMENT '被执行人',
  `org_code` varchar(32) DEFAULT NULL COMMENT '组织机构代码',
  `exec_money` varchar(32) DEFAULT NULL COMMENT '执行标的',
  `exec_court` varchar(32) DEFAULT NULL COMMENT '执行法院',
  `case_create_date` datetime DEFAULT NULL COMMENT '立案时间',
  `publish_date` datetime DEFAULT NULL,
  `case_number` varchar(32) DEFAULT NULL COMMENT '案号',
  `sex` varchar(16) DEFAULT NULL COMMENT '性别',
  `province` varchar(16) DEFAULT NULL COMMENT '省份',
  `gist_num` varchar(255) DEFAULT NULL COMMENT '执行依据文号',
  `gist_unit` varchar(64) DEFAULT NULL COMMENT '做出执行依据单位',
  `duty` text COMMENT '生效法律文书确定的义务',
  `performance` text COMMENT '被执行人的履行情况',
  `disrupttype_name` text COMMENT '失信被执行人行为具体情形',
  `end_date` datetime DEFAULT NULL COMMENT '终本日期',
  `unexectued` text COMMENT '未履行金额',
  `legal_person` varchar(64) DEFAULT NULL COMMENT '法定代表人或者负责人姓名',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2939 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for website_info
-- ----------------------------
DROP TABLE IF EXISTS `website_info`;
CREATE TABLE `website_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `web_name` varchar(64) DEFAULT NULL COMMENT '网址名称',
  `web_site` varchar(255) DEFAULT NULL COMMENT '网站首页',
  `examine_date` datetime DEFAULT NULL COMMENT '审核时间',
  `liscense` varchar(32) DEFAULT NULL COMMENT '备案号',
  `company_type` varchar(32) DEFAULT NULL COMMENT '主办单位性质',
  `ym` varchar(112) DEFAULT NULL COMMENT '域名',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8375 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for year_report
-- ----------------------------
DROP TABLE IF EXISTS `year_report`;
CREATE TABLE `year_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `company_name` varchar(64) DEFAULT NULL COMMENT '公司名',
  `report_year` varchar(28) DEFAULT NULL COMMENT '年报年份',
  `reg_number` varchar(28) DEFAULT NULL COMMENT '工商注册号',
  `manage_state` varchar(28) DEFAULT NULL COMMENT '企业经营状态',
  `employee_num` varchar(64) DEFAULT NULL COMMENT '从业人数',
  `phone_number` text COMMENT '联系电话',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `postal_address` varchar(255) DEFAULT NULL COMMENT '企业通讯地址',
  `postcode` varchar(28) DEFAULT NULL COMMENT '邮政编码',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=204603 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for year_report_assert
-- ----------------------------
DROP TABLE IF EXISTS `year_report_assert`;
CREATE TABLE `year_report_assert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `total_assets` varchar(64) DEFAULT NULL COMMENT '资产总额',
  `total_equity` varchar(64) DEFAULT NULL COMMENT '所有者权益合计',
  `total_sales` varchar(64) DEFAULT NULL COMMENT '销售总额',
  `total_profit` varchar(64) DEFAULT NULL COMMENT '利润总额',
  `prime_busprofit` varchar(64) DEFAULT NULL COMMENT '主营业收入',
  `retained_profit` varchar(64) DEFAULT NULL COMMENT '净利润',
  `total_tax` varchar(64) DEFAULT NULL COMMENT '纳税总额',
  `total_liability` varchar(64) DEFAULT NULL COMMENT '负债总额',
  `report_year` varchar(64) DEFAULT NULL COMMENT '年份',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=167268 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for year_report_social_security
-- ----------------------------
DROP TABLE IF EXISTS `year_report_social_security`;
CREATE TABLE `year_report_social_security` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `endowment_insurance` varchar(28) DEFAULT NULL COMMENT '养老保险',
  `medical_insurance` varchar(28) DEFAULT NULL COMMENT '医疗保险',
  `maternit_insurance` varchar(28) DEFAULT NULL COMMENT '生育保险',
  `unemployment_insurance` varchar(28) DEFAULT NULL COMMENT '失业保险',
  `employmentinjury_insurance` varchar(28) DEFAULT NULL COMMENT '工伤保险',
  `endowment_insurance_base` varchar(64) DEFAULT NULL COMMENT '养老保险缴费基数',
  `medical_insurance_base` varchar(64) DEFAULT NULL COMMENT '医疗保险缴费基数',
  `maternit_insurance_base` varchar(64) DEFAULT NULL COMMENT '生育保险缴费基数',
  `unemployment_insurance_base` varchar(64) DEFAULT NULL COMMENT '失业保险缴费基数',
  `employmentinjury_insurance_base` varchar(64) DEFAULT NULL COMMENT '工伤保险缴费基数',
  `endowment_insurance_payamount` varchar(64) DEFAULT NULL COMMENT '养老保险实际缴费金额',
  `medical_insurance_payamount` varchar(64) DEFAULT NULL COMMENT '医疗保险实际缴费金额',
  `maternit_insurance_payamount` varchar(64) DEFAULT NULL COMMENT '生育保险实际缴费金额',
  `unemployment_insurance_payamount` varchar(64) DEFAULT NULL COMMENT '失业保险实际缴费金额',
  `employmentinjury_insurance_payamount` varchar(64) DEFAULT NULL COMMENT '工伤保险实际缴费金额',
  `endowment_insurance_oweamount` varchar(64) DEFAULT NULL COMMENT '养老保险累计欠款金额',
  `medical_insurance_oweamount` varchar(64) DEFAULT NULL COMMENT '医疗保险累计欠款金额',
  `maternit_insurance_oweamount` varchar(64) DEFAULT NULL COMMENT '生育保险累计欠款金额',
  `unemployment_insurance_oweamount` varchar(64) DEFAULT NULL COMMENT '失业保险累计欠款金额',
  `employmentinjury_insurance_oweamount` varchar(64) DEFAULT NULL COMMENT '工伤保险累计欠款金额',
  `report_year` varchar(28) DEFAULT NULL COMMENT '年份',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=116159 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for year_report_store
-- ----------------------------
DROP TABLE IF EXISTS `year_report_store`;
CREATE TABLE `year_report_store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c_id` int(11) DEFAULT NULL,
  `web_name` varchar(64) DEFAULT NULL COMMENT '名称',
  `web_type` varchar(28) DEFAULT NULL COMMENT '类型',
  `web_site` varchar(255) DEFAULT NULL COMMENT '网址',
  `report_year` varchar(28) DEFAULT NULL COMMENT '年份',
  PRIMARY KEY (`id`),
  KEY `c_id` (`c_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=7129 DEFAULT CHARSET=utf8;
