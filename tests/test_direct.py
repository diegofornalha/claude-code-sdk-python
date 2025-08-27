#!/usr/bin/env python3
"""Script direto para testar o problema"""

import sys
import asyncio
import pytest
sys.path.insert(0, '/home/codable/terminal/claude-code-sdk-python')

from src import query, AssistantMessage, TextBlock, ResultMessage

@pytest.mark.asyncio
@pytest.mark.timeout(10)
async def test_single_query():
    prompt = "teste"
    print(f"Testando com: {prompt}")
    
    try:
        response_received = False
        async for message in query(prompt=prompt):
            response_received = True
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Resposta: {block.text}")
            elif isinstance(message, ResultMessage):
                print(f"Tokens: {message.usage.input_tokens} in, {message.usage.output_tokens} out")
        
        if response_received:
            print("✓ Resposta processada com sucesso")
        else:
            print("✗ Nenhuma resposta recebida")
            
    except Exception as e:
        print(f"Erro: {e}")
    
    print("Script finalizado normalmente")
    return

if __name__ == "__main__":
    import signal
    
    def timeout_handler(signum, frame):
        print("⏱️ Timeout atingido, encerrando...")
        sys.exit(1)
    
    # Define timeout de 5 segundos para execução direta
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)
    
    try:
        asyncio.run(test_single_query())
    except SystemExit:
        pass
    finally:
        signal.alarm(0)  # Cancela o alarme
        print("Saindo...")
        sys.exit(0)