-- Script de inicialização do banco PostgreSQL
-- Este arquivo é executado automaticamente ao iniciar o container PostgreSQL

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_clientes_cpf ON clientes(cpf);
CREATE INDEX IF NOT EXISTS idx_contas_numero ON contas(numero);
CREATE INDEX IF NOT EXISTS idx_contas_cliente_id ON contas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_transacoes_conta_id ON transacoes(conta_id);
CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Grant permissões ao usuário bancario
GRANT CONNECT ON DATABASE banco_bancario TO bancario;
GRANT USAGE ON SCHEMA public TO bancario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bancario;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bancario;

COMMIT;
