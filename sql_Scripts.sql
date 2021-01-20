
CREATE DATABASE IF NOT EXISTS todoapp;


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE IF NOT EXISTS `list` (
  `ListId` int(11) NOT NULL,
  `Title` varchar(250) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `DueDate` int(11) NOT NULL,
  `OwnerId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `listmembers` (
  `ListId` int(11) NOT NULL,
  `UserId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `task` (
  `TaskId` int(11) NOT NULL,
  `AssignedUserId` int(11) DEFAULT NULL,
  `ListId` int(11) NOT NULL,
  `Content` varchar(500) NOT NULL,
  `IsCompleted` tinyint(1) NOT NULL,
  `Point` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `user` (
  `UserId` int(11) NOT NULL,
  `Name` varchar(500) NOT NULL,
  `LastName` varchar(500) NOT NULL,
  `Password` varchar(500) NOT NULL,
  `Email` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `list`
  ADD PRIMARY KEY IF NOT EXISTS (`ListId`);


ALTER TABLE `task`
  ADD PRIMARY KEY IF NOT EXISTS (`TaskId`);


ALTER TABLE `user`
  ADD PRIMARY KEY IF NOT EXISTS (`UserId`);


ALTER TABLE `list`
  MODIFY `ListId` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `task`
  MODIFY `TaskId` int(11) NOT NULL AUTO_INCREMENT;


ALTER TABLE `user`
  MODIFY `UserId` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

