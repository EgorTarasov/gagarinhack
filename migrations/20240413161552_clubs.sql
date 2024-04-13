-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
CREATE TABLE IF NOT EXISTS "clubs"(
    id bigserial primary key,
    title text,
    description text,
    contact text
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
DROP TABLE clubs;
-- +goose StatementEnd
