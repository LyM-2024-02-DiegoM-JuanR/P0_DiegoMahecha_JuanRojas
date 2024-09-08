import re

# Conjuntos para almacenar variables y funciones definidas dinámicamente
VARIABLES = []
MACROS = {}

# Especificación base de los tokens (excluyendo VARIABLE y MACRO)
base_tokens_specifications = [
    ("EXEC", r'exec'),  # Comando de ejecución
    ("DEFINITION", r'new|var|macro'),  # Definición de variables, macros
    ("COMMAND", r'turntomy|turntothe|walk|jump|drop|pick|grab|letgo|pop|moves|nop|safeexe'),  # Comandos
    ("CONTROL_STRUCTURE", r'if|then|else|fi|do|od|rep|times|per'),  # Estructuras de control
    ("CONDITIONAL", r'isblocked\?|isfacing\?|zero\?|not'),  # Condicionales
    ("VALUE", r'size|myx|myy|mychips|myballoons|balloonshere|chipshere|roomforchips'),  # Valores
    ("DIRECTION", r'left|right|back|front|forward|backwards'),  # Direcciones
    ("ORIENTATION", r'north|south|east|west'),  # Orientaciones
    ("NUMBER", r'\d+'),  # Números enteros
    ("ASSIGN", r'='),  # Operador de asignación
    ("END", r';'),  # Terminador de sentencias
    ("LPAREN", r'\('),  # Paréntesis izquierdo
    ("RPAREN", r'\)'),  # Paréntesis derecho
    ("LBRACE", r'\{'),  # Llave izquierda
    ("RBRACE", r'\}'),  # Llave derecha
    ("COMMA", r','),  # Coma
    ("NEWLINE", r'\n'),  # Nueva línea (ignorado)
    ("GENERIC", r'[a-z_][a-z0-9_]*') # Identificadores genéricos si no coincide otra cosa
]


def addVariable(variable_name):
    """Agrega una nueva variable a la lista de variables y recompila el lexer."""
    VARIABLES.append(variable_name)
    recompile_token_regex()
    

def removeVariable(variable_name):
    """Elimina una variable de la lista de variables y recompila el lexer."""
    if variable_name in VARIABLES:
        VARIABLES.remove(variable_name)
        recompile_token_regex()


def addMacro(macro_name, param_count):
    """Agrega una nueva entrada al diccionario de macros."""
    MACROS[macro_name] = param_count
    recompile_token_regex()


def getVariablesList():
    """Retorna la lista de variables"""
    return VARIABLES


def getMacrosDict():
    """Retorna el diccionaro de macros"""
    return MACROS


def generateTokenSpecifications():
    """Genera la especificación de los tokens dinámicamente con variables y macros."""
    dynamic_token_specifications = []

    if MACROS:
        function_pattern = '|'.join(re.escape(func) for func in MACROS)
        dynamic_token_specifications.append(("MACRO", function_pattern))
    else:
        dynamic_token_specifications.append(("MACRO", r'(?!)'))  # No hay funciones, no coincidirá nada

    if VARIABLES:
        variable_pattern = '|'.join(re.escape(var) for var in VARIABLES)
        dynamic_token_specifications.append(("VARIABLE", variable_pattern))
    else:
        dynamic_token_specifications.append(("VARIABLE", r'(?!)'))  # No hay variables, no coincidirá nada
    
    base_tokens_specifications_copy = base_tokens_specifications.copy()
    base_tokens_specifications_copy.insert(1, dynamic_token_specifications[0])
    base_tokens_specifications_copy.insert(9, dynamic_token_specifications[1])
    
    return base_tokens_specifications_copy


def recompile_token_regex():
    """Recompila las expresiones regulares."""
    global token_regex
    token_spec = generateTokenSpecifications()
    
    regex_patterns = [f'(?P<{name}>{pattern})' for name, pattern in token_spec]
    
    token_regex = '|'.join(regex_patterns)

# Inicializa el regex de los tokens al cargar el módulo
recompile_token_regex()

# Define el lexer/tokenizador con compilación dinámica de regex
def tokenize(input_text):
    """Convierte el texto de entrada en tokens."""
    input_text = input_text.lower()
    tokens = []
    
    for match in re.finditer(token_regex, input_text):
        token_type = match.lastgroup
        token_value = match.group(0)

        if token_type == "NEWLINE":
            continue  # Ignora nuevas líneas
        if token_type == "GENERIC" and token_value.strip() == "":
            continue  # Ignora espacios vacíos

        if token_type:
            tokens.append((token_type, token_value.strip()))

    return tokens