#!/usr/bin/env python3
"""
Registra todo o projeto Claude Code SDK Python no Neo4j
Cria um grafo de conhecimento com arquivos, funções, classes e documentação
"""

import os
import ast
from pathlib import Path
from neo4j import GraphDatabase
from datetime import datetime
import hashlib

class ClaudeSDKToNeo4j:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "password")
        )
        self.project_root = Path("/home/codable/terminal/claude-code-sdk-python")
        self.files_data = []
        
    def analyze_python_file(self, file_path):
        """Analisa arquivo Python e extrai estrutura"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            # Extrair informações
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        'name': node.name,
                        'methods': methods,
                        'docstring': ast.get_docstring(node)
                    })
                elif isinstance(node, ast.FunctionDef):
                    # Apenas funções top-level
                    if node.col_offset == 0:
                        functions.append({
                            'name': node.name,
                            'docstring': ast.get_docstring(node),
                            'async': isinstance(node, ast.AsyncFunctionDef)
                        })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        
            return {
                'classes': classes,
                'functions': functions,
                'imports': list(set(imports)),
                'content': content[:2000]  # Primeiros 2000 chars
            }
        except Exception as e:
            print(f"⚠️ Erro ao analisar {file_path}: {e}")
            return None
            
    def scan_project(self):
        """Varre o projeto e coleta informações"""
        print("📂 Escaneando projeto Claude Code SDK Python...")
        
        # Arquivos importantes
        important_files = [
            "README.md",
            "pyproject.toml",
            "CLAUDE.md",
            "CHANGELOG.md"
        ]
        
        # Coletar arquivos de documentação
        for filename in important_files:
            file_path = self.project_root / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.files_data.append({
                    'path': str(file_path),
                    'name': filename,
                    'type': 'documentation',
                    'content': content[:5000],
                    'full_content': content if len(content) < 10000 else None
                })
                print(f"  ✓ {filename}")
        
        # Coletar arquivos Python
        for py_file in self.project_root.rglob("*.py"):
            # Pular arquivos de teste por enquanto
            if "test" in str(py_file):
                continue
                
            relative_path = py_file.relative_to(self.project_root)
            
            analysis = self.analyze_python_file(py_file)
            if analysis:
                self.files_data.append({
                    'path': str(py_file),
                    'name': py_file.name,
                    'relative_path': str(relative_path),
                    'type': 'python',
                    'analysis': analysis
                })
                print(f"  ✓ {relative_path}")
                
        print(f"\n📊 Total de arquivos coletados: {len(self.files_data)}")
        
    def save_to_neo4j(self):
        """Salva dados no Neo4j"""
        print("\n💾 Salvando no Neo4j...")
        
        with self.driver.session() as session:
            # Limpar dados antigos
            session.run("""
                MATCH (n:ClaudeSDKPython) DETACH DELETE n
            """)
            
            # Criar nó do projeto
            session.run("""
                CREATE (p:ClaudeSDKPython:Project {
                    name: 'Claude Code SDK Python',
                    path: $path,
                    version: '0.0.20',
                    description: 'Python SDK for Claude Code',
                    github: 'https://github.com/anthropics/claude-code-sdk-python',
                    created_at: datetime()
                })
            """, path=str(self.project_root))
            
            # Processar cada arquivo
            for file_data in self.files_data:
                if file_data['type'] == 'documentation':
                    # Salvar documentação
                    session.run("""
                        MATCH (p:ClaudeSDKPython:Project)
                        CREATE (d:ClaudeSDKPython:Documentation {
                            name: $name,
                            path: $path,
                            content: $content,
                            type: 'documentation',
                            file_type: $name
                        })
                        CREATE (p)-[:HAS_DOCUMENTATION]->(d)
                    """, 
                    name=file_data['name'],
                    path=file_data['path'],
                    content=file_data['content'])
                    
                elif file_data['type'] == 'python':
                    # Salvar arquivo Python
                    analysis = file_data['analysis']
                    
                    result = session.run("""
                        MATCH (p:ClaudeSDKPython:Project)
                        CREATE (f:ClaudeSDKPython:PythonFile {
                            name: $name,
                            path: $path,
                            relative_path: $relative_path,
                            content_preview: $content,
                            imports: $imports,
                            type: 'source_code'
                        })
                        CREATE (p)-[:CONTAINS_FILE]->(f)
                        
                        WITH f
                        UNWIND $classes as class_data
                        CREATE (c:ClaudeSDKPython:Class {
                            name: class_data.name,
                            methods: class_data.methods,
                            docstring: class_data.docstring,
                            file_path: $path
                        })
                        CREATE (f)-[:DEFINES_CLASS]->(c)
                        
                        WITH f
                        UNWIND $functions as func_data
                        CREATE (fn:ClaudeSDKPython:Function {
                            name: func_data.name,
                            async: func_data.async,
                            docstring: func_data.docstring,
                            file_path: $path
                        })
                        CREATE (f)-[:DEFINES_FUNCTION]->(fn)
                        
                        RETURN count(*) as created
                    """,
                    name=file_data['name'],
                    path=file_data['path'],
                    relative_path=file_data['relative_path'],
                    content=analysis['content'],
                    imports=analysis['imports'],
                    classes=analysis['classes'],
                    functions=analysis['functions'])
            
            # Criar relacionamentos entre arquivos baseado em imports
            session.run("""
                MATCH (f1:ClaudeSDKPython:PythonFile)
                MATCH (f2:ClaudeSDKPython:PythonFile)
                WHERE f1 <> f2
                  AND ANY(imp IN f1.imports WHERE f2.relative_path CONTAINS replace(imp, '.', '/'))
                CREATE (f1)-[:IMPORTS]->(f2)
            """)
            
            # Criar nó de conhecimento agregado
            session.run("""
                CREATE (k:ClaudeSDKPython:Knowledge {
                    name: 'Claude SDK Python Knowledge Base',
                    description: 'Base de conhecimento completa do SDK Python',
                    total_files: size([(f:ClaudeSDKPython:PythonFile) | f]),
                    total_classes: size([(c:ClaudeSDKPython:Class) | c]),
                    total_functions: size([(fn:ClaudeSDKPython:Function) | fn]),
                    created_at: datetime()
                })
                
                WITH k
                MATCH (p:ClaudeSDKPython:Project)
                CREATE (p)-[:HAS_KNOWLEDGE]->(k)
            """)
            
            # Estatísticas
            result = session.run("""
                MATCH (p:ClaudeSDKPython:Project)
                OPTIONAL MATCH (p)-[:CONTAINS_FILE]->(f:PythonFile)
                OPTIONAL MATCH (p)-[:HAS_DOCUMENTATION]->(d:Documentation)
                OPTIONAL MATCH (f)-[:DEFINES_CLASS]->(c:Class)
                OPTIONAL MATCH (f)-[:DEFINES_FUNCTION]->(fn:Function)
                RETURN count(distinct f) as files,
                       count(distinct d) as docs,
                       count(distinct c) as classes,
                       count(distinct fn) as functions
            """)
            stats = result.single()
            
            print(f"\n✅ Dados salvos no Neo4j:")
            print(f"   • Arquivos Python: {stats['files']}")
            print(f"   • Documentações: {stats['docs']}")
            print(f"   • Classes: {stats['classes']}")
            print(f"   • Funções: {stats['functions']}")
            
    def run(self):
        """Executa o processo completo"""
        print("🚀 Registrando Claude Code SDK Python no Neo4j\n")
        self.scan_project()
        self.save_to_neo4j()
        print("\n✨ Registro concluído!")
        print("\n🔍 Queries úteis:")
        print("   MATCH (p:ClaudeSDKPython:Project) RETURN p")
        print("   MATCH (c:ClaudeSDKPython:Class) RETURN c.name, c.methods")
        print("   MATCH (f:ClaudeSDKPython:Function) WHERE f.async = true RETURN f")
        print("   MATCH p=(:PythonFile)-[:IMPORTS]->(:PythonFile) RETURN p")
        
    def close(self):
        self.driver.close()

if __name__ == "__main__":
    registrar = ClaudeSDKToNeo4j()
    try:
        registrar.run()
    finally:
        registrar.close()