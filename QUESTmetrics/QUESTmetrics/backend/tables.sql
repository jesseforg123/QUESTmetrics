CREATE TABLE `people` (
    `personId` int(11) NOT NULL AUTO_INCREMENT,
    `firstName` varchar(255) NOT NULL,
    `lastName` varchar(255) NOT NULL,
    `directoryId` varchar(255) NOT NULL,
    UNIQUE (`directoryId`),
    PRIMARY KEY (`personId`)
);

CREATE TABLE `groups` (
    `groupId` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `watch` boolean NOT NULL DEFAULT(0),
    `classId` int(11) NOT NULL,
    `groupHealth` int(11) NOT NULL DEFAULT (3),
    `groupScore` DOUBLE PRECISION NOT NULL DEFAULT (0),
    CONSTRAINT `fk_groups_classId_classes_classId` FOREIGN KEY (`classId`) REFERENCES `classes` (`classId`),
    UNIQUE (`name`),
    PRIMARY KEY (`groupId`)
);

CREATE TABLE `classes` (
    `classId` int(11) NOT NULL AUTO_INCREMENT,
    `className` varchar(255) NOT NULL,
    UNIQUE (`className`),
    PRIMARY KEY (`classId`)
);

CREATE TABLE `students` (
    `studentId` int(11) NOT NULL AUTO_INCREMENT,
    `uid` int(11),
    `personId` int(11) NOT NULL,
    PRIMARY KEY (`studentId`),
    UNIQUE (`uid`),
    CONSTRAINT `fk_students_personId_people_personId` FOREIGN KEY (`personId`) REFERENCES `people` (`personId`)
);

CREATE TABLE `student_teams` (
    `studentId` int(11) NOT NULL,
    `groupId` int(11) NOT NULL,
    PRIMARY KEY (`studentId`, `groupId`),
    CONSTRAINT `fk_student_teams_studentId_students_studentId` FOREIGN KEY (`studentId`) REFERENCES `students` (`studentId`),
    CONSTRAINT `fk_student_teams_groupId_groups_groupId` FOREIGN KEY (`groupId`) REFERENCES `groups` (`groupId`)
);
CREATE TABLE `slackData` (
    `messageId` int(11) NOT NULL AUTO_INCREMENT,
    `groupId` int(11) NOT NULL,
    `slackMsgId` varchar(255) NOT NULL,
    `channel` varchar(255) NOT NULL,
    `user` varchar(255) NOT NULL,
    `timestamp` VARCHAR (255) NOT NULL,
    PRIMARY KEY (`messageId`),
    CONSTRAINT `fk_slackData_groupId_groups_groupId` FOREIGN KEY (`groupId`) REFERENCES `groups` (`groupId`)
);
CREATE TABLE `elmsData` (
    `studentId` int(11) NOT NULL,
    `classId` int(11) NOT NULL,
    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `lastView` VARCHAR (255) NOT NULL,
    `currentGrade` FLOAT(5,2),
    `percentLate` FLOAT(4,4),
    PRIMARY KEY (`studentId`, `classId`, `timestamp`),
    CONSTRAINT `fk_elmsData_classId_classes_classId` FOREIGN KEY (`classId`) REFERENCES `classes` (`classId`),
    CONSTRAINT `fk_elmsData_studentId_students_studentId` FOREIGN KEY (`studentId`) REFERENCES `students` (`studentId`)
);

CREATE TABLE `admin` (
    `id` varchar(255) NOT NULL,
    `privileges` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `weights` (
    `id` varchar(255) NOT NULL,
    `slack` DOUBLE PRECISION NOT NULL DEFAULT 20,
    `grades` DOUBLE PRECISION NOT NULL DEFAULT 15,
    `lateness` DOUBLE PRECISION NOT NULL DEFAULT 17.5,
    `survey` DOUBLE PRECISION NOT NULL DEFAULT 30,
    `lastView` DOUBLE PRECISION NOT NULL DEFAULT 17.5,
    PRIMARY KEY (`id`)
);

CREATE TABLE `surveys` (
    `surveyId` int(11) NOT NULL AUTO_INCREMENT,
    `classId` int(11) NOT NULL,
    PRIMARY KEY (`surveyId`),
    CONSTRAINT `fk_surveys_classId_classes_classId` FOREIGN KEY (`classId`) REFERENCES `classes` (`classId`)
);

CREATE TABLE `questions` (
    `questionId` int(11) NOT NULL AUTO_INCREMENT,
    `surveyId` int(11) NOT NULL,
    `question` TEXT NOT NULL,
    PRIMARY KEY (`questionId`),
    CONSTRAINT `fk_questions_surveyId_surveys_surveyId` FOREIGN KEY (`surveyId`) REFERENCES `surveys` (`surveyId`)
);

CREATE TABLE `answers` (
    `answerId` int(11) NOT NULL AUTO_INCREMENT,
    `studentId` int(11) NOT NULL,
    `questionId` int(11) NOT NULL,
    `answer` TEXT NOT NULL,
    PRIMARY KEY (`answerId`),
    CONSTRAINT `fk_answers_studentId_students_studentId` FOREIGN KEY (`studentId`) REFERENCES `students` (`studentId`),
    CONSTRAINT `fk_answers_questionId_questions_questionId` FOREIGN KEY (`questionId`) REFERENCES `questions` (`questionId`)
);

CREATE TABLE `surveyHistory` (
    `historyId` int(11) NOT NULL AUTO_INCREMENT,
    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `classId` int(11) NOT NULL,
    `data` JSON NOT NULL ,
    PRIMARY KEY (`historyId`, `timestamp`),
    CONSTRAINT `fk_history_classId_classes_classId` FOREIGN KEY (`classId`) REFERENCES `classes` (`classId`)
);
