# SDK do Claude Code para Python - Versão Melhorada

## Instalação

### Via PyPI (Produção)
```bash
pip install claude-code-sdk-py
```

### Instalação Local (Desenvolvimento)

**Pré-requisitos:**
- Python 3.10+
- Node.js 
- Claude Code: `sudo npm install -g @anthropic-ai/claude-code`

#### Passos para instalação local:

1. **Clone o repositório e navegue até a pasta:**
```bash
cd /home/codable/terminal/claude-code-sdk-python
```

2. **Crie um ambiente virtual Python:**
```bash
python3 -m venv venv
```

3. **Ative o ambiente virtual e instale o SDK:**
```bash
source venv/bin/activate
pip install -e .
```

4. **Teste a instalação:**
```bash
python -m src "Olá, Claude!"
```

## Interfaces CLI Disponíveis

O SDK oferece duas interfaces de linha de comando:

### 1. Interface Rápida: `./wrappers_cli/claude`
Execução direta que não trava após responder. Ideal para scripts e automação.

```bash
cd wrappers_cli
chmod +x claude
./claude "Qual é a capital do Brasil?"
```

### 2. Interface Completa: `python -m src`
CLI completo com modos interativo, chat e ferramentas avançadas.

```bash
# Modo interativo
python -m src

# Query única
python -m src "Sua pergunta"

# Modo chat com contexto
python -m src --chat

# Com ferramentas específicas
python -m src --tools Read,Write "Leia o arquivo config.json"
```

Veja mais detalhes em [wrappers_cli/README.md](wrappers_cli/README.md)

## Problemas Resolvidos Durante a Instalação

### Conflito de Nomes com Módulo Python

**Problema:** O arquivo `types.py` do projeto conflitava com o módulo `types` padrão do Python, causando erro de importação circular.

**Solução:** 
1. Renomear `types.py` para `sdk_types.py`
2. Atualizar todas as importações no projeto:
```bash
find src -name "*.py" -exec sed -i 's/from \.types import/from .sdk_types import/g; s/from \.\.types import/from ..sdk_types import/g' {} \;
```

### Erro de Permissão ao Instalar Globalmente

**Problema:** `pip install -e .` falhava sem ambiente virtual.

**Solução:** Criar e usar um ambiente virtual Python isolado.

### Erro de Importação Relativa

**Problema:** `ImportError: attempted relative import with no known parent package`

**Solução:** Executar como módulo usando `python -m src` em vez de `python src/__main__.py`

## Início Rápido

```python
import anyio
from claude_code_sdk import query

async def main():
    async for message in query(prompt="Quanto é 2 + 2?"):
        print(message)

anyio.run(main)
```

## Uso

### Consulta Básica

```python
from claude_code_sdk import query, ClaudeCodeOptions, AssistantMessage, TextBlock

# Consulta simples
async for message in query(prompt="Olá Claude"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print(block.text)

# Com opções
options = ClaudeCodeOptions(
    system_prompt="Você é um assistente útil",
    max_turns=1
)

async for message in query(prompt="Me conte uma piada", options=options):
    print(message)
```

### Usando Ferramentas

```python
options = ClaudeCodeOptions(
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode='acceptEdits'  # aceitar automaticamente edições de arquivo
)

async for message in query(
    prompt="Crie um arquivo hello.py", 
    options=options
):
    # Processar uso de ferramentas e resultados
    pass
```

### Diretório de Trabalho

```python
from pathlib import Path

options = ClaudeCodeOptions(
    cwd="/caminho/para/projeto"  # ou Path("/caminho/para/projeto")
)
```

## Referência da API

### `query(prompt, options=None)`

Função assíncrona principal para consultar o Claude.

**Parâmetros:**
- `prompt` (str): O prompt para enviar ao Claude
- `options` (ClaudeCodeOptions): Configuração opcional

**Retorna:** AsyncIterator[Message] - Stream de mensagens de resposta

### Tipos

Veja [src/claude_code_sdk/types.py](src/claude_code_sdk/types.py) para definições completas de tipos:
- `ClaudeCodeOptions` - Opções de configuração
- `AssistantMessage`, `UserMessage`, `SystemMessage`, `ResultMessage` - Tipos de mensagem
- `TextBlock`, `ToolUseBlock`, `ToolResultBlock` - Blocos de conteúdo

## Tratamento de Erros

```python
from claude_code_sdk import (
    ClaudeSDKError,      # Erro base
    CLINotFoundError,    # Claude Code não instalado
    CLIConnectionError,  # Problemas de conexão
    ProcessError,        # Processo falhou
    CLIJSONDecodeError,  # Problemas ao analisar JSON
)

try:
    async for message in query(prompt="Olá"):
        pass
except CLINotFoundError:
    print("Por favor, instale o Claude Code")
except ProcessError as e:
    print(f"Processo falhou com código de saída: {e.exit_code}")
except CLIJSONDecodeError as e:
    print(f"Falha ao analisar resposta: {e}")
```

Veja [src/claude_code_sdk/_errors.py](src/claude_code_sdk/_errors.py) para todos os tipos de erro.

## Ferramentas Disponíveis

Consulte a [documentação do Claude Code](https://docs.anthropic.com/en/docs/claude-code/settings#tools-available-to-claude) para uma lista completa das ferramentas disponíveis.

## Exemplos

Veja [examples/quick_start.py](examples/quick_start.py) para um exemplo completo e funcional.

