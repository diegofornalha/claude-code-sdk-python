# SDK do Claude Code para Python

SDK Python para o Claude Code. Consulte a [documentação do SDK do Claude Code](https://docs.anthropic.com/en/docs/claude-code/sdk) para mais informações.

## Instalação

```bash
pip install claude-code-sdk
```

**Pré-requisitos:**
- Python 3.10+
- Node.js 
- Claude Code: `npm install -g @anthropic-ai/claude-code`

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

## Licença

MIT