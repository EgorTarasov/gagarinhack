-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS "news"(
    id bigserial primary key,
    title text,
    created_at timestamp,
    description text,
    image_link text
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE news;
-- +goose StatementEnd
