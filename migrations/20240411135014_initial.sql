-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
CREATE TABLE IF NOT EXISTS "users"(
    id bigserial primary key,
    email text unique,
    pswd text,
    first_name text,
    last_name text,
    created_at timestamp default CURRENT_TIMESTAMP,
    updated_at timestamp default CURRENT_TIMESTAMP,
    deleted boolean default false,
    deleted_at timestamp default null
);
-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
DROP TABLE user;
-- +goose StatementEnd