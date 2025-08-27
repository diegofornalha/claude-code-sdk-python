#!/usr/bin/env python3
"""Teste do modo chat único."""

import subprocess
import sys
import time

def test_chat():
    print("=== TESTANDO MODO CHAT INTERATIVO ===\n")
    
    # Inicia o processo do claude (sempre modo chat agora)
    process = subprocess.Popen(
        ["./claude"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd="/home/codable/terminal/claude-code-sdk-python/wrappers_cli"
    )
    
    # Lê o cabeçalho inicial
    for _ in range(5):
        line = process.stdout.readline()
        if line:
            print(line.rstrip())
    
    # Teste 1: Pergunta simples
    print("\n>>> Enviando: 'Quanto é 2 + 2?'")
    process.stdin.write("Quanto é 2 + 2?\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Lê resposta
    while True:
        line = process.stdout.readline()
        if not line or "👤 Você:" in line:
            break
        print(line.rstrip())
    
    # Teste 2: Pergunta com contexto
    print("\n>>> Enviando: 'Multiplique o resultado anterior por 5'")
    process.stdin.write("Multiplique o resultado anterior por 5\n")
    process.stdin.flush()
    time.sleep(2)
    
    # Lê resposta
    while True:
        line = process.stdout.readline()
        if not line or "👤 Você:" in line:
            break
        print(line.rstrip())
    
    # Teste 3: Limpar contexto
    print("\n>>> Enviando: 'clear'")
    process.stdin.write("clear\n")
    process.stdin.flush()
    time.sleep(1)
    
    # Lê resposta
    for _ in range(3):
        line = process.stdout.readline()
        if line:
            print(line.rstrip())
    
    # Teste 4: Sair
    print("\n>>> Enviando: 'sair'")
    process.stdin.write("sair\n")
    process.stdin.flush()
    
    # Aguarda processo terminar
    process.wait(timeout=5)
    
    print("\n=== TESTE CONCLUÍDO COM SUCESSO ===")

if __name__ == "__main__":
    test_chat()