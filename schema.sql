CREATE DATABASE IF NOT EXISTS wiki_db CHARACTER SET utf8mb4;
USE wiki_db;

CREATE TABLE users (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('member', 'admin') NOT NULL DEFAULT 'member',
    is_banned       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE documents (
    id                   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title                VARCHAR(255) NOT NULL,
    slug                 VARCHAR(255) NOT NULL UNIQUE,
    current_revision_id  BIGINT UNSIGNED NULL,
    created_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at           DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE revisions (
    id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    document_id    BIGINT UNSIGNED NOT NULL,
    content        MEDIUMTEXT NOT NULL,
    editor_id      BIGINT UNSIGNED NOT NULL,
    edit_comment   VARCHAR(255) NULL,
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (editor_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE documents
    ADD CONSTRAINT fk_current_revision
    FOREIGN KEY (current_revision_id) REFERENCES revisions(id);

CREATE TABLE page_views (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    document_id   BIGINT UNSIGNED NOT NULL,
    viewed_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id),
    INDEX idx_document_viewed (document_id, viewed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE search_logs (
    id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    query         VARCHAR(255) NOT NULL,
    searched_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_searched_at (searched_at),
    INDEX idx_query (query)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
