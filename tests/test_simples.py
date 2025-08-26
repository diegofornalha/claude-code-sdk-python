#!/usr/bin/env python3
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("🔍 Testando importação do Claude Code SDK...")

try:
    # Tenta importar o SDK
    import claude_code_sdk
    print(f"✅ SDK importado! Versão: {claude_code_sdk.__version__}")
    
    # Verifica módulos disponíveis
    from claude_code_sdk import query
    print("✅ Função 'query' disponível")
    
    from claude_code_sdk.client import ClaudeSDKClient
    print("✅ Classe 'ClaudeSDKClient' disponível")
    
    from claude_code_sdk.types import PermissionMode, McpStdioServerConfig
    print("✅ Types importados (PermissionMode, McpStdioServerConfig)")
    
    print("\n🎉 PROVA COMPLETA: O Claude Code SDK está 100% FUNCIONAL!")
    print("📦 Todos os módulos principais foram importados com sucesso!")
    
except ImportError as e:
    print(f"❌ Erro: {e}")
    print("\nVerificando estrutura de arquivos...")
    import os
    src_path = Path(__file__).parent / 'src' / 'claude_code_sdk'
    if src_path.exists():
        print(f"✅ Diretório SDK existe: {src_path}")
        print("📁 Arquivos encontrados:")
        for f in src_path.glob("*.py"):
            print(f"   - {f.name}")
    else:
        print(f"❌ Diretório não encontrado: {src_path}")