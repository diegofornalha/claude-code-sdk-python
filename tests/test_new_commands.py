#!/usr/bin/env python3
"""Teste dos novos comandos de saída."""

import subprocess
import time

def test_commands():
    print("=== TESTANDO NOVOS COMANDOS ===\n")
    
    # Teste 1: Comando 's'
    print(">>> Teste 1: Comando 's' para sair")
    process = subprocess.Popen(
        ["./claude"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd="/home/codable/terminal/claude-code-sdk-python/wrappers_cli"
    )
    
    # Lê cabeçalho
    for _ in range(5):
        line = process.stdout.readline()
        if line:
            print(line.rstrip())
    
    # Envia 's' para sair
    print("\n>>> Enviando: 's'")
    process.stdin.write("s\n")
    process.stdin.flush()
    
    # Aguarda saída
    process.wait(timeout=2)
    print("✅ Comando 's' funcionou - processo saiu\n")
    
    # Teste 2: Comando 'sair'
    print(">>> Teste 2: Comando 'sair' para sair")
    process = subprocess.Popen(
        ["./claude"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd="/home/codable/terminal/claude-code-sdk-python/wrappers_cli"
    )
    
    # Pula cabeçalho
    for _ in range(6):
        process.stdout.readline()
    
    # Envia 'sair' para sair
    print(">>> Enviando: 'sair'")
    process.stdin.write("sair\n")
    process.stdin.flush()
    
    process.wait(timeout=2)
    print("✅ Comando 'sair' funcionou - processo saiu\n")
    
    # Teste 3: Comandos antigos não devem funcionar
    print(">>> Teste 3: Verificando que 'exit' e 'quit' não saem mais")
    process = subprocess.Popen(
        ["./claude"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd="/home/codable/terminal/claude-code-sdk-python/wrappers_cli"
    )
    
    # Pula cabeçalho
    for _ in range(6):
        process.stdout.readline()
    
    # Tenta 'exit' (não deve sair)
    print(">>> Enviando: 'exit' (deve ser tratado como pergunta)")
    process.stdin.write("exit\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Verifica se ainda está rodando
    if process.poll() is None:
        print("✅ 'exit' não saiu - tratado como mensagem normal")
        
        # Agora sai de verdade
        process.stdin.write("s\n")
        process.stdin.flush()
        process.wait(timeout=2)
    else:
        print("❌ 'exit' saiu incorretamente")
    
    print("\n=== TODOS OS TESTES CONCLUÍDOS ===")

if __name__ == "__main__":
    test_commands()