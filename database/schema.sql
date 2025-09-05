-- Criação do banco de dados
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    funcao TEXT NOT NULL -- admin, assistente, voluntario
);

CREATE TABLE familias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    responsavel TEXT NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    necessidades TEXT
);

CREATE TABLE membros_familia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_familia INTEGER NOT NULL,
    nome TEXT NOT NULL,
    idade INTEGER,
    relacao TEXT,
    FOREIGN KEY (id_familia) REFERENCES familias (id)
);

CREATE TABLE atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_familia INTEGER NOT NULL,
    data TEXT NOT NULL,
    tipo_auxilio TEXT NOT NULL,
    observacoes TEXT,
    retorno_previsto TEXT,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_familia) REFERENCES familias (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
);
