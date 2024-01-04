-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 17, 2023 at 02:44 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `edutrackingsystemdb2`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendancemodel`
--

CREATE TABLE `attendancemodel` (
  `id` int(11) NOT NULL,
  `teacher_id` varchar(11) NOT NULL,
  `device_number` varchar(50) NOT NULL,
  `out_time` datetime NOT NULL,
  `input_time` datetime NOT NULL,
  `status` varchar(15) DEFAULT NULL,
  `punch` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendancemodel`
--

INSERT INTO `attendancemodel` (`id`, `teacher_id`, `device_number`, `out_time`, `input_time`, `status`, `punch`) VALUES
(3, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(4, '10', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(5, '10', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(6, '10', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(7, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(8, '10', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(9, '3', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(10, '4', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(11, '5', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(12, '9', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(13, '8', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(14, '6', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(15, '7', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(16, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '4'),
(17, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(18, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(19, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(20, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(21, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(22, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(23, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(24, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(25, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(26, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(27, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(28, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(29, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(30, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(31, '8', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(32, '8', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(33, '8', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(34, '8', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '1'),
(35, '777', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(36, '778', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(37, '778', '5', '2023-08-26 00:00:00', '2023-08-26 00:00:00', '', '0'),
(38, '777', '5', '2023-08-27 00:00:00', '2023-08-27 00:00:00', '', '0'),
(39, '1', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(40, '5', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(41, '1', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(42, '5', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(43, '1', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(44, '777', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(45, '1', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(46, '8', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(47, '3', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(48, '3', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(49, '5', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(50, '3', '5', '2023-08-28 00:00:00', '2023-08-28 00:00:00', '', '0'),
(51, '1', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '0'),
(52, '1', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '0'),
(53, '4', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '0'),
(54, '4', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '0'),
(55, '5', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '0'),
(56, '8', '5', '2023-08-29 00:00:00', '2023-08-29 00:00:00', '', '1'),
(57, '3', '5', '2023-09-01 00:00:00', '2023-09-01 00:00:00', '', '0'),
(58, '3', '5', '2023-09-02 00:00:00', '2023-09-02 00:00:00', '', '0'),
(59, '3', '5', '2023-09-02 00:00:00', '2023-09-02 00:00:00', '', '0'),
(60, '1', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(61, '3', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(62, '10', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(63, '3', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(64, '10', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(65, '3', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(66, '778', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(67, '4', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(68, '8', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(69, '10', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(70, '10', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(71, '4', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(72, '1', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(73, '5', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(74, '5', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(75, '1', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(76, '2', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(77, '5', '5', '2023-09-03 00:00:00', '2023-09-03 00:00:00', '', '0'),
(78, '1', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(79, '1', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(80, '1', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(81, '5', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(82, '1', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(83, '5', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(84, '10', '5', '2023-09-04 00:00:00', '2023-09-04 00:00:00', '', '0'),
(85, '1', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(86, '1', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(87, '1', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(88, '1', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(89, '1', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(90, '5', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(91, '4', '5', '2023-09-05 00:00:00', '2023-09-05 00:00:00', '', '0'),
(92, '1', '5', '2023-09-09 00:00:00', '2023-09-09 00:00:00', '', '0'),
(93, '10', '5', '2023-09-09 00:00:00', '2023-09-09 00:00:00', '', '0'),
(94, '4', '5', '2023-09-09 00:00:00', '2023-09-09 00:00:00', '', '0'),
(95, '11', '5', '2023-09-12 00:00:00', '2023-09-12 00:00:00', '', '0'),
(96, '5', '5', '2023-09-12 00:00:00', '2023-09-12 00:00:00', '', '0'),
(97, '777', '5', '2023-09-13 00:00:00', '2023-09-13 00:00:00', '', '0'),
(98, '11', '5', '2023-09-13 00:00:00', '2023-09-13 00:00:00', '', '0'),
(99, '11', '5', '2023-09-13 00:00:00', '2023-09-13 00:00:00', '', '0'),
(100, '11', '5', '2023-09-13 00:00:00', '2023-09-13 00:00:00', '', '0'),
(101, '11', '5', '2023-09-13 00:00:00', '2023-09-13 00:00:00', '', '0'),
(102, '777', '5', '2023-09-20 00:00:00', '2023-09-20 00:00:00', '', '0'),
(103, '5', '5', '2023-10-05 00:00:00', '2023-10-05 00:00:00', '', '0'),
(104, '11', '5', '2023-10-06 00:00:00', '2023-10-06 00:00:00', '', '0'),
(105, '777', '5', '2023-10-08 00:00:00', '2023-10-08 00:00:00', '', '0'),
(106, '777', '5', '2023-10-08 00:00:00', '2023-10-08 00:00:00', '', '0'),
(107, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(108, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(109, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(110, '4', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(111, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(112, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(113, '5', '5', '2023-10-05 00:00:00', '2023-10-05 00:00:00', '', '0'),
(114, '11', '5', '2023-10-06 00:00:00', '2023-10-06 00:00:00', '', '0'),
(115, '777', '5', '2023-10-08 00:00:00', '2023-10-08 00:00:00', '', '0'),
(116, '777', '5', '2023-10-08 00:00:00', '2023-10-08 00:00:00', '', '0'),
(117, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(118, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(119, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(120, '4', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(121, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0'),
(122, '11', '5', '2023-10-09 00:00:00', '2023-10-09 00:00:00', '', '0');

-- --------------------------------------------------------

--
-- Table structure for table `boardfathers`
--

CREATE TABLE `boardfathers` (
  `member_id` int(11) NOT NULL,
  `social_status` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `organic_status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `classroom`
--

CREATE TABLE `classroom` (
  `id` int(11) NOT NULL,
  `school_id` int(11) DEFAULT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classroom`
--

INSERT INTO `classroom` (`id`, `school_id`, `name`) VALUES
(27, 91, 'الثاني'),
(28, 91, 'الثالث');

-- --------------------------------------------------------

--
-- Table structure for table `councilfathers`
--

CREATE TABLE `councilfathers` (
  `id` int(11) NOT NULL,
  `members_id` int(11) NOT NULL,
  `CouncilFathersTask` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `councilfathers`
--

INSERT INTO `councilfathers` (`id`, `members_id`, `CouncilFathersTask`) VALUES
(7, 92, 'kkkkkkkkkkkkk');

-- --------------------------------------------------------

--
-- Table structure for table `device`
--

CREATE TABLE `device` (
  `id` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port` int(11) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `device`
--

INSERT INTO `device` (`id`, `school_id`, `name`, `ip`, `port`, `status`) VALUES
(5, 91, 'جهاز مدرسة فاطمة الزهراء', '192.168.1.201', 4370, 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `fingerprintdata`
--

CREATE TABLE `fingerprintdata` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `finger_id` int(11) NOT NULL,
  `device_number` int(11) NOT NULL,
  `card_id` int(11) NOT NULL,
  `password` varchar(30) NOT NULL,
  `f1` int(11) NOT NULL,
  `f2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `school_id` int(11) NOT NULL,
  `fName` varchar(255) NOT NULL,
  `sName` varchar(50) NOT NULL,
  `tName` varchar(50) NOT NULL,
  `lName` varchar(50) NOT NULL,
  `phone` int(11) NOT NULL,
  `dateBerth` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`id`, `school_id`, `fName`, `sName`, `tName`, `lName`, `phone`, `dateBerth`) VALUES
(79, 91, 'fgfg', 'fgf', 'gfg', 'fgf', 444444, '2000-01-01'),
(80, 91, 'mohammed 	', 'hamoud', 'ahmed', 'mohammed', 0, '2000-01-01'),
(81, 91, 'mohammed', 'hamous', 'ahmed', 'essa', 454545, '2000-01-01'),
(82, 91, 'hhhhhh', 'h', 'hhhhhhhhhhhh', 'hhhhhhr44', 444, '2000-01-01'),
(83, 91, 'dsfdddddddd', 'sdf', 'dsf', 'ddd', 333, '2000-01-01'),
(84, 91, 'df', 'df', 'df', 'df', 0, '2000-01-01'),
(85, 91, 'fh', 'ghf', 'gh', 'fghfg', 5555555, '2000-01-01'),
(86, 91, 'rrrrrr', 'dsf', 'sdf', 'sdf', 344, '2000-01-01'),
(87, 91, 'tttttt', 't', 'ttttttttttttttttt', 'tttttttttttt', 33333333, '2000-01-01'),
(88, 91, 'dddd', 'dddd', 'ddddd', 'dddd', 44444, '2000-01-01'),
(89, 91, 'ddddd', 'dddddddddddddddd', 'ddddddddddddd', 'ddddddddddddd', 33333, '2000-01-01'),
(90, 91, 'sd', 'ddddds', 'ssss', 'ssss', 0, '2000-01-01'),
(91, 91, 'ff', 'fffffffffffffff', 'fffffffffffff', 'fffffffffffff', 555, '2000-01-01'),
(92, 91, 'kkk', 'kkkkkkkkkkkkkk', 'kkkkkkkkkkkkk', 'kkkkkkkkkkkkkk', 0, '2000-01-01');

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `led_main` tinyint(1) NOT NULL,
  `led_manage` tinyint(1) NOT NULL,
  `led_setting` tinyint(1) NOT NULL,
  `bt_save_student` tinyint(1) NOT NULL,
  `bt_search_student` tinyint(1) NOT NULL,
  `bt_update_student` tinyint(1) NOT NULL,
  `bt_delete_student` tinyint(1) NOT NULL,
  `bt_reports_student` tinyint(1) NOT NULL,
  `bt_show_student` tinyint(1) NOT NULL,
  `bt_export_student` tinyint(1) NOT NULL,
  `bt_save_teacher` tinyint(1) NOT NULL,
  `bt_search_teacher` tinyint(1) NOT NULL,
  `bt_update_teacher` tinyint(1) NOT NULL,
  `bt_delete_teacher` tinyint(1) NOT NULL,
  `bt_reports_teacher` tinyint(1) NOT NULL,
  `bt_show_teacher` tinyint(1) NOT NULL,
  `bt_export_teacher` tinyint(1) NOT NULL,
  `bt_save_fathers` tinyint(1) NOT NULL,
  `bt_search_fathers` tinyint(1) NOT NULL,
  `bt_update_fathers` tinyint(1) NOT NULL,
  `bt_delete_fathers` tinyint(1) NOT NULL,
  `bt_save_user` tinyint(1) NOT NULL,
  `bt_search_user` tinyint(1) NOT NULL,
  `bt_update_user` tinyint(1) NOT NULL,
  `bt_delete_user` tinyint(1) NOT NULL,
  `bt_save_device` tinyint(1) NOT NULL,
  `bt_search_device` tinyint(1) NOT NULL,
  `bt_update_device` tinyint(1) NOT NULL,
  `bt_delete_device` tinyint(1) NOT NULL,
  `bt_export_device` tinyint(1) NOT NULL,
  `bt_show_device` tinyint(1) NOT NULL,
  `bt_save_attendance` tinyint(1) NOT NULL,
  `bt_search_attendance` tinyint(1) NOT NULL,
  `bt_update_attendance` tinyint(1) NOT NULL,
  `bt_delete_attendance` tinyint(1) NOT NULL,
  `bt_export_attendance` tinyint(1) NOT NULL,
  `bt_show_attendance` tinyint(1) NOT NULL,
  `bt_save_timetable_student` tinyint(1) NOT NULL,
  `bt_show_timetable_student` tinyint(1) NOT NULL,
  `bt_export_timetable_student` tinyint(1) NOT NULL,
  `bt_show_timetable_teacher` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `users_id`, `led_main`, `led_manage`, `led_setting`, `bt_save_student`, `bt_search_student`, `bt_update_student`, `bt_delete_student`, `bt_reports_student`, `bt_show_student`, `bt_export_student`, `bt_save_teacher`, `bt_search_teacher`, `bt_update_teacher`, `bt_delete_teacher`, `bt_reports_teacher`, `bt_show_teacher`, `bt_export_teacher`, `bt_save_fathers`, `bt_search_fathers`, `bt_update_fathers`, `bt_delete_fathers`, `bt_save_user`, `bt_search_user`, `bt_update_user`, `bt_delete_user`, `bt_save_device`, `bt_search_device`, `bt_update_device`, `bt_delete_device`, `bt_export_device`, `bt_show_device`, `bt_save_attendance`, `bt_search_attendance`, `bt_update_attendance`, `bt_delete_attendance`, `bt_export_attendance`, `bt_show_attendance`, `bt_save_timetable_student`, `bt_show_timetable_student`, `bt_export_timetable_student`, `bt_show_timetable_teacher`) VALUES
(1, 6, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(2, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `school`
--

CREATE TABLE `school` (
  `id` int(11) NOT NULL,
  `school_name` varchar(100) NOT NULL,
  `city` varchar(30) NOT NULL,
  `directorate` varchar(30) NOT NULL,
  `village` varchar(30) NOT NULL,
  `academic_level` varchar(20) NOT NULL,
  `student_gender_type` varchar(10) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `school`
--

INSERT INTO `school` (`id`, `school_name`, `city`, `directorate`, `village`, `academic_level`, `student_gender_type`, `created_at`, `updated_at`) VALUES
(91, 'مدرسة فاطمة الزهراء', 'عمران', 'المدان', 'سسسسس', 'ثانوي', 'مختلط', '2023-10-09 22:36:55', '2023-10-09 22:36:55');

-- --------------------------------------------------------

--
-- Table structure for table `session`
--

CREATE TABLE `session` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `shifttime`
--

CREATE TABLE `shifttime` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `shift_Type` varchar(50) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shifttime`
--

INSERT INTO `shifttime` (`id`, `name`, `shift_Type`, `start_time`, `end_time`) VALUES
(1, 'الوردية الاولى', 'صباحي', '08:30:00', '13:30:00'),
(2, 'الوردية الثانية', 'مسائي', '13:30:00', '16:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `shift_time`
--

CREATE TABLE `shift_time` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `shift_Type` varchar(50) NOT NULL,
  `start_time` time NOT NULL,
  `delay_times` int(11) NOT NULL,
  `end_time` time NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shift_time`
--

INSERT INTO `shift_time` (`id`, `name`, `shift_Type`, `start_time`, `delay_times`, `end_time`, `created_at`, `updated_at`) VALUES
(1, 'wer', 'weeee', '08:30:00', 20, '13:00:00', '2023-10-16 02:01:37', '2023-10-16 02:01:37'),
(2, 'dsf', 'dsf', '00:00:00', 22, '00:00:00', '2023-10-16 22:13:25', '2023-10-16 22:13:25');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `id` int(11) NOT NULL,
  `name` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`id`, `name`) VALUES
(1, 'dsfdsf'),
(2, 'dddddddd'),
(3, 'llllllllllll'),
(4, 'يبلبيل'),
(5, 'سسسس'),
(6, 'سسسيبيبب'),
(7, 'ااااا');

-- --------------------------------------------------------

--
-- Table structure for table `systemscreens`
--

CREATE TABLE `systemscreens` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `system_fr` varchar(40) NOT NULL,
  `additional` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `members_id` int(11) NOT NULL,
  `major` varchar(255) NOT NULL,
  `task` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `fingerPrintData` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `members_id`, `major`, `task`, `state`, `fingerPrintData`) VALUES
(53, 89, 'dddddddddddddddd', 'dddddddddd', 'مفعل', ''),
(54, 90, 'ss', 'sssssss', 'مفعل', ''),
(55, 91, 'ffff', 'ffffffff', 'مفعل', '');

-- --------------------------------------------------------

--
-- Table structure for table `teachershifts`
--

CREATE TABLE `teachershifts` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `shift_time_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teachersubjectclassroomtermtable`
--

CREATE TABLE `teachersubjectclassroomtermtable` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `subject_id` varchar(255) NOT NULL,
  `class_room_id` int(11) NOT NULL,
  `number_of_lessons` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teachersubjectclassroomtermtable`
--

INSERT INTO `teachersubjectclassroomtermtable` (`id`, `teacher_id`, `subject_id`, `class_room_id`, `number_of_lessons`) VALUES
(63, NULL, 'الجغرافيا', 28, 55);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `account_type` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `userPassword` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `state` varchar(255) NOT NULL,
  `initialization` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `account_type`, `Name`, `userName`, `userPassword`, `created_at`, `updated_at`, `state`, `initialization`) VALUES
(6, 'مسؤول', 'mohammed', 'moh', '123', '2023-10-16 03:04:13', '2023-10-16 03:04:13', 'True', 'False'),
(7, 'مدرسة', 'ali', 'ali', 'aaa', '2023-10-16 03:58:14', '2023-10-16 03:58:14', 'True', 'False');

-- --------------------------------------------------------

--
-- Table structure for table `weeklyclassschedule`
--

CREATE TABLE `weeklyclassschedule` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `class_room_id` int(11) NOT NULL,
  `day_id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendancemodel`
--
ALTER TABLE `attendancemodel`
  ADD PRIMARY KEY (`id`),
  ADD KEY `attendancemodel_teacher_id` (`teacher_id`);

--
-- Indexes for table `boardfathers`
--
ALTER TABLE `boardfathers`
  ADD PRIMARY KEY (`member_id`);

--
-- Indexes for table `classroom`
--
ALTER TABLE `classroom`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `classroom_name` (`name`),
  ADD KEY `classroom_school_id` (`school_id`);

--
-- Indexes for table `councilfathers`
--
ALTER TABLE `councilfathers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `councilfathers_members_id` (`members_id`);

--
-- Indexes for table `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`id`),
  ADD KEY `device_school_id` (`school_id`);

--
-- Indexes for table `fingerprintdata`
--
ALTER TABLE `fingerprintdata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fingerprintdata_teacher_id` (`teacher_id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `members_school_id` (`school_id`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `permissions_users_id` (`users_id`);

--
-- Indexes for table `school`
--
ALTER TABLE `school`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shifttime`
--
ALTER TABLE `shifttime`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shift_time`
--
ALTER TABLE `shift_time`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `students_member_id` (`member_id`),
  ADD KEY `students_class_id` (`class_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `systemscreens`
--
ALTER TABLE `systemscreens`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teachers_members_id` (`members_id`);

--
-- Indexes for table `teachershifts`
--
ALTER TABLE `teachershifts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teachershifts_teacher_id` (`teacher_id`),
  ADD KEY `teachershifts_shift_time_id` (`shift_time_id`);

--
-- Indexes for table `teachersubjectclassroomtermtable`
--
ALTER TABLE `teachersubjectclassroomtermtable`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teachersubjectclassroomtermtable_teacher_id` (`teacher_id`),
  ADD KEY `teachersubjectclassroomtermtable_class_room_id` (`class_room_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `weeklyclassschedule`
--
ALTER TABLE `weeklyclassschedule`
  ADD PRIMARY KEY (`id`),
  ADD KEY `weeklyclassschedule_teacher_id` (`teacher_id`),
  ADD KEY `weeklyclassschedule_subject_id` (`subject_id`),
  ADD KEY `weeklyclassschedule_class_room_id` (`class_room_id`),
  ADD KEY `weeklyclassschedule_day_id` (`day_id`),
  ADD KEY `weeklyclassschedule_session_id` (`session_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendancemodel`
--
ALTER TABLE `attendancemodel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=123;

--
-- AUTO_INCREMENT for table `classroom`
--
ALTER TABLE `classroom`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `councilfathers`
--
ALTER TABLE `councilfathers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `device`
--
ALTER TABLE `device`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `fingerprintdata`
--
ALTER TABLE `fingerprintdata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `school`
--
ALTER TABLE `school`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- AUTO_INCREMENT for table `session`
--
ALTER TABLE `session`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shifttime`
--
ALTER TABLE `shifttime`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `shift_time`
--
ALTER TABLE `shift_time`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `systemscreens`
--
ALTER TABLE `systemscreens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `teachershifts`
--
ALTER TABLE `teachershifts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `teachersubjectclassroomtermtable`
--
ALTER TABLE `teachersubjectclassroomtermtable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `weeklyclassschedule`
--
ALTER TABLE `weeklyclassschedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `boardfathers`
--
ALTER TABLE `boardfathers`
  ADD CONSTRAINT `boardfathers_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`);

--
-- Constraints for table `councilfathers`
--
ALTER TABLE `councilfathers`
  ADD CONSTRAINT `councilfathers_ibfk_1` FOREIGN KEY (`members_id`) REFERENCES `members` (`id`);

--
-- Constraints for table `device`
--
ALTER TABLE `device`
  ADD CONSTRAINT `device_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`);

--
-- Constraints for table `fingerprintdata`
--
ALTER TABLE `fingerprintdata`
  ADD CONSTRAINT `fingerprintdata_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`);

--
-- Constraints for table `members`
--
ALTER TABLE `members`
  ADD CONSTRAINT `members_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `permissions`
--
ALTER TABLE `permissions`
  ADD CONSTRAINT `permissions_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`members_id`) REFERENCES `members` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `teachershifts`
--
ALTER TABLE `teachershifts`
  ADD CONSTRAINT `teachershifts_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
  ADD CONSTRAINT `teachershifts_ibfk_2` FOREIGN KEY (`shift_time_id`) REFERENCES `shifttime` (`id`);

--
-- Constraints for table `teachersubjectclassroomtermtable`
--
ALTER TABLE `teachersubjectclassroomtermtable`
  ADD CONSTRAINT `teachersubjectclassroomtermtable_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `members` (`id`),
  ADD CONSTRAINT `teachersubjectclassroomtermtable_ibfk_2` FOREIGN KEY (`class_room_id`) REFERENCES `classroom` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `weeklyclassschedule`
--
ALTER TABLE `weeklyclassschedule`
  ADD CONSTRAINT `weeklyclassschedule_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `members` (`id`),
  ADD CONSTRAINT `weeklyclassschedule_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`id`),
  ADD CONSTRAINT `weeklyclassschedule_ibfk_3` FOREIGN KEY (`class_room_id`) REFERENCES `classroom` (`id`),
  ADD CONSTRAINT `weeklyclassschedule_ibfk_5` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
