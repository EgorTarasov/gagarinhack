-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
create table if not exists vk_users(
    id         serial                  primary key,
    first_name text                    not null,
    last_name  text                    not null,
    photo_url  text                    not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null,
    bdate      timestamp               not null,
    sex        text                    not null,
    city       text                    not null,
    deleted    boolean  default false  not null
);

create table if not exists vk_groups(
    id          serial                  primary key,
    name        text                    not null,
    screen_name text                    not null,
    type        text                    not null,
    photo_200   text                    not null,
    created_at  timestamp default now() not null,
    updated_at  timestamp default now() not null,
    description text
);


create table user_group_association
(
    vk_user_id  integer
        references public.vk_users,
    vk_group_id integer
        references public.vk_groups
);

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
drop table user_group_association;
drop table vk_users;
drop table vk_groups;

-- +goose StatementEnd
