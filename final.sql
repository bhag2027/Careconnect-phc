/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - phc_management_hos
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`phc_management_hos` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `phc_management_hos`;

/*Table structure for table `aasha_worker` */

DROP TABLE IF EXISTS `aasha_worker`;

CREATE TABLE `aasha_worker` (
  `aasha_worker_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`aasha_worker_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `aasha_worker` */

insert  into `aasha_worker`(`aasha_worker_id`,`login_id`,`firstname`,`lastname`,`city`,`phone`,`email`) values 
(1,71,'Arun','ss','kollam','8956895623','arun@gmail.com'),
(2,80,'Ashaworker','Ashaworker','kollam','7894561230','Ashaworker@gmail.com'),
(3,81,'Anu','ram','kannur','9090909090','anu@gmail.com'),
(4,86,'harsha','cc','jkl','8989898989','harsha@gmail.com');

/*Table structure for table `appointments` */

DROP TABLE IF EXISTS `appointments`;

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) DEFAULT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `appointment_date` varchar(30) DEFAULT NULL,
  `time` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `token_no` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `appointments` */

insert  into `appointments`(`appointment_id`,`doctor_id`,`patient_id`,`appointment_date`,`time`,`status`,`amount`,`token_no`,`type`) values 
(1,21,27,'2025-04-05','18:46','paid','0','1','Face To Face');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `category` */

insert  into `category`(`category_id`,`category`) values 
(2,'Bags'),
(3,'Vehicles '),
(5,'Jdjdj'),
(7,'Fan'),
(8,'Girl');

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) DEFAULT NULL,
  `complaint` varchar(50) DEFAULT NULL,
  `reply` varchar(30) DEFAULT NULL,
  `date_time` varchar(30) DEFAULT 'CURRENT_TIMESTAMP',
  PRIMARY KEY (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`complaint_id`,`patient_id`,`complaint`,`reply`,`date_time`) values 
(1,1,'not good','hiii','17-02-2021'),
(2,1,'werty','sdfsdc','17-02-2021'),
(3,3,'dfdf','good','2023-04-19'),
(17,7,'good hospitality ','pending','2024-01-20'),
(16,7,'yyyy','ok','2024-01-15'),
(6,7,'dghj','jjj','2023-12-20'),
(15,7,'ghuhbbh','fffff','2024-01-15'),
(8,7,'ningal poraaa','YYY','2023-12-20'),
(14,7,'fggh','hii','2024-01-14'),
(13,7,'hrrygv','jnjn','2023-12-28'),
(12,7,'cvh','ggg','2023-12-28'),
(18,22,'medicine shotage','nskddks','2025-03-12'),
(22,25,'Dr.anna is not punchual.','pending','2025-03-13 10:12:38'),
(23,24,'Rude behaviour of staff','pending','2025-03-13 13:54:39'),
(26,24,'poor hygiene','pending','2025-03-13 15:05:06'),
(27,27,'fffffffffffff','d','2025-03-16 22:55:03');

/*Table structure for table `departments` */

DROP TABLE IF EXISTS `departments`;

CREATE TABLE `departments` (
  `department_id` int(11) NOT NULL AUTO_INCREMENT,
  `hospital_id` int(11) DEFAULT NULL,
  `department_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`department_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `departments` */

insert  into `departments`(`department_id`,`hospital_id`,`department_name`) values 
(4,1,'Gynaecology'),
(3,1,'ENT'),
(5,4,'dept'),
(6,7,'ent'),
(7,7,'Gynaecology');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `doctor_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `hospital_id` int(11) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `qualification` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `leave_status` varchar(20) DEFAULT 'available',
  `leave_date` date DEFAULT NULL,
  PRIMARY KEY (`doctor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`doctor_id`,`login_id`,`hospital_id`,`first_name`,`last_name`,`place`,`phone`,`email`,`image`,`qualification`,`department`,`leave_status`,`leave_date`) values 
(21,68,1,'sam','aa','kollam','9865326598','sam@gmail.com','static/images/d2e7c72f-3b10-4119-be4c-ce72ac007b3edoctor.png','mbbs','department_name','available',NULL),
(22,76,1,'Roma','a','koduvally','9874561236','rr@gmail.com','static/images/6fba3a67-717b-494b-95e8-edda09195e26images (17).jpg','mbbs','department_id','available',NULL),
(25,89,1,'DrAnna','eldho','adimally','9697979876','anna@gmail.com','static/images/b1a27076-a48b-432c-8baf-b6986f9e94b5download.jpeg','mbbs','department_id','available',NULL),
(24,87,1,'karthik','shankar','trivandram','8989898989','karthik@gmail.com','static/images/a31e47b9-10cd-40ee-9f6c-ed55768ed96ddownload (1).jpeg','mbbs','department_id','available',NULL);

