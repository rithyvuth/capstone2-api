-- texts table
CREATE TABLE `texts` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `wav_name` varchar(255) DEFAULT NULL,
  `text` varchar(1000) NOT NULL,
  `status` varchar(100) NOT NULL,
  'user_id' int(11) DEFAULT NULL,
  `from_file` varchar(255) DEFAULT NULL,
  `deleted` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `users` (
  `id` int(11) PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
