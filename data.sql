-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 14, 2025 at 05:28 PM
-- Server version: 11.7.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `petmedix`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `hashed_password` varchar(64) NOT NULL,
  `role` varchar(50) NOT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `created_date` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `last_name`, `email`, `hashed_password`, `role`, `status`, `created_date`) VALUES
('2025A0001', 'Admin', NULL, 'admin@petmedix.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin', 'Verified', '2025-05-14 02:20:37'),
('2025R0001', 'Joelmar', 'Grecia', 'joelmar@petmedix.med', 'efda4bedf74923aed3d86a45b16d79a901e8b833a52299a8570c6702e32263bb', 'Receptionist', 'Verified', '2025-05-14 02:21:29'),
('2025V0001', 'Axel', 'Nuqui', 'axel@petmedix.med', '136fb1c37b1ed9088329405f62bbb903985612eeac49d3938a73966ea545cdb0', 'Veterinarian', 'Verified', '2025-05-14 06:42:12');

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`client_id`, `name`, `address`, `contact_number`, `email`) VALUES
(2, 'Joelmar Grecia', 'Molo, Iloilo City', '09934099656', 'joelmargrecia15@gmail.com'),
(3, 'Axel Nuqui', 'Villa', '033131', 'axel@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `clinic_info`
--

CREATE TABLE `clinic_info` (
  `clinic_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `employees_count` int(11) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `logo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`clinic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `clinic_info`
--

INSERT INTO `clinic_info` (`clinic_id`, `name`, `address`, `contact_number`, `email`, `employees_count`, `photo_path`, `logo_path`) VALUES
(1, 'VetGuard Animal Clinic', 'Jaro, Iloilo City', '09430434443', 'vetguardclinic@gmail.com', 3, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_profiles`
--

CREATE TABLE `user_profiles` (
  `profile_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `contact_number` varchar(15) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`profile_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `security_questions`
--

CREATE TABLE `security_questions` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `question_one` varchar(255) NOT NULL,
  `answer_one` varchar(255) NOT NULL,
  `question_two` varchar(255) NOT NULL,
  `answer_two` varchar(255) NOT NULL,
  `question_three` varchar(255) NOT NULL,
  `answer_three` varchar(255) NOT NULL,
  PRIMARY KEY (`question_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `security_questions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `security_questions`
--

INSERT INTO `security_questions` (`question_id`, `user_id`, `question_one`, `answer_one`, `question_two`, `answer_two`, `question_three`, `answer_three`) VALUES
(1, '2025R0001', 'What is your mother\'s maiden name?', 'efda4bedf74923aed3d86a45b16d79a901e8b833a52299a8570c6702e32263bb', 'What was the name of your first pet?', 'efda4bedf74923aed3d86a45b16d79a901e8b833a52299a8570c6702e32263bb', 'What is the name of the street you grew up on?', 'efda4bedf74923aed3d86a45b16d79a901e8b833a52299a8570c6702e32263bb'),
(2, '2025V0001', 'What is your mother\'s maiden name?', '4183b9f5ed14b64d012ce1e728cfa1e7afc399cb82b6729b222784db6b1a50a7', 'What was the name of your first pet?', '4183b9f5ed14b64d012ce1e728cfa1e7afc399cb82b6729b222784db6b1a50a7', 'What is the name of the street you grew up on?', '4183b9f5ed14b64d012ce1e728cfa1e7afc399cb82b6729b222784db6b1a50a7');

-- --------------------------------------------------------

--
-- Table structure for table `password_history`
--

CREATE TABLE `password_history` (
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) NOT NULL,
  `hashed_password` varchar(64) NOT NULL,
  `created_date` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`history_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `password_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pets`
--

CREATE TABLE `pets` (
  `pet_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `species` varchar(50) DEFAULT NULL,
  `breed` varchar(50) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `weight` decimal(10,2) DEFAULT NULL,
  `height` decimal(10,2) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `pets_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `pets`
--

INSERT INTO `pets` (`pet_id`, `client_id`, `name`, `gender`, `species`, `breed`, `color`, `birthdate`, `age`, `weight`, `height`, `photo_path`) VALUES
(3, 2, 'Jano', 'Male', 'Cat', 'Catpin', 'dad', '2025-05-14', 3, 2.00, 2.00, 'C:/Users/Joelmar/Pictures/cam/DSC00183.JPG'),
(4, 2, 'Alex', 'Male', 'Cat', 'Catpin', 'BW', '2025-05-14', 3, 20.00, 20.00, 'C:/Users/Joelmar/Pictures/cam/DSC00254.JPG'),
(5, 3, 'dwada', 'Male', 'dawd', 'dawd', 'bw', '2025-05-14', 3, 20.00, 20.00, 'C:/Users/Joelmar/Pictures/cam/DSC00257.JPG');

-- --------------------------------------------------------

--
-- Table structure for table `pet_notes`
--

CREATE TABLE `pet_notes` (
  `note_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `note_type` varchar(20) NOT NULL CHECK (`note_type` IN ('past_illnesses', 'medical_history')),
  `notes` text,
  `last_updated` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`note_id`),
  UNIQUE KEY `pet_note_type` (`pet_id`, `note_type`),
  CONSTRAINT `pet_notes_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Indexes for table pet notes (past illnesses and medical history)
--
CREATE INDEX `idx_pet_notes_pet_id` ON `pet_notes` (`pet_id`);
CREATE INDEX `idx_pet_notes_type` ON `pet_notes` (`note_type`);

--
-- Table structure for table `appointments`
--
s
CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `status` enum('Scheduled','Completed','Cancelled','No-Show','Rescheduled','Urgent') NOT NULL,
  `payment_status` enum('Pending','Paid','Unpaid') NOT NULL,
  `reason` text DEFAULT NULL,
  `veterinarian` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `pet_id`, `client_id`, `date`, `time`, `status`, `payment_status`, `reason`, `veterinarian`) VALUES
(1, 4, 2, '2025-05-08', '14:00:00', 'Scheduled', 'Paid', 'dawda', 'Axel'),
(2, 3, 2, '2025-05-14', '14:00:00', 'No-Show', 'Unpaid', 'dawda', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `billing`
--

CREATE TABLE `billing` (
  `billing_id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice_no` varchar(50) DEFAULT NULL,
  `client_id` int(11) NOT NULL,
  `pet_id` int(11) NOT NULL,
  `date_issued` date NOT NULL,
  `subtotal` decimal(10,2) NOT NULL DEFAULT 0.00,
  `vat` decimal(10,2) NOT NULL DEFAULT 0.00,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_status` enum('PAID', 'UNPAID', 'PARTIAL') NOT NULL,
  `partial_amount` decimal(10,2) DEFAULT 0.00,
  `payment_method` enum('CASH', 'CREDIT CARD', 'GCASH', 'BANK TRANSFER'),
  `received_by` varchar(100),
  `reason` varchar(200),
  `veterinarian` varchar(100),
  `notes` text,
  PRIMARY KEY (`billing_id`),
  KEY `client_id` (`client_id`),
  KEY `pet_id` (`pet_id`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE,
  CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `billing_services`
--

CREATE TABLE `billing_services` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `billing_id` int(11) NOT NULL,
  `service_description` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `line_total` decimal(10,2) NOT NULL,
  `service_date` date,
  PRIMARY KEY (`service_id`),
  KEY `billing_id` (`billing_id`),
  CONSTRAINT `billing_services_ibfk_1` FOREIGN KEY (`billing_id`) REFERENCES `billing` (`billing_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `consultations`
--

CREATE TABLE `consultations` (
  `consultation_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `reason` text NOT NULL,
  `diagnosis` text NOT NULL,
  `prescribed_treatment` text NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`consultation_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `consultations_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `consultations_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `consultations`
--

INSERT INTO `consultations` (`consultation_id`, `pet_id`, `client_id`, `date`, `reason`, `diagnosis`, `prescribed_treatment`, `veterinarian`) VALUES
(1, 4, 2, '2025-05-14', 'dawda', 'dawda', 'dwada', 'Axel'),
(2, 4, 2, '2025-05-14', 'dwad', 'dwadwa', 'dwada', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `deworming`
--

CREATE TABLE `deworming` (
  `deworming_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `medication` text NOT NULL,
  `dosage` text NOT NULL,
  `next_scheduled` date NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`deworming_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `deworming_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `deworming_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `deworming`
--

INSERT INTO `deworming` (`deworming_id`, `pet_id`, `client_id`, `date`, `medication`, `dosage`, `next_scheduled`, `veterinarian`) VALUES
(1, 5, 3, '2025-05-14', 'dawda', 'dawda', '2025-05-24', 'Axel'),
(2, 3, 2, '2025-05-14', 'dawda', 'dwaadw', '2025-05-29', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `grooming`
--

CREATE TABLE `grooming` (
  `grooming_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `services` text NOT NULL,
  `notes` text NOT NULL,
  `next_scheduled` date NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`grooming_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `grooming_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `grooming_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `grooming`
--

INSERT INTO `grooming` (`grooming_id`, `pet_id`, `client_id`, `date`, `services`, `notes`, `next_scheduled`, `veterinarian`) VALUES
(1, 4, 2, '2025-05-14', 'dwad', 'dwada', '2025-05-27', 'Axel'),
(2, 4, 2, '2025-05-14', 'dadwa', 'dawa', '2025-05-23', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `other_treatments`
--

CREATE TABLE `other_treatments` (
  `treatment_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `treatment_type` text NOT NULL,
  `medication` text NOT NULL,
  `dosage` text NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`treatment_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `other_treatments_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `other_treatments_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `other_treatments`
--

INSERT INTO `other_treatments` (`treatment_id`, `pet_id`, `client_id`, `date`, `treatment_type`, `medication`, `dosage`, `veterinarian`) VALUES
(1, 3, 2, '2025-05-14', 'dada', 'dwada', 'dwada', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `surgeries`
--

CREATE TABLE `surgeries` (
  `surgery_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `surgery_type` text NOT NULL,
  `anesthesia` text NOT NULL,
  `next_followup` date NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`surgery_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `surgeries_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `surgeries_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `surgeries`
--

INSERT INTO `surgeries` (`surgery_id`, `pet_id`, `client_id`, `date`, `surgery_type`, `anesthesia`, `next_followup`, `veterinarian`) VALUES
(1, 5, 3, '2025-05-14', 'dwada', 'dwadaw', '2025-05-30', 'Axel'),
(2, 4, 2, '2025-05-15', 'dadaw', 'dwadwa', '2025-05-29', 'Axel');

-- --------------------------------------------------------

--
-- Table structure for table `vaccinations`
--

CREATE TABLE `vaccinations` (
  `vaccination_id` int(11) NOT NULL AUTO_INCREMENT,
  `pet_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `vaccine` text NOT NULL,
  `dosage` text NOT NULL,
  `next_scheduled` date NOT NULL,
  `veterinarian` varchar(100) NOT NULL,
  PRIMARY KEY (`vaccination_id`),
  KEY `pet_id` (`pet_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `vaccinations_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  CONSTRAINT `vaccinations_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `vaccinations`
--

INSERT INTO `vaccinations` (`vaccination_id`, `pet_id`, `client_id`, `date`, `vaccine`, `dosage`, `next_scheduled`, `veterinarian`) VALUES
(1, 4, 2, '2025-05-14', 'dawddawdwa', 'dadaw', '2025-05-29', 'Axel'),
(2, 5, 3, '2025-05-14', 'dawda', 'nn', '2025-05-28', 'Axel');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`billing_id`),
  ADD KEY `client_id` (`client_id`),
  ADD KEY `pet_id` (`pet_id`);

--
-- Indexes for table `billing_services`
--
ALTER TABLE `billing_services`
  ADD PRIMARY KEY (`service_id`),
  ADD KEY `billing_id` (`billing_id`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`client_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `clinic_info`
--
ALTER TABLE `clinic_info`
  ADD PRIMARY KEY (`clinic_id`);

--
-- Indexes for table `consultations`
--
ALTER TABLE `consultations`
  ADD PRIMARY KEY (`consultation_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `deworming`
--
ALTER TABLE `deworming`
  ADD PRIMARY KEY (`deworming_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `grooming`
--
ALTER TABLE `grooming`
  ADD PRIMARY KEY (`grooming_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `other_treatments`
--
ALTER TABLE `other_treatments`
  ADD PRIMARY KEY (`treatment_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `password_history`
--
ALTER TABLE `password_history`
  ADD PRIMARY KEY (`history_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `pets`
--
ALTER TABLE `pets`
  ADD PRIMARY KEY (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `security_questions`
--
ALTER TABLE `security_questions`
  ADD PRIMARY KEY (`question_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `surgeries`
--
ALTER TABLE `surgeries`
  ADD PRIMARY KEY (`surgery_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_profiles`
--
ALTER TABLE `user_profiles`
  ADD PRIMARY KEY (`profile_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `vaccinations`
--
ALTER TABLE `vaccinations`
  ADD PRIMARY KEY (`vaccination_id`),
  ADD KEY `pet_id` (`pet_id`),
  ADD KEY `client_id` (`client_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `billing_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `billing_services`
--
ALTER TABLE `billing_services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `clinic_info`
--
ALTER TABLE `clinic_info`
  MODIFY `clinic_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `consultations`
--
ALTER TABLE `consultations`
  MODIFY `consultation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `deworming`
--
ALTER TABLE `deworming`
  MODIFY `deworming_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `grooming`
--
ALTER TABLE `grooming`
  MODIFY `grooming_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `other_treatments`
--
ALTER TABLE `other_treatments`
  MODIFY `treatment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `password_history`
--
ALTER TABLE `password_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pets`
--
ALTER TABLE `pets`
  MODIFY `pet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `security_questions`
--
ALTER TABLE `security_questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `surgeries`
--
ALTER TABLE `surgeries`
  MODIFY `surgery_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user_profiles`
--
ALTER TABLE `user_profiles`
  MODIFY `profile_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vaccinations`
--
ALTER TABLE `vaccinations`
  MODIFY `vaccination_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `billing`
--
ALTER TABLE `billing`
  ADD CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE;

--
-- Constraints for table `billing_services`
--
ALTER TABLE `billing_services`
  ADD CONSTRAINT `billing_services_ibfk_1` FOREIGN KEY (`billing_id`) REFERENCES `billing` (`billing_id`) ON DELETE CASCADE;

--
-- Constraints for table `consultations`
--
ALTER TABLE `consultations`
  ADD CONSTRAINT `consultations_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `consultations_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `deworming`
--
ALTER TABLE `deworming`
  ADD CONSTRAINT `deworming_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `deworming_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `grooming`
--
ALTER TABLE `grooming`
  ADD CONSTRAINT `grooming_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grooming_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `other_treatments`
--
ALTER TABLE `other_treatments`
  ADD CONSTRAINT `other_treatments_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `other_treatments_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `password_history`
--
ALTER TABLE `password_history`
  ADD CONSTRAINT `password_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `pets`
--
ALTER TABLE `pets`
  ADD CONSTRAINT `pets_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `security_questions`
--
ALTER TABLE `security_questions`
  ADD CONSTRAINT `security_questions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `surgeries`
--
ALTER TABLE `surgeries`
  ADD CONSTRAINT `surgeries_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `surgeries_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_profiles`
--
ALTER TABLE `user_profiles`
  ADD CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `vaccinations`
--
ALTER TABLE `vaccinations`
  ADD CONSTRAINT `vaccinations_ibfk_1` FOREIGN KEY (`pet_id`) REFERENCES `pets` (`pet_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vaccinations_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `clients` (`client_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
