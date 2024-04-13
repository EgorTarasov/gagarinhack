-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
CREATE TABLE IF NOT EXISTS "achievements"(
    id bigserial primary key,
    user_id int,
    title text,
    date timestamp,
    place text,
    description text,
    event_link text,
    file_link text
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
DROP TABLE achievements;
-- +goose StatementEnd
