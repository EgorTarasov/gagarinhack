-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
ALTER TABLE IF EXISTS achievements
    ADD COLUMN IF NOT EXISTS type text;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
ALTER TABLE IF EXISTS achievements
    DROP COLUMN IF EXISTS type;
-- +goose StatementEnd