/*Table structure for table `doctor_leave` */

DROP TABLE IF EXISTS `doctor_leave`;

CREATE TABLE `doctor_leave` (
  `leave_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) NOT NULL,
  `leave_date` date NOT NULL,
  PRIMARY KEY (`leave_id`),
  KEY `doctor_id` (`doctor_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `doctor_leave` */

/*Table structure for table `duplicates` */

DROP TABLE IF EXISTS `duplicates`;

CREATE TABLE `duplicates` (
  `duplicate_id` int(11) NOT NULL AUTO_INCREMENT,
  `medical_record_id` int(11) DEFAULT NULL,
  `fpath` varchar(1000) DEFAULT NULL,
  `dfile` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`duplicate_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `duplicates` */

insert  into `duplicates`(`duplicate_id`,`medical_record_id`,`fpath`,`dfile`) values 
(1,8,'static/duplicates/e15307fd-0115-4294-8cab-0d769f75e1b6.jpg','static/duplicates/024f26d5-27c1-450e-9336-82a267a51330.jpg');

/*Table structure for table `event` */

DROP TABLE IF EXISTS `event`;

CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `aasha_worker_id` int(11) DEFAULT NULL,
  `event` varchar(100) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Data for the table `event` */

insert  into `event`(`event_id`,`aasha_worker_id`,`event`,`description`,`date`,`time`) values 
(5,4,'webinar','webinar about safety','2025-03-29','09:30:00'),
(7,4,'SEMINAR','Strategies to ensure access to health services:overcoming barriers ','2025-03-22','14:30:00'),
(8,4,'World Environment Day: Advancing pharmacy for a more sustainable world','World Environment Day is celebrated annually on 5 June to raise awareness and take action on critical issues to make a positive impact on the environment','2025-04-06','10:30:00'),
(14,4,'tyj','vnm,,,','2025-04-06','11:21:00');

/*Table structure for table `hospitals` */

DROP TABLE IF EXISTS `hospitals`;

CREATE TABLE `hospitals` (
  `hospital_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `hospital_name` varchar(30) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `landmark` varchar(30) DEFAULT NULL,
  `latitiude` varchar(30) DEFAULT NULL,
  `longitude` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`hospital_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `hospitals` */

insert  into `hospitals`(`hospital_id`,`login_id`,`hospital_name`,`place`,`landmark`,`latitiude`,`longitude`,`phone`,`email`,`image`,`status`) values 
(1,75,'oduvally','koduvally','near gov school','9.988800214678564','76.27249717712402','9874561230','bhagyaajayan@gmail.com','static/images/f40f14e5-859c-4897-95c1-98fa4d105649images (16).jpg','approved');

/*Table structure for table `lab` */

DROP TABLE IF EXISTS `lab`;

CREATE TABLE `lab` (
  `lab_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(100) DEFAULT NULL,
  `hospital_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`lab_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `lab` */

insert  into `lab`(`lab_id`,`login_id`,`hospital_id`,`name`,`details`) values 
(6,69,1,'Seva','Seva High Tech Laboratory');

/*Table structure for table `leave_request` */

DROP TABLE IF EXISTS `leave_request`;

CREATE TABLE `leave_request` (
  `leave_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`leave_request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `leave_request` */

insert  into `leave_request`(`leave_request_id`,`doctor_id`,`date`) values 
(1,25,'2025-04-04'),
(2,24,'2025-04-02');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(1000) DEFAULT NULL,
  `user_type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`user_type`) values 
(1,'admin','admin','admin'),
(68,'sam','scrypt:32768:8:1$hx9M6GWe278XPwwT$86330a5061d89770d8175b7e7b6768760f406480a60d84d9df1515cd147ad042083bb2ce1b5a5045431dabb1dde059cfcddfc68a757b86d6d502c999ba72a89f','doctor'),
(80,'Ashaworker','scrypt:32768:8:1$3A6ie464Nr00PVyE$af25a0f4ee5293be5645afb8d404caba25507800dc6adc77a3c6ba99381e754fe129f2dc8f7f867280e9ebcc141487b53a6b201b9d0c19e6af556db74cd431f3','aasha_worker'),
(76,'Doctorroma','scrypt:32768:8:1$NlhF2cw62l9e3WSp$4e13a32a285ac6fd18ed46d6761858126f543fabe314e05cf4856389e221d8c8437da6657a8c09a56786bf250f179fe516dde915db2ba17593521ecbc9ac0379','doctor'),
(66,'PharmacyAdmin','scrypt:32768:8:1$eYYacvUsHRW2x9A3$f10644b92b63ab729f1320f1e370a30917b19f0bea79612e3cc33e980c6098e3f1b550b28c1f1b8415a214317505530479bedb66996a81d54e8ea56e59ae83cc','pharmacy'),
(74,'qq','scrypt:32768:8:1$2yFgre2aviaxSLAI$f2ef44eaf3db37c3fcbf5c4f81341681bd609d9dd90881f410bc036af21a4da9726f694d312cb3b11cebfe7d076317902f827f637f5898b0dbbbfd04131c0b4f','patient'),
(71,'arun','scrypt:32768:8:1$vINc5VjLHkkfLOB2$dc6dd31d5cd87a35ced6ee313ed997ddcd5050777430eada97a21425d2c067b866a22b6a82286d005764ce07843dcd23efe1e096a6939370918af71abfb2df50','aasha_worker'),
(73,'mm','scrypt:32768:8:1$0ouKe54olnf9aM2T$e44c959a3462692d1c8aa82ceda068b8dc24991a5d4c7bc359cdaf387603a64d6b179572938fcbc40ceb245a222526570d9031a7453628df63a70dd23109fac9','patient'),
(75,'bhagyaajaya','scrypt:32768:8:1$visAEIqNLCz3MnSM$9896042095e1186a77883404b9ecb80595689818e809458e2bbc1548d6e5415a972657abdbc13588857e7311a43ceb2b9446e7dc3a503127d0026bef0e9a53aa','hospital'),
(77,'Arunima','scrypt:32768:8:1$xv773San9R7rEhSK$ff0db90b2c207ae12a04bed73a3c6876b58a4b508ae796c8fe3a15a172c24db1e54b95bd384d088ea7e34aee7cd92edca7ee704b58de35a58e3712fa99c0c9d6','patient'),
(69,'Labadmin','scrypt:32768:8:1$jpTHw2UMvgvDtX2U$fcc87755ddf4c02bdb6ed27596a68f2f6567ba8e628386b7431587cfcb078cdb8ba3ac2c637500cced3bb7d46a6d84bc0ad1be8b2634ce597f6a81817ce97482','lab'),
(81,'Anuram','scrypt:32768:8:1$9DxH7nu5nfGa7o2y$bc2adc2c930dd52972ceee17cc2aec47abf245ac6352b563b2ad4921307329f828fe3f9d440104318b5a6166f847ffe038e05379e2d14c08358136167bae2d66','aasha_worker'),
(82,'Gopika123','scrypt:32768:8:1$wP57e9AdRzQQd9S9$a08e82e33ece6706e1513d78ac209e9afc91ca63b98dce4d672c76b24e60c83d9829e23523a4f785ab926c0674977b3cf2c89949c2bd2d1c91b5ad015d622d0a','patient'),
(89,'annaeldho','scrypt:32768:8:1$XmFHS511YQpIVHLN$5cdad1850c9c9408c729f81b24ffc4f04a0c20af1791cbd09565a61ee9762974ca1158c794d57e0f5961490ed38b8e7bc5294b016c8d925c7e9586ad084784ab','doctor'),
(84,'harijn','scrypt:32768:8:1$iIIjnkj9Nes5726U$007d39cdc88939d145325e7abb37dfee3cf3cb9b1c83dc9b34626277d9d302127fa971566a3cdfb91b0b7ed9ef42c67ba6d0c05ef382e64d4ffe2b14525d6d2f','patient'),
(85,'Bhagyaajayan','scrypt:32768:8:1$bcBytUsxTi3b6ITc$d0468857d3911b450fb0d3b3a8970237712ecbf47327e709ef00bb80bbb29be53b97b799e396c751ebcdad1e31356b114e10de9f5d49af9c6b09e923a85c3a21','patient'),
(86,'harshacc','scrypt:32768:8:1$BgvcCiEEuiUniaVA$ec6c4558e05dfff620d8dadc54a914ba0ebeda38f67a0f755cad51d2571676b9448faeda71d3a0e9f2d5c3a0d5fa777ef19c463324d03b522a198d832af06c38','aasha_worker'),
(87,'karthik','scrypt:32768:8:1$NZ5i8Q2kz6k638IQ$31a7d277b353f88ebde9b768887f0e83618c78b478c584f8eb6e70366485edfeb2214bc6248eaef57b55fe0b14aacf23a929a781e5b8bfd70ce5038bdd76f3c3','doctor'),
(88,'ashnapaul','scrypt:32768:8:1$d6E0qVM075pHpUVt$eb78244b02db3050233f5d165fcfde2bbcf26d649b797a6097f7950fcb52c8e8dc20c2d98031d37d49f4e0ba99443a6e2a6b56dc900f678d211c588c5e730cee','patient'),
(90,'amalkk','scrypt:32768:8:1$62gAwEDJ0wYZbc7F$b0ac9d95e4dad6f54b78b2fbb145d4589048ea8231f40bff520a7a86cb36585074e9aefb42651ec0be1eaacdc6cd1b27302a2fd16564248eb1a67a36439a987f','patient'),
(91,'shilpa','scrypt:32768:8:1$Kl6Rsvaxg0lx9L6Q$9a123bfdd31a35f7ddf99d91de4c18ca4c0a0fba2a8ba6b37d628f1e1387ad2b2665c0e02da873cb504f1665ea414b3b3277eb3e37886d0bbac7f7b57250612a','patient'),
(92,'albinkurian','scrypt:32768:8:1$w88SFxx0yQzsEWCL$280929defedef2fa788cf226cf9c2bd3b6791d3b0ddac06393d61c19ebb49700352da36bc235e212bf7e68930590745d82c7bf37baf59ce9f31fa691b8ba85de','patient'),
(93,'sumith','scrypt:32768:8:1$JAHqDHP1XJpSiA4o$69bc91c0df8336c9c4042d9f89532d5d01ea3be9fde5368a8e693cee68d8c1e0a79e29c147d2f4ba3c78ece9c132f617c9b4319a8b1729a7027e1a1ead1b943b','patient');

/*Table structure for table `medical_records` */

DROP TABLE IF EXISTS `medical_records`;

CREATE TABLE `medical_records` (
  `medical_record_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `uploaded_by` varchar(30) DEFAULT NULL,
  `file` varchar(500) DEFAULT NULL,
  `date_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`medical_record_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `medical_records` */

insert  into `medical_records`(`medical_record_id`,`patient_id`,`doctor_id`,`uploaded_by`,`file`,`date_time`) values 
(1,15,21,'doctor','static/uploads/5b796d42-d14a-4bbe-862e-de00a40fd02emedical_repory.png','2025-03-05 20:19:20'),
(2,15,21,'doctor','static/uploads/631e8ef2-b875-4af2-b660-7f72fc346cfcmedical_repory.png','2025-03-06 17:03:59'),
(3,17,22,'doctor','static/uploads/1d404d41-740c-4ba9-beda-504822edb2cfthumbnail.png','2025-03-09 12:02:36'),
(4,22,24,'doctor','static/uploads/8ef17d3a-1d44-481d-9c18-020d44d04a31medical report.png','2025-03-12 01:48:11'),
(5,25,25,'doctor','static/uploads/1a2d98d0-2728-476e-ac8f-a7acfec77d93download (2).jpeg','2025-03-13 10:14:26'),
(6,17,22,'doctor','static/uploads/d91b22a1-5e41-41ea-ad52-70a2b2da47c0download (2).jpeg','2025-03-13 11:22:13'),
(7,17,22,'doctor','static/uploads/6e456a62-e26d-4955-b138-76b0f77c3932download (2).jpeg','2025-03-13 11:27:00'),
(8,17,22,'doctor','static/uploads/8b990275-2f55-4119-933a-d421315c0e2cdownload (2).jpeg','2025-03-13 11:27:18'),
(9,24,24,'doctor','static/uploads/b863ba51-121b-4371-8084-bd259bbfa610download (2).jpeg','2025-03-13 15:02:18'),
(10,23,25,'doctor','static/uploads/18e4cfb6-6b59-4c7f-a2ac-f017559dc0b5download (2).jpeg','2025-03-17 09:39:01');

/*Table structure for table `messages` */

DROP TABLE IF EXISTS `messages`;

CREATE TABLE `messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `sender_type` varchar(30) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `receiver_type` varchar(30) DEFAULT NULL,
  `message` varchar(30) DEFAULT NULL,
  `date_time` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

/*Data for the table `messages` */

insert  into `messages`(`message_id`,`sender_id`,`sender_type`,`receiver_id`,`receiver_type`,`message`,`date_time`) values 
(1,34,'patient',36,'doctor','hai appu','2023-12-21 17:35:56'),
(2,36,'',34,'','hii','2023-12-21'),
(3,34,'patient',36,'doctor','dsmncdscvdbn','2023-12-21 17:39:28'),
(4,34,'patient',9,'doctor','hhh','2023-12-28 13:27:18'),
(5,34,'patient',36,'doctor','jjj','2023-12-28 13:29:23'),
(6,36,'',34,'','hj','2023-12-28'),
(7,36,'',34,'','gff','2023-12-28'),
(8,36,'',34,'','ert','2023-12-28'),
(9,36,'',47,'','jj','2024-01-12'),
(10,36,'',47,'','hhh','2024-01-12'),
(11,36,'',47,'','tff','2024-01-12'),
(12,36,'',47,'','tff','2024-01-12'),
(13,36,'',47,'','ty','2024-01-12'),
(14,36,'',47,'','ho','2024-01-12'),
(15,36,'',47,'','ghj','2024-01-12'),
(16,47,'patient',9,'doctor','jjjj','2024-01-13 14:52:12'),
(17,36,'',49,'','hy','2024-01-15'),
(18,34,'patient',12,'doctor','jjjj','2024-01-18 18:29:08'),
(19,34,'patient',48,'doctor','hi','2024-01-18 20:25:19'),
(20,49,'patient',16,'doctor','kkk','2024-01-20 11:13:10'),
(21,68,'patient',67,'doctor','hiiii','2025-03-05 19:03:40'),
(22,73,'patient',68,'doctor','hiiii','2025-03-05 20:41:39'),
(23,73,'patient',68,'doctor','jjjj','2025-03-05 20:43:59'),
(24,73,'patient',68,'doctor','kkk','2025-03-05 20:44:59'),
(25,68,'patient',73,'doctor','ll','2025-03-05 20:46:08'),
(26,77,'patient',76,'doctor','hai doctor','2025-03-09 13:04:11'),
(27,76,'patient',77,'doctor','how are ypou','2025-03-09 13:04:59'),
(28,77,'patient',76,'doctor','hii doctor','2025-03-10 21:51:03'),
(29,87,'patient',88,'doctor','hii','2025-03-13 15:08:01');

/*Table structure for table `patients` */

DROP TABLE IF EXISTS `patients`;

CREATE TABLE `patients` (
  `patient_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` varchar(100) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `dob` varchar(30) DEFAULT NULL,
  `gender` varchar(30) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

/*Data for the table `patients` */

insert  into `patients`(`patient_id`,`login_id`,`first_name`,`last_name`,`dob`,`gender`,`place`,`phone`,`email`) values 
(23,'88','Ashna','paulson','2025-03-21','female','bisonballey','6767676767','ashnadsilva2309@gmail.com'),
(17,'77','arunima','ds','2025-02-26','female','kollam','987456126','shemi96ven@gmail.com'),
(22,'85','Bhagya','ajayan','2025-03-15','female','oduvally','4545454545','bhagyazz2027@gmail.com'),
(24,'90','Amal','kk','2003-03-23','male','thamassery','8989898989','amalkk@gmail.com'),
(25,'91','shilpa','B','2016-01-10','female','adoor','789654123','manasabinduraj@gmail.com'),
(26,'92','Albin','kurian','2006-02-01','male','ashankavala','9345657632','albin@gmail.com'),
(27,'93','sumith','ps','2025-03-05','male','Thissur','7593938854','sumithps78@gmail.com');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `appointment_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `payment_status` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`appointment_id`,`amount`,`date`,`payment_status`) values 
(18,4,'5','2025-03-06','pending'),
(19,6,'5','2025-03-09','pending'),
(20,1,'5','2025-03-12','pending'),
(21,2,'5','2025-03-12','pending'),
(22,1,'5','2025-03-13','pending'),
(23,2,'5','2025-03-13','pending'),
(24,3,'5','2025-03-13','pending'),
(25,2,'5','2025-03-13','pending'),
(26,3,'5','2025-03-13','pending'),
(27,4,'5','2025-03-13','pending'),
(28,3,'5','2025-03-13','pending'),
(29,5,'5','2025-03-13','pending'),
(30,1,'5','2025-03-17','pending'),
(31,1,'5','2025-03-17','pending'),
(32,1,'5','2025-03-20','pending'),
(33,1,'5','2025-03-20','pending'),
(34,1,'5','2025-03-20','pending'),
(35,1,'5','2025-03-20','pending');

/*Table structure for table `pharmacy` */

DROP TABLE IF EXISTS `pharmacy`;

CREATE TABLE `pharmacy` (
  `pharmacy_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `landmark` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pharmacy_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `pharmacy` */

insert  into `pharmacy`(`pharmacy_id`,`login_id`,`name`,`place`,`landmark`,`phone`,`email`) values 
(1,66,'Medi Plus','Thissur','Thrissur round','7593938854','MediPlus@gmail.com');

/*Table structure for table `predict` */

DROP TABLE IF EXISTS `predict`;

CREATE TABLE `predict` (
  `predict_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `disease_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`predict_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `predict` */

/*Table structure for table `prescription` */

DROP TABLE IF EXISTS `prescription`;

CREATE TABLE `prescription` (
  `prescription_id` int(11) NOT NULL AUTO_INCREMENT,
  `appointment_id` int(11) DEFAULT NULL,
  `prescription` varchar(10000) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`prescription_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `prescription` */

insert  into `prescription`(`prescription_id`,`appointment_id`,`prescription`,`date`,`amount`,`status`) values 
(1,3,'xxxxxx','2025-03-06 16:45:39','1500','paid'),
(2,4,'gdhghfh','2025-03-06 21:10:51','2000','pending'),
(3,6,'Dosage: 500 mg  Frequency: Every 4â€“6 hours as needed for fever\r\nfhjlghhj','2025-03-09 12:36:40','pending','pending'),
(4,10,'Cetirizine (Setride, Okacet)\r\n Levocetirizine (Levozet, Xyzal) \r\nLoratadine (Claritin) Fexofenadine (Allegra)','2025-03-12 01:50:11','pending','pending'),
(5,12,'dolo','2025-03-13 10:15:00','pending','pending'),
(6,7,'ghj','2025-03-13 11:22:57','pending','pending'),
(7,20,'dolo','2025-03-13 15:01:37','pending','pending'),
(8,2,'jjkj','2025-03-17 09:38:42','pending','pending');

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rating_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient_id` int(11) DEFAULT NULL,
  `rate` varchar(100) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `Review` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rating_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`rating_id`,`patient_id`,`rate`,`doctor_id`,`Review`) values 
(6,7,'3.0',9,'super'),
(7,7,'4.0',10,'wooowww'),
(8,7,'4.0',11,'wooww'),
(9,7,'4.0',13,'good');

/*Table structure for table `request1` */

DROP TABLE IF EXISTS `request1`;

CREATE TABLE `request1` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `prescription_id` int(11) DEFAULT NULL,
  `pharmacy_id` int(11) DEFAULT NULL,
  `amount` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `request1` */

insert  into `request1`(`request_id`,`prescription_id`,`pharmacy_id`,`amount`,`date`,`status`) values 
(2,2,1,'0','curdate()','pending'),
(4,2,1,'522','curdate()','paid'),
(5,2,1,'0','2024-01-02','pending');

/*Table structure for table `requests` */

DROP TABLE IF EXISTS `requests`;

CREATE TABLE `requests` (
  `request_id` int(11) NOT NULL AUTO_INCREMENT,
  `medical_record_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `date_times` varchar(30) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `requests` */

insert  into `requests`(`request_id`,`medical_record_id`,`doctor_id`,`date_times`,`status`) values 
(4,2,3,'2021-03-16','pending'),
(3,2,3,'2021-03-16','pending'),
(5,3,3,'2021-03-16','Accepted'),
(6,10,3,'2021-09-16','pending');

/*Table structure for table `scheduling` */

DROP TABLE IF EXISTS `scheduling`;

CREATE TABLE `scheduling` (
  `scheduling_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) DEFAULT NULL,
  `ftime` varchar(50) DEFAULT NULL,
  `ttime` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`scheduling_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `scheduling` */

insert  into `scheduling`(`scheduling_id`,`doctor_id`,`ftime`,`ttime`) values 
(2,4,'07:30','10:30'),
(3,3,'07:30','10:30'),
(4,5,'13:48','18:46'),
(7,9,'16:15','08:24'),
(9,9,'08:15','22:28'),
(10,10,'10:25','14:25'),
(11,11,'18:47','23:47'),
(12,12,'23:32','13:32'),
(13,21,'18:46','20:46'),
(14,22,'11:54','11:55'),
(15,24,'09:00','12:40'),
(16,23,'01:33','05:00'),
(17,25,'01:00','05:30'),
(18,21,'02:02','02:02'),
(19,21,'01:01','01:05'),
(20,21,'01:01','01:05');

/*Table structure for table `symptoms` */

DROP TABLE IF EXISTS `symptoms`;

CREATE TABLE `symptoms` (
  `symptoms_id` int(11) NOT NULL AUTO_INCREMENT,
  `disease_id` int(11) DEFAULT NULL,
  `symptoms` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`symptoms_id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;

/*Data for the table `symptoms` */

insert  into `symptoms`(`symptoms_id`,`disease_id`,`symptoms`) values 
(1,7,'ooppoopo'),
(6,9,'uuo'),
(5,9,'uuo'),
(12,12,'stoolppp'),
(16,16,'headache and coldS'),
(10,12,'pp'),
(18,13,'jnn'),
(19,13,'jjj'),
(20,16,'ddd'),
(22,15,'jjjj'),
(23,15,'jjjj'),
(25,5,'nfj'),
(26,5,'nfj'),
(27,5,'nfj'),
(28,5,'nfj'),
(29,21,'stool'),
(30,21,'stool'),
(31,21,'stool'),
(32,21,'stool'),
(33,28,'uuuu'),
(34,28,'uuuu'),
(37,39,'jjj');

/*Table structure for table `test_reult` */

DROP TABLE IF EXISTS `test_reult`;

CREATE TABLE `test_reult` (
  `test_reult_id` int(11) NOT NULL AUTO_INCREMENT,
  `appointment_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `result` text,
  `amount` text,
  `status` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`test_reult_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `test_reult` */

insert  into `test_reult`(`test_reult_id`,`appointment_id`,`date`,`time`,`result`,`amount`,`status`) values 
(1,1,'2025-03-05','21:49:45','static/uploads/ce6bf561-c14c-450e-816f-68d7e0cb91d6medical_repory.png','1500','pending'),
(2,2,'2025-03-05','21:50:43','static/uploads/1cb10783-8d6f-4bf8-9227-875784e69dbbmedical_repory.png','30','pending'),
(10,12,'2025-03-13','10:16:06','static/uploads/84bbb55a-b622-40d8-a9f8-2fa4f31a7dc7medical report.png','10','paid'),
(6,6,'2025-03-09','12:45:40','static/uploads/6f7c341f-00ea-4d9f-8e5d-c5e8d25a8a41thumbnail.png','300','paid'),
(7,7,'2025-03-10','22:27:05','static/uploads/48de9074-ab3a-473b-ae38-e614c7501ab9pic8.png','35','paid'),
(8,10,'2025-03-12','01:54:43','static/uploads/2db35e24-6e43-4193-b4fc-990579e9baa7download (2).jpeg','30','paid'),
(9,11,'2025-03-12','22:37:32','static/uploads/adb98453-2556-4dbc-a687-1698c3b915e5download (2).jpeg','10','paid'),
(11,20,'2025-03-13','15:03:32','static/uploads/0bd032f5-bf03-484b-af89-7add3085401dmedical report.png','10','paid'),
(12,3,'2025-03-17','09:51:58','static/uploads/19857e9d-1f7c-4ae1-a0ec-98dacef29da7download (2).jpeg','15','paid');

/*Table structure for table `user_reg` */

DROP TABLE IF EXISTS `user_reg`;

CREATE TABLE `user_reg` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `user_reg` */

insert  into `user_reg`(`user_id`,`fname`,`image`) values 
(1,'Durga','static/847c36d7-482c-4b41-93b3-5c7f0359c1071699612619769.png');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
