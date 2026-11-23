-- Таблица курсов учебного заведения «Цифровая Академия».
-- Студент: Даньшин Вадим (@82v-82)

CREATE TABLE `courses` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Первичный ключ курса',
    `specialty_id` INT UNSIGNED NOT NULL COMMENT 'Ссылка на специальность',
    `title` VARCHAR(150) NOT NULL COMMENT 'Название курса',
    `description` TEXT NULL COMMENT 'Описание курса',
    `duration_weeks` SMALLINT UNSIGNED NOT NULL COMMENT 'Продолжительность курса в неделях',

    PRIMARY KEY (`id`),
    KEY `idx_courses_specialty_id` (`specialty_id`),

    CONSTRAINT `fk_courses_specialty_id`
        FOREIGN KEY (`specialty_id`)
        REFERENCES `specialties` (`id`)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Курсы, относящиеся к специальностям';
