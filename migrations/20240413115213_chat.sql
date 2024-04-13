-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
create table if not exists chat(
    id uuid primary key,
    created_at timestamp default current_timestamp
);

create table if not exists query(
    id bigserial primary key,
    fk_chat_id uuid references chat(id),
    body text not null,
    created_at timestamp default  current_timestamp
);

create table if not exists response(
    id bigserial primary key,
    fk_chat_id uuid references chat(id),
    fk_query_id bigint references query(id),
    body text not null,
    metadata text[]
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
drop table response;
drop table query;
drop table chat;
-- +goose StatementEnd
