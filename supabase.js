// supabase.js
const SUPABASE_URL = 'https://ojodoocwsgbprgxndtmp.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9qb2Rvb2N3c2dicHJneG5kdG1wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM2MzYyNTUsImV4cCI6MjA2OTIxMjI1NX0.Yp4lHyHLWugYmAGJQPwZMZP7TT0o2hSsWzW4-VVEwyk'; // ← your full anon key

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
