CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS chatbot;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create Organization table (public schema)
CREATE TABLE IF NOT EXISTS public.organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create User table (public schema)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    context JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    organization_id UUID NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    role VARCHAR DEFAULT 'user',
    email_verified BOOLEAN DEFAULT false,
    CONSTRAINT uq_email_org UNIQUE (email, organization_id),
    FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE
);

-- Create indexes for User table
CREATE INDEX idx_users_org_id ON public.users(organization_id);
CREATE INDEX idx_users_email ON public.users(email);

-- Create Session table (chatbot schema)
CREATE TABLE IF NOT EXISTS chatbot.sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    organization_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expiry_time TIMESTAMPTZ NOT NULL,
    deleted_at TIMESTAMPTZ NULL,
    context JSONB DEFAULT '{}'::jsonb,
    status VARCHAR NOT NULL DEFAULT 'active',
    device_info JSONB DEFAULT '{}'::jsonb,
    ip_address VARCHAR NULL,
    FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE
);

-- Create indexes for Session table
CREATE INDEX idx_sessions_user_id ON chatbot.sessions(user_id);
CREATE INDEX idx_sessions_org_id ON chatbot.sessions(organization_id);
CREATE INDEX idx_sessions_expiry_time ON chatbot.sessions(expiry_time);

-- Create Transaction table (chatbot schema)
CREATE TABLE IF NOT EXISTS chatbot.transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    organization_id UUID NOT NULL,
    user_id UUID NOT NULL,
    user_feedback VARCHAR NULL,
    positive_feedback BOOLEAN DEFAULT NULL,
    graph_state JSONB DEFAULT '{}'::jsonb,
    logs TEXT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expiry_at TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (session_id) REFERENCES chatbot.sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
);

-- Create indexes for Transaction table
CREATE INDEX idx_transactions_session_id ON chatbot.transactions(session_id);
CREATE INDEX idx_transactions_org_id ON chatbot.transactions(organization_id);
CREATE INDEX idx_transactions_user_id ON chatbot.transactions(user_id);