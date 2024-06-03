-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2024 at 09:38 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vto`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `cdate` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `mid`, `pid`, `qty`, `cdate`) VALUES
(1, 2, 1, 1, '2024-03-25 01:23:55'),
(2, 2, 1, 1, '2024-03-25 01:24:38'),
(3, 2, 1, 1, '2024-03-25 01:25:24'),
(4, 2, 1, 1, '2024-03-25 01:26:20'),
(5, 2, 1, 1, '2024-03-25 01:28:19'),
(6, 2, 1, 1, '2024-03-25 01:30:41'),
(7, 2, 1, 1, '2024-03-25 01:31:29'),
(8, 2, 1, 1, '2024-03-25 01:33:32'),
(9, 2, 1, 1, '2024-03-25 01:34:21'),
(10, 2, 1, 1, '2024-03-25 01:34:50'),
(11, 2, 1, 1, '2024-03-25 01:36:30'),
(12, 2, 1, 1, '2024-03-25 01:37:26'),
(13, 2, 1, 1, '2024-03-25 01:40:25'),
(14, 2, 1, 1, '2024-03-25 01:41:41'),
(15, 2, 1, 1, '2024-03-25 01:43:20'),
(16, 2, 1, 1, '2024-03-25 01:43:55'),
(17, 2, 1, 1, '2024-03-25 01:44:59');

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`id`, `name`, `email`, `password`) VALUES
(1, 'vijay l kumar', 'lokanadam@gmail.com', 'secret'),
(2, 'chak', 'chak@gmail.com', 'chak');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `pname` varchar(50) NOT NULL,
  `pic` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `descrip` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `pname`, `pic`, `price`, `descrip`) VALUES
(1, 'PowerLook', 'f1.jpg', 78, ''),
(2, 'Sweatshirt', 'f2.jpg', 84, ''),
(3, 'top', 'm1.jpg', 100, 'Black and white printed sweatshirt with applique detail on chest, has a hood, long sleeves, two pock'),
(4, 'elegant', 'm2.jpg', 125, ''),
(5, 'top', 'm3.jpg', 99, ''),
(6, 'top', 'm4.jpg', 125, ''),
(7, 'Sweatshirt', 'f3.jpg', 123, ''),
(8, 'Sweatshirt', 'f4.jpg', 105, '');

-- --------------------------------------------------------

--
-- Table structure for table `resumes`
--

CREATE TABLE `resumes` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `education` varchar(200) DEFAULT NULL,
  `experience` varchar(500) DEFAULT NULL,
  `skills` varchar(500) DEFAULT NULL,
  `certifications` varchar(500) DEFAULT NULL,
  `languages` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `resumes`
--
ALTER TABLE `resumes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `resumes`
--
ALTER TABLE `resumes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
