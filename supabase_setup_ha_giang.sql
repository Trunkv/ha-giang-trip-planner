-- Chạy một lần trong Supabase: SQL Editor -> New query -> Run
create table if not exists public.trip_planner_data (
    id text primary key,
    data jsonb not null,
    updated_at timestamptz not null default now()
);

-- Ứng dụng dùng SUPABASE_SERVICE_ROLE_KEY lưu trong Streamlit Secrets.
-- Service role key bỏ qua RLS; không đưa key này vào mã nguồn/GitHub.
alter table public.trip_planner_data enable row level security;
