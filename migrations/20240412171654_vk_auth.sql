-- +goose Up
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
create table if not exists timetable  (
    id bigserial primary key,
    title text not null,
    weekday int not null,
    arrangement int not null, -- order in https://github.com/NextGen-LMS/lms-backend-schedule/blob/main/app/models/orm_models.py
    odd_even_week int not null,
    type text,
    lesson_time text
);

-- +goose Down
-- +goose StatementBegin
SELECT 'down SQL query';
drop table timetable;
-- +goose StatementEnd
