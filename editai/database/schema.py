SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,username TEXT,first_name TEXT,created_at REAL NOT NULL,last_seen REAL NOT NULL);
CREATE TABLE IF NOT EXISTS user_settings(user_id INTEGER PRIMARY KEY,profile TEXT NOT NULL,clip_count INTEGER NOT NULL,clip_duration INTEGER NOT NULL,vertical_mode TEXT NOT NULL,subtitles INTEGER NOT NULL,music INTEGER NOT NULL,updated_at REAL NOT NULL,FOREIGN KEY(user_id) REFERENCES users(user_id));
CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,user_id INTEGER NOT NULL,chat_id INTEGER NOT NULL,source_kind TEXT NOT NULL,source_value TEXT NOT NULL,status TEXT NOT NULL,settings_json TEXT NOT NULL,created_at REAL NOT NULL,updated_at REAL NOT NULL,error TEXT,analysis_path TEXT,manifest_path TEXT,output_count INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS idx_jobs_user_created ON jobs(user_id,created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE TABLE IF NOT EXISTS metrics(key TEXT PRIMARY KEY,value INTEGER NOT NULL DEFAULT 0,updated_at REAL NOT NULL);
"""
